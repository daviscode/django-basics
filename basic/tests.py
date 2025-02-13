from django.test import TestCase
from graphene.test import Client
from basic.schema import schema  # Adjust the import according to your project structure
from basic.models import Currency, QRCode, Product  # Adjust the import according to your project structure
from django.contrib.auth.models import User
from graphql_jwt.shortcuts import get_token

class GraphQLAPITestCase(TestCase):
    def setUp(self):
        self.client = Client(schema)
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = get_token(self.user)

        # Create some test data
        self.currency = Currency.objects.create(code='USD', name='US Dollar', symbol='$')
        self.qr_code = QRCode.objects.create(product_id=1, qr_code_data='sample_data', dynamic=False)
        self.product = Product.objects.create(name='Sample Product', description='A sample product.', price=100.0, currency_id=self.currency.id, category='Sample')

    def test_query_currency(self):
        query = '''
        query {
            currency(id: "%s") {
                code
                name
                symbol
            }
        }
        ''' % self.currency.id

        executed = self.client.execute(query, context_value={'user': self.user})
        self.assertIsNone(executed.errors)
        self.assertEqual(executed.data['currency']['code'], 'USD')
        self.assertEqual(executed.data['currency']['name'], 'US Dollar')
        self.assertEqual(executed.data['currency']['symbol'], '$')

    def test_query_all_currencies(self):
        query = '''
        query {
            allCurrencies {
                edges {
                    node {
                        code
                        name
                        symbol
                    }
                }
            }
        }
        '''

        executed = self.client.execute(query, context_value={'user': self.user})
        self.assertIsNone(executed.errors)
        self.assertEqual(len(executed.data['allCurrencies']['edges']), 1)
        self.assertEqual(executed.data['allCurrencies']['edges'][0]['node']['code'], 'USD')

    def test_create_currency(self):
        mutation = '''
        mutation {
            createCurrency(input: {code: "EUR", name: "Euro", symbol: "€"}) {
                currency {
                    code
                    name
                    symbol
                }
                success
                errors
            }
        }
        '''

        executed = self.client.execute(mutation, context_value={'user': self.user})
        self.assertIsNone(executed.errors)
        self.assertTrue(executed.data['createCurrency']['success'])
        self.assertEqual(executed.data['createCurrency']['currency']['code'], 'EUR')

    def test_update_currency(self):
        mutation = '''
        mutation {
            updateCurrency(id: "%s", input: {name: "US Dollar Updated"}) {
                currency {
                    name
                }
                success
                errors
            }
        }
        ''' % self.currency.id

        executed = self.client.execute(mutation, context_value={'user': self.user})
        self.assertIsNone(executed.errors)
        self.assertTrue(executed.data['updateCurrency']['success'])
        self.assertEqual(executed.data['updateCurrency']['currency']['name'], 'US Dollar Updated')

    def test_delete_currency(self):
        mutation = '''
        mutation {
            deleteCurrency(id: "%s") {
                success
                errors
            }
        }
        ''' % self.currency.id

        executed = self.client.execute(mutation, context_value={'user': self.user})
        self.assertIsNone(executed.errors)
        self.assertTrue(executed.data['deleteCurrency']['success'])

    # Similar tests can be written for QRCode and Product queries and mutations

    def test_query_qr_code(self):
        query = '''
        query {
            qrCode(id: "%s") {
                qrCodeData
                dynamic
            }
        }
        ''' % self.qr_code.id

        executed = self.client.execute(query, context_value={'user': self.user})
        self.assertIsNone(executed.errors)
        self.assertEqual(executed.data['qrCode']['qrCodeData'], 'sample_data')
        self.assertFalse(executed.data['qrCode']['dynamic'])

    def test_query_all_qr_codes(self):
        query = '''
        query {
            allQrCodes {
                edges {
                    node {
                        qrCodeData
                        dynamic
                    }
                }
            }
        }
        '''

        executed = self.client.execute(query, context_value={'user': self.user})
        self.assertIsNone(executed.errors)
        self.assertEqual(len(executed.data['allQrCodes']['edges']), 1)
        self.assertEqual(executed.data['allQrCodes']['edges'][0]['node']['qrCodeData'], 'sample_data')

    def test_create_qr_code(self):
        mutation = '''
        mutation {
            createQrCode(input: {productId: 1, qrCodeData: "new_data", dynamic: true}) {
                qrCode {
                    qrCodeData
                    dynamic
                }
                success
                errors
            }
        }
        '''

        executed = self.client.execute(mutation, context_value={'user': self.user})
        self.assertIsNone(executed.errors)
        self.assertTrue(executed.data['createQrCode']['success'])
        self.assertEqual(executed.data['createQrCode']['qrCode']['qrCodeData'], 'new_data')
        self.assertTrue(executed.data['createQrCode']['qrCode']['dynamic'])

    def test_update_qr_code(self):
        mutation = '''
        mutation {
            updateQrCode(id: "%s", input: {qrCodeData: "updated_data"}) {
                qrCode {
                    qrCodeData
                }
                success
                errors
            }
        }
        ''' % self.qr_code.id

        executed = self.client.execute(mutation, context_value={'user': self.user})
        self.assertIsNone(executed.errors)
        self.assertTrue(executed.data['updateQrCode']['success'])
        self.assertEqual(executed.data['updateQrCode']['qrCode']['qrCodeData'], 'updated_data')

    def test_delete_qr_code(self):
        mutation = '''
        mutation {
            deleteQrCode(id: "%s") {
                success
                errors
            }
        }
        ''' % self.qr_code.id

        executed = self.client.execute(mutation, context_value={'user': self.user})
        self.assertIsNone(executed.errors)
        self.assertTrue(executed.data['deleteQrCode']['success'])

    def test_query_product(self):
        query = '''
        query {
            product(id: "%s") {
                name
                description
                price
            }
        }
        ''' % self.product.id

        executed = self.client.execute(query, context_value={'user': self.user})
        self.assertIsNone(executed.errors)
        self.assertEqual(executed.data['product']['name'], 'Sample Product')
        self.assertEqual(executed.data['product']['description'], 'A sample product.')
        self.assertEqual(executed.data['product']['price'], 100.0)

    def test_query_all_products(self):
        query = '''
        query {
            allProducts {
                edges {
                    node {
                        name
                        description
                        price
                    }
                }
            }
        }
        '''

        executed = self.client.execute(query, context_value={'user': self.user})
        self.assertIsNone(executed.errors)
        self.assertEqual(len(executed.data['allProducts']['edges']), 1)
        self.assertEqual(executed.data['allProducts']['edges'][0]['node']['name'], 'Sample Product')

    def test_create_product(self):
        mutation = '''
        mutation {
            createProduct(input: {name: "New Product", description: "A new product.", price: 200.0, currencyId: "%s", category: "New"}) {
                product {
                    name
                    description
                    price
                }
                success
                errors
            }
        }
        ''' % self.currency.id

        executed = self.client.execute(mutation, context_value={'user': self.user})
        self.assertIsNone(executed.errors)
        self.assertTrue(executed.data['createProduct']['success'])
        self.assertEqual(executed.data['createProduct']['product']['name'], 'New Product')

    def test_update_product(self):
        mutation = '''
        mutation {
            updateProduct(id: "%s", input: {name: "Updated Product"}) {
                product {
                    name
                }
                success
                errors
            }
        }
        ''' % self.product.id

        executed = self.client.execute(mutation, context_value={'user': self.user})
        self.assertIsNone(executed.errors)
        self.assertTrue(executed.data['updateProduct']['success'])
        self.assertEqual(executed.data['updateProduct']['product']['name'], 'Updated Product')

    def test_delete_product(self):
        mutation = '''
        mutation {
            deleteProduct(id: "%s") {
                success
                errors
            }
        }
        ''' % self.product.id

        executed = self.client.execute(mutation, context_value={'user': self.user})
        self.assertIsNone(executed.errors)
        self.assertTrue(executed.data['deleteProduct']['success'])
