from datetime import datetime
from app import create_app, db, Client, Product, ProformaInvoice, InvoiceItem, generate_invoice_number


class TestAppCreation:
    def test_app_creates(self, app):
        assert app is not None
        assert app.config['TESTING'] is True

    def test_database_setup(self, app):
        with app.app_context():
            assert db.engine is not None

    def test_dashboard(self, client):
        resp = client.get('/')
        assert resp.status_code == 200
        assert b'GCS CRM Dashboard' in resp.data


class TestClientCRUD:
    def test_client_list(self, client):
        resp = client.get('/clients')
        assert resp.status_code == 200

    def test_client_create(self, client, app):
        resp = client.post('/clients/new', data={
            'company_name': 'Acme Corp',
            'email': 'info@acme.com',
            'phone': '123456',
            'address': '123 Main St',
            'city': 'Nairobi',
            'country': 'Kenya',
        }, follow_redirects=True)
        assert resp.status_code == 200
        with app.app_context():
            c = Client.query.filter_by(company_name='Acme Corp').first()
            assert c is not None
            assert c.email == 'info@acme.com'

    def test_client_detail(self, client, app):
        with app.app_context():
            c = Client(company_name='Test Co')
            db.session.add(c)
            db.session.commit()
            cid = c.id
        resp = client.get(f'/clients/{cid}')
        assert resp.status_code == 200
        assert b'Test Co' in resp.data

    def test_client_edit(self, client, app):
        with app.app_context():
            c = Client(company_name='Old Name')
            db.session.add(c)
            db.session.commit()
            cid = c.id
        resp = client.post(f'/clients/{cid}/edit', data={
            'company_name': 'New Name',
            'email': '', 'phone': '', 'address': '', 'city': '', 'country': '',
        }, follow_redirects=True)
        assert resp.status_code == 200
        with app.app_context():
            c = db.session.get(Client, cid)
            assert c.company_name == 'New Name'

    def test_client_delete(self, client, app):
        with app.app_context():
            c = Client(company_name='Delete Me')
            db.session.add(c)
            db.session.commit()
            cid = c.id
        resp = client.post(f'/clients/{cid}/delete', follow_redirects=True)
        assert resp.status_code == 200
        with app.app_context():
            assert db.session.get(Client, cid) is None


class TestProductCRUD:
    def test_product_list(self, client):
        resp = client.get('/products')
        assert resp.status_code == 200

    def test_product_create(self, client, app):
        resp = client.post('/products/new', data={
            'name': 'Widget',
            'description': 'A fine widget',
            'unit_price': '29.99',
            'unit': 'piece',
        }, follow_redirects=True)
        assert resp.status_code == 200
        with app.app_context():
            p = Product.query.filter_by(name='Widget').first()
            assert p is not None
            assert p.unit_price == 29.99

    def test_product_edit(self, client, app):
        with app.app_context():
            p = Product(name='OldProduct', unit_price=10.0)
            db.session.add(p)
            db.session.commit()
            pid = p.id
        resp = client.post(f'/products/{pid}/edit', data={
            'name': 'NewProduct',
            'description': '',
            'unit_price': '20.00',
            'unit': 'unit',
        }, follow_redirects=True)
        assert resp.status_code == 200
        with app.app_context():
            p = db.session.get(Product, pid)
            assert p.name == 'NewProduct'
            assert p.unit_price == 20.0

    def test_product_delete(self, client, app):
        with app.app_context():
            p = Product(name='Gone', unit_price=5.0)
            db.session.add(p)
            db.session.commit()
            pid = p.id
        resp = client.post(f'/products/{pid}/delete', follow_redirects=True)
        assert resp.status_code == 200
        with app.app_context():
            assert db.session.get(Product, pid) is None


class TestProformaInvoice:
    def _create_client(self, app):
        with app.app_context():
            c = Client(company_name='Invoice Client')
            db.session.add(c)
            db.session.commit()
            return c.id

    def test_invoice_number_generation(self, app):
        with app.app_context():
            num1 = generate_invoice_number()
            year = datetime.utcnow().year
            assert num1 == f'GCS-PI-{year}-0001'

            c = Client(company_name='Test')
            db.session.add(c)
            db.session.commit()

            inv = ProformaInvoice(
                invoice_number=num1,
                client_id=c.id,
                date_issued=datetime.utcnow().date(),
            )
            db.session.add(inv)
            db.session.commit()

            num2 = generate_invoice_number()
            assert num2 == f'GCS-PI-{year}-0002'

    def test_invoice_creation(self, client, app):
        cid = self._create_client(app)
        today = datetime.utcnow().strftime('%Y-%m-%d')
        resp = client.post('/proforma-invoices/new', data={
            'client_id': cid,
            'date_issued': today,
            'valid_until': '',
            'status': 'Draft',
            'notes': 'Test invoice',
            'tax_rate': '16',
            'item_description': ['Service A'],
            'item_quantity': ['2'],
            'item_unit_price': ['100'],
            'item_product_id': [''],
        }, follow_redirects=True)
        assert resp.status_code == 200
        with app.app_context():
            inv = ProformaInvoice.query.first()
            assert inv is not None
            assert inv.invoice_number.startswith('GCS-PI-')

    def test_invoice_total_calculation(self, app):
        with app.app_context():
            c = Client(company_name='Calc Client')
            db.session.add(c)
            db.session.commit()

            inv = ProformaInvoice(
                invoice_number='GCS-PI-2025-9999',
                client_id=c.id,
                date_issued=datetime.utcnow().date(),
                tax_rate=16.0,
            )
            db.session.add(inv)
            db.session.flush()

            item1 = InvoiceItem(
                proforma_invoice_id=inv.id,
                description='Item A',
                quantity=2,
                unit_price=100,
                total=200,
            )
            item2 = InvoiceItem(
                proforma_invoice_id=inv.id,
                description='Item B',
                quantity=1,
                unit_price=50,
                total=50,
            )
            db.session.add_all([item1, item2])
            db.session.flush()

            from app import recalculate_invoice
            recalculate_invoice(inv)
            db.session.commit()

            assert inv.subtotal == 250.0
            assert inv.tax_amount == 40.0
            assert inv.total == 290.0

    def test_invoice_list(self, client):
        resp = client.get('/proforma-invoices')
        assert resp.status_code == 200

    def test_invoice_detail(self, client, app):
        cid = self._create_client(app)
        with app.app_context():
            inv = ProformaInvoice(
                invoice_number='GCS-PI-2025-0001',
                client_id=cid,
                date_issued=datetime.utcnow().date(),
            )
            db.session.add(inv)
            db.session.commit()
            iid = inv.id
        resp = client.get(f'/proforma-invoices/{iid}')
        assert resp.status_code == 200
        assert b'GCS-PI-2025-0001' in resp.data
