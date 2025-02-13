# Import necessary modules and classes
import graphene  # Base library for building GraphQL APIs in Python
from graphene_django import DjangoObjectType, DjangoConnectionField  # Integration of GraphQL with Django
from graphene import relay  # Relay library for pagination and connections
from .models import Currency, QRCode, Product  # Import Django models
from django.core.exceptions import ObjectDoesNotExist, ValidationError  # Django exceptions
from graphql_jwt.decorators import login_required  # JWT authentication decorator
import graphql_jwt  # JWT authentication for GraphQL
from datetime import timedelta  # For handling date and time

# Utility function to format errors
def format_errors(e):
    if isinstance(e, ValidationError):
        return [f"{field}: {error}" for field, error in e.message_dict.items()]
    return [str(e)]

# Define GraphQL types for the models with relay.Node for pagination
class CurrencyType(DjangoObjectType):
    class Meta:
        model = Currency  # Associate with the Currency model
        fields = "__all__"  # Include all fields from the model
        interfaces = (relay.Node,)  # Enable pagination with Relay
        filter_fields = {
            'code': ['exact', 'icontains'],  # Define filterable fields
            'name': ['exact', 'icontains'],
            'symbol': ['exact', 'icontains'],
        }
        description = "Represents a currency with code, name, and symbol."

    name = graphene.String(description="The name of the currency.")
    symbol = graphene.String(description="The symbol of the currency.")

    def resolve_name(self, info):
        # Resolve the name field, potentially using cached data
        cached_data = Currency.get_cached_name_and_symbol(self.code)
        return cached_data['name'] if cached_data else self.name

    def resolve_symbol(self, info):
        # Resolve the symbol field, potentially using cached data
        cached_data = Currency.get_cached_name_and_symbol(self.code)
        return cached_data['symbol'] if cached_data else self.symbol

class QRCodeType(DjangoObjectType):
    class Meta:
        model = QRCode  # Associate with the QRCode model
        fields = "__all__"  # Include all fields from the model
        interfaces = (relay.Node,)  # Enable pagination with Relay
        filter_fields = {
            'product_id': ['exact'],  # Define filterable fields
            'qr_code_data': ['exact', 'icontains'],
            'expiry_date': ['exact', 'lt', 'gt'],
            'dynamic': ['exact'],
        }
        description = "Represents a QR code associated with a product."

class ProductType(DjangoObjectType):
    class Meta:
        model = Product  # Associate with the Product model
        fields = "__all__"  # Include all fields from the model
        interfaces = (relay.Node,)  # Enable pagination with Relay
        filter_fields = {
            'name': ['exact', 'icontains'],  # Define filterable fields
            'description': ['exact', 'icontains'],
            'price': ['exact', 'lt', 'gt'],
            'currency_id': ['exact'],
            'category': ['exact', 'icontains'],
            'eco_friendly': ['exact'],
        }
        description = "Represents a product with name, description, price, and other details."

# Define queries with pagination and filtering
class Query(graphene.ObjectType):
    currency = relay.Node.Field(CurrencyType, description="Retrieve a currency by ID.")
    all_currencies = DjangoConnectionField(CurrencyType, description="Retrieve all currencies with filtering and pagination.")

    qr_code = relay.Node.Field(QRCodeType, description="Retrieve a QR code by ID.")
    all_qr_codes = DjangoConnectionField(QRCodeType, description="Retrieve all QR codes with filtering and pagination.")

    product = relay.Node.Field(ProductType, description="Retrieve a product by ID.")
    all_products = DjangoConnectionField(ProductType, description="Retrieve all products with filtering and pagination.")

    @login_required  # Requires authentication
    def resolve_currency(self, info, id):
        try:
            return Currency.objects.get(pk=id)  # Retrieve a currency by ID
        except ObjectDoesNotExist:
            return None

    @login_required  # Requires authentication
    def resolve_qr_code(self, info, id):
        try:
            return QRCode.objects.get(pk=id)  # Retrieve a QR code by ID
        except ObjectDoesNotExist:
            return None

    @login_required  # Requires authentication
    def resolve_product(self, info, id):
        try:
            return Product.objects.get(pk=id)  # Retrieve a product by ID
        except ObjectDoesNotExist:
            return None

# Define input types for mutations
class CurrencyInput(graphene.InputObjectType):
    code = graphene.String(required=True, description="The code of the currency.")
    name = graphene.String(required=True, description="The name of the currency.")
    symbol = graphene.String(required=True, description="The symbol of the currency.")

class QRCodeInput(graphene.InputObjectType):
    product_id = graphene.Int(required=True, description="The ID of the associated product.")
    qr_code_data = graphene.String(required=True, description="The data for the QR code.")
    expiry_date = graphene.DateTime(description="The expiry date of the QR code.")
    dynamic = graphene.Boolean(description="Whether the QR code is dynamic.")

class ProductInput(graphene.InputObjectType):
    name = graphene.String(required=True, description="The name of the product.")
    description = graphene.String(description="The description of the product.")
    price = graphene.Decimal(required=True, description="The price of the product.")
    currency_id = graphene.Int(required=True, description="The ID of the associated currency.")
    category = graphene.String(required=True, description="The category of the product.")
    qr_code_id = graphene.Int(description="The ID of the associated QR code.")
    eco_friendly = graphene.Boolean(description="Whether the product is eco-friendly.")
    image = graphene.String(description="The image URL of the product.")

# Define mutations for Currency
class CreateCurrency(graphene.Mutation):
    class Arguments:
        input = CurrencyInput(required=True)

    currency = graphene.Field(CurrencyType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    @login_required  # Requires authentication
    def mutate(self, info, input):
        try:
            currency = Currency(**input)
            currency.full_clean()  # Validate the model
            currency.save()
            return CreateCurrency(currency=currency, success=True, errors=None)
        except Exception as e:
            return CreateCurrency(currency=None, success=False, errors=format_errors(e))

class UpdateCurrency(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True, description="The ID of the currency to update.")
        input = CurrencyInput(required=True)

    currency = graphene.Field(CurrencyType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    @login_required  # Requires authentication
    def mutate(self, info, id, input):
        try:
            currency = Currency.objects.get(pk=id)
            for key, value in input.items():
                setattr(currency, key, value)
            currency.full_clean()  # Validate the model
            currency.save()
            return UpdateCurrency(currency=currency, success=True, errors=None)
        except ObjectDoesNotExist:
            return UpdateCurrency(currency=None, success=False, errors=["Currency not found"])
        except Exception as e:
            return UpdateCurrency(currency=None, success=False, errors=format_errors(e))

class DeleteCurrency(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True, description="The ID of the currency to delete.")

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    @login_required  # Requires authentication
    def mutate(self, info, id):
        try:
            currency = Currency.objects.get(pk=id)
            currency.delete()
            return DeleteCurrency(success=True, errors=None)
        except ObjectDoesNotExist:
            return DeleteCurrency(success=False, errors=["Currency not found"])
        except Exception as e:
            return DeleteCurrency(success=False, errors=format_errors(e))

# Define mutations for QRCode
class CreateQRCode(graphene.Mutation):
    class Arguments:
        input = QRCodeInput(required=True)

    qr_code = graphene.Field(QRCodeType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    @login_required  # Requires authentication
    def mutate(self, info, input):
        try:
            qr_code = QRCode(**input)
            qr_code.full_clean()  # Validate the model
            qr_code.save()
            return CreateQRCode(qr_code=qr_code, success=True, errors=None)
        except Exception as e:
            return CreateQRCode(qr_code=None, success=False, errors=format_errors(e))

class UpdateQRCode(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True, description="The ID of the QR code to update.")
        input = QRCodeInput(required=True)

    qr_code = graphene.Field(QRCodeType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    @login_required  # Requires authentication
    def mutate(self, info, id, input):
        try:
            qr_code = QRCode.objects.get(pk=id)
            for key, value in input.items():
                setattr(qr_code, key, value)
            qr_code.full_clean()  # Validate the model
            qr_code.save()
            return UpdateQRCode(qr_code=qr_code, success=True, errors=None)
        except ObjectDoesNotExist:
            return UpdateQRCode(qr_code=None, success=False, errors=["QR Code not found"])
        except Exception as e:
            return UpdateQRCode(qr_code=None, success=False, errors=format_errors(e))

class DeleteQRCode(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True, description="The ID of the QR code to delete.")

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    @login_required  # Requires authentication
    def mutate(self, info, id):
        try:
            qr_code = QRCode.objects.get(pk=id)
            qr_code.delete()
            return DeleteQRCode(success=True, errors=None)
        except ObjectDoesNotExist:
            return DeleteQRCode(success=False, errors=["QR Code not found"])
        except Exception as e:
            return DeleteQRCode(success=False, errors=format_errors(e))

# Define mutations for Product
class CreateProduct(graphene.Mutation):
    class Arguments:
        input = ProductInput(required=True)

    product = graphene.Field(ProductType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    @login_required  # Requires authentication
    def mutate(self, info, input):
        try:
            product = Product(**input)
            product.full_clean()  # Validate the model
            product.save()
            return CreateProduct(product=product, success=True, errors=None)
        except Exception as e:
            return CreateProduct(product=None, success=False, errors=format_errors(e))

class UpdateProduct(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True, description="The ID of the product to update.")
        input = ProductInput(required=True)

    product = graphene.Field(ProductType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    @login_required  # Requires authentication
    def mutate(self, info, id, input):
        try:
            product = Product.objects.get(pk=id)
            for key, value in input.items():
                setattr(product, key, value)
            product.full_clean()  # Validate the model
            product.save()
            return UpdateProduct(product=product, success=True, errors=None)
        except ObjectDoesNotExist:
            return UpdateProduct(product=None, success=False, errors=["Product not found"])
        except Exception as e:
            return UpdateProduct(product=None, success=False, errors=format_errors(e))

class DeleteProduct(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True, description="The ID of the product to delete.")

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    @login_required  # Requires authentication
    def mutate(self, info, id):
        try:
            product = Product.objects.get(pk=id)
            product.delete()
            return DeleteProduct(success=True, errors=None)
        except ObjectDoesNotExist:
            return DeleteProduct(success=False, errors=["Product not found"])
        except Exception as e:
            return DeleteProduct(success=False, errors=format_errors(e))

# Define mutation class
class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()  # Obtain JWT token
    verify_token = graphql_jwt.Verify.Field()  # Verify JWT token
    refresh_token = graphql_jwt.Refresh.Field()  # Refresh JWT token
    revoke_token = graphql_jwt.Revoke.Field()

    create_currency = CreateCurrency.Field()
    update_currency = UpdateCurrency.Field()
    delete_currency = DeleteCurrency.Field()

    create_qr_code = CreateQRCode.Field()
    update_qr_code = UpdateQRCode.Field()
    delete_qr_code = DeleteQRCode.Field()

    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()
    delete_product = DeleteProduct.Field()

# Create the schema
schema = graphene.Schema(query=Query, mutation=Mutation)
