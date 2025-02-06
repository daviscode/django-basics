import graphene
from graphene_django import DjangoObjectType
from .models import Currency, QRCode, Product
from django.core.exceptions import ObjectDoesNotExist, ValidationError

# Define GraphQL types for the models
class CurrencyType(DjangoObjectType):
    class Meta:
        model = Currency
        fields = "__all__"

class QRCodeType(DjangoObjectType):
    class Meta:
        model = QRCode
        fields = "__all__"

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = "__all__"

# Define queries
class Query(graphene.ObjectType):
    all_currencies = graphene.List(CurrencyType)
    currency = graphene.Field(CurrencyType, id=graphene.Int())

    all_qr_codes = graphene.List(QRCodeType)
    qr_code = graphene.Field(QRCodeType, id=graphene.Int())

    all_products = graphene.List(ProductType)
    product = graphene.Field(ProductType, id=graphene.Int())

    def resolve_all_currencies(self, info, **kwargs):
        return Currency.objects.all()

    def resolve_currency(self, info, id):
        try:
            return Currency.objects.get(pk=id)
        except ObjectDoesNotExist:
            return None

    def resolve_all_qr_codes(self, info, **kwargs):
        return QRCode.objects.all()

    def resolve_qr_code(self, info, id):
        try:
            return QRCode.objects.get(pk=id)
        except ObjectDoesNotExist:
            return None

    def resolve_all_products(self, info, **kwargs):
        return Product.objects.all()

    def resolve_product(self, info, id):
        try:
            return Product.objects.get(pk=id)
        except ObjectDoesNotExist:
            return None

# Define mutations with error handling
class CreateCurrency(graphene.Mutation):
    class Arguments:
        code = graphene.String(required=True)
        name = graphene.String(required=True)
        symbol = graphene.String(required=True)

    currency = graphene.Field(CurrencyType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    def mutate(self, info, code, name, symbol):
        try:
            currency = Currency(code=code, name=name, symbol=symbol)
            currency.full_clean()  # Validate the model before saving
            currency.save()
            return CreateCurrency(currency=currency, success=True, errors=None)
        except ValidationError as e:
            errors = [f"{field}: {error}" for field, error in e.message_dict.items()]
            return CreateCurrency(currency=None, success=False, errors=errors)
        except Exception as e:
            return CreateCurrency(currency=None, success=False, errors=[str(e)])

class UpdateCurrency(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        code = graphene.String()
        name = graphene.String()
        symbol = graphene.String()

    currency = graphene.Field(CurrencyType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    def mutate(self, info, id, code=None, name=None, symbol=None):
        try:
            currency = Currency.objects.get(pk=id)
            if code:
                currency.code = code
            if name:
                currency.name = name
            if symbol:
                currency.symbol = symbol
            currency.full_clean()  # Validate the model before saving
            currency.save()
            return UpdateCurrency(currency=currency, success=True, errors=None)
        except ObjectDoesNotExist:
            return UpdateCurrency(currency=None, success=False, errors=["Currency not found"])
        except ValidationError as e:
            errors = [f"{field}: {error}" for field, error in e.message_dict.items()]
            return UpdateCurrency(currency=None, success=False, errors=errors)
        except Exception as e:
            return UpdateCurrency(currency=None, success=False, errors=[str(e)])

class DeleteCurrency(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    def mutate(self, info, id):
        try:
            currency = Currency.objects.get(pk=id)
            currency.delete()
            return DeleteCurrency(success=True, errors=None)
        except ObjectDoesNotExist:
            return DeleteCurrency(success=False, errors=["Currency not found"])
        except Exception as e:
            return DeleteCurrency(success=False, errors=[str(e)])

class CreateQRCode(graphene.Mutation):
    class Arguments:
        product_id = graphene.Int(required=True)
        qr_code_data = graphene.String(required=True)
        expiry_date = graphene.DateTime()
        dynamic = graphene.Boolean()

    qr_code = graphene.Field(QRCodeType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    def mutate(self, info, product_id, qr_code_data, expiry_date=None, dynamic=False):
        try:
            qr_code = QRCode(product_id=product_id, qr_code_data=qr_code_data, expiry_date=expiry_date, dynamic=dynamic)
            qr_code.full_clean()  # Validate the model before saving
            qr_code.save()
            return CreateQRCode(qr_code=qr_code, success=True, errors=None)
        except ValidationError as e:
            errors = [f"{field}: {error}" for field, error in e.message_dict.items()]
            return CreateQRCode(qr_code=None, success=False, errors=errors)
        except Exception as e:
            return CreateQRCode(qr_code=None, success=False, errors=[str(e)])

class UpdateQRCode(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        product_id = graphene.Int()
        qr_code_data = graphene.String()
        expiry_date = graphene.DateTime()
        dynamic = graphene.Boolean()

    qr_code = graphene.Field(QRCodeType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    def mutate(self, info, id, product_id=None, qr_code_data=None, expiry_date=None, dynamic=None):
        try:
            qr_code = QRCode.objects.get(pk=id)
            if product_id:
                qr_code.product_id = product_id
            if qr_code_data:
                qr_code.qr_code_data = qr_code_data
            if expiry_date:
                qr_code.expiry_date = expiry_date
            if dynamic is not None:
                qr_code.dynamic = dynamic
            qr_code.full_clean()  # Validate the model before saving
            qr_code.save()
            return UpdateQRCode(qr_code=qr_code, success=True, errors=None)
        except ObjectDoesNotExist:
            return UpdateQRCode(qr_code=None, success=False, errors=["QR Code not found"])
        except ValidationError as e:
            errors = [f"{field}: {error}" for field, error in e.message_dict.items()]
            return UpdateQRCode(qr_code=None, success=False, errors=errors)
        except Exception as e:
            return UpdateQRCode(qr_code=None, success=False, errors=[str(e)])

class DeleteQRCode(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    def mutate(self, info, id):
        try:
            qr_code = QRCode.objects.get(pk=id)
            qr_code.delete()
            return DeleteQRCode(success=True, errors=None)
        except ObjectDoesNotExist:
            return DeleteQRCode(success=False, errors=["QR Code not found"])
        except Exception as e:
            return DeleteQRCode(success=False, errors=[str(e)])

class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()
        price = graphene.Decimal(required=True)
        currency_id = graphene.Int(required=True)
        category = graphene.String(required=True)
        qr_code_id = graphene.Int()
        eco_friendly = graphene.Boolean()
        image = graphene.String()

    product = graphene.Field(ProductType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    def mutate(self, info, name, description, price, currency_id, category, qr_code_id=None, eco_friendly=False, image=None):
        try:
            product = Product(
                name=name,
                description=description,
                price=price,
                currency_id=currency_id,
                category=category,
                qr_code_id=qr_code_id,
                eco_friendly=eco_friendly,
                image=image
            )
            product.full_clean()  # Validate the model before saving
            product.save()
            return CreateProduct(product=product, success=True, errors=None)
        except ValidationError as e:
            errors = [f"{field}: {error}" for field, error in e.message_dict.items()]
            return CreateProduct(product=None, success=False, errors=errors)
        except Exception as e:
            return CreateProduct(product=None, success=False, errors=[str(e)])

class UpdateProduct(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        description = graphene.String()
        price = graphene.Decimal()
        currency_id = graphene.Int()
        category = graphene.String()
        qr_code_id = graphene.Int()
        eco_friendly = graphene.Boolean()
        image = graphene.String()

    product = graphene.Field(ProductType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    def mutate(self, info, id, name=None, description=None, price=None, currency_id=None, category=None, qr_code_id=None, eco_friendly=None, image=None):
        try:
            product = Product.objects.get(pk=id)
            if name:
                product.name = name
            if description:
                product.description = description
            if price:
                product.price = price
            if currency_id:
                product.currency_id = currency_id
            if category:
                product.category = category
            if qr_code_id:
                product.qr_code_id = qr_code_id
            if eco_friendly is not None:
                product.eco_friendly = eco_friendly
            if image:
                product.image = image
            product.full_clean()  # Validate the model before saving
            product.save()
            return UpdateProduct(product=product, success=True, errors=None)
        except ObjectDoesNotExist:
            return UpdateProduct(product=None, success=False, errors=["Product not found"])
        except ValidationError as e:
            errors = [f"{field}: {error}" for field, error in e.message_dict.items()]
            return UpdateProduct(product=None, success=False, errors=errors)
        except Exception as e:
            return UpdateProduct(product=None, success=False, errors=[str(e)])

class DeleteProduct(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    def mutate(self, info, id):
        try:
            product = Product.objects.get(pk=id)
            product.delete()
            return DeleteProduct(success=True, errors=None)
        except ObjectDoesNotExist:
            return DeleteProduct(success=False, errors=["Product not found"])
        except Exception as e:
            return DeleteProduct(success=False, errors=[str(e)])

class Mutation(graphene.ObjectType):
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
