import os
from datetime import datetime, timedelta, timezone
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import (
    StringField, TextAreaField, DecimalField, SelectField,
    IntegerField, FieldList, FormField, HiddenField, FloatField
)
from wtforms.validators import DataRequired, Email, Optional, NumberRange

db = SQLAlchemy()


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(50))
    address = db.Column(db.String(300))
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    contacts = db.relationship('Contact', backref='client', lazy=True, cascade='all, delete-orphan')
    invoices = db.relationship('ProformaInvoice', backref='client', lazy=True)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(50))
    position = db.Column(db.String(100))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    unit_price = db.Column(db.Float, nullable=False, default=0)
    unit = db.Column(db.String(50), default='unit')


class ProformaInvoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(50), unique=True, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    date_issued = db.Column(db.Date, default=lambda: datetime.now(timezone.utc).date())
    valid_until = db.Column(db.Date)
    status = db.Column(db.String(20), default='Draft')
    notes = db.Column(db.Text)
    subtotal = db.Column(db.Float, default=0)
    tax_rate = db.Column(db.Float, default=16.0)
    tax_amount = db.Column(db.Float, default=0)
    total = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    items = db.relationship('InvoiceItem', backref='invoice', lazy=True, cascade='all, delete-orphan')


class InvoiceItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    proforma_invoice_id = db.Column(db.Integer, db.ForeignKey('proforma_invoice.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=True)
    description = db.Column(db.String(300), nullable=False)
    quantity = db.Column(db.Float, nullable=False, default=1)
    unit_price = db.Column(db.Float, nullable=False, default=0)
    total = db.Column(db.Float, nullable=False, default=0)
    product = db.relationship('Product')


# ---------------------------------------------------------------------------
# Forms
# ---------------------------------------------------------------------------

class ClientForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired()])
    email = StringField('Email', validators=[Optional()])
    phone = StringField('Phone', validators=[Optional()])
    address = StringField('Address', validators=[Optional()])
    city = StringField('City', validators=[Optional()])
    country = StringField('Country', validators=[Optional()])


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[Optional()])
    phone = StringField('Phone', validators=[Optional()])
    position = StringField('Position', validators=[Optional()])
    client_id = SelectField('Client', coerce=int, validators=[DataRequired()])


class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    unit_price = DecimalField('Unit Price', validators=[DataRequired(), NumberRange(min=0)])
    unit = StringField('Unit', validators=[Optional()], default='unit')


class InvoiceForm(FlaskForm):
    client_id = SelectField('Client', coerce=int, validators=[DataRequired()])
    date_issued = StringField('Date Issued', validators=[DataRequired()])
    valid_until = StringField('Valid Until', validators=[Optional()])
    status = SelectField('Status', choices=[
        ('Draft', 'Draft'), ('Sent', 'Sent'), ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'), ('Expired', 'Expired')
    ])
    notes = TextAreaField('Notes', validators=[Optional()])
    tax_rate = DecimalField('Tax Rate (%)', default=16.0, validators=[Optional()])


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def generate_invoice_number():
    year = datetime.now(timezone.utc).year
    prefix = f"GCS-PI-{year}-"
    last = ProformaInvoice.query.filter(
        ProformaInvoice.invoice_number.like(f"{prefix}%")
    ).order_by(ProformaInvoice.id.desc()).first()
    if last:
        last_num = int(last.invoice_number.split('-')[-1])
        next_num = last_num + 1
    else:
        next_num = 1
    return f"{prefix}{next_num:04d}"


def recalculate_invoice(invoice):
    subtotal = sum(item.total for item in invoice.items)
    invoice.subtotal = round(subtotal, 2)
    invoice.tax_amount = round(subtotal * invoice.tax_rate / 100, 2)
    invoice.total = round(invoice.subtotal + invoice.tax_amount, 2)


# ---------------------------------------------------------------------------
# App factory
# ---------------------------------------------------------------------------

def create_app(config=None):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'gcs-crm-dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', 'sqlite:///crm.db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if config:
        app.config.update(config)

    db.init_app(app)
    CSRFProtect(app)

    with app.app_context():
        db.create_all()

    # -------------------------------------------------------------------
    # Dashboard
    # -------------------------------------------------------------------
    @app.route('/')
    def dashboard():
        total_clients = Client.query.count()
        total_products = Product.query.count()
        total_invoices = ProformaInvoice.query.count()
        pending_invoices = ProformaInvoice.query.filter_by(status='Draft').count()
        recent_invoices = ProformaInvoice.query.order_by(
            ProformaInvoice.created_at.desc()
        ).limit(5).all()
        return render_template('dashboard.html',
                               total_clients=total_clients,
                               total_products=total_products,
                               total_invoices=total_invoices,
                               pending_invoices=pending_invoices,
                               recent_invoices=recent_invoices)

    # -------------------------------------------------------------------
    # Clients
    # -------------------------------------------------------------------
    @app.route('/clients')
    def client_list():
        clients = Client.query.order_by(Client.company_name).all()
        return render_template('clients/list.html', clients=clients)

    @app.route('/clients/new', methods=['GET', 'POST'])
    def client_new():
        form = ClientForm()
        if form.validate_on_submit():
            client = Client(
                company_name=form.company_name.data,
                email=form.email.data,
                phone=form.phone.data,
                address=form.address.data,
                city=form.city.data,
                country=form.country.data,
            )
            db.session.add(client)
            db.session.commit()
            flash('Client created successfully.', 'success')
            return redirect(url_for('client_detail', id=client.id))
        return render_template('clients/form.html', form=form, title='New Client')

    @app.route('/clients/<int:id>')
    def client_detail(id):
        client = Client.query.get_or_404(id)
        return render_template('clients/detail.html', client=client)

    @app.route('/clients/<int:id>/edit', methods=['GET', 'POST'])
    def client_edit(id):
        client = Client.query.get_or_404(id)
        form = ClientForm(obj=client)
        if form.validate_on_submit():
            form.populate_obj(client)
            db.session.commit()
            flash('Client updated successfully.', 'success')
            return redirect(url_for('client_detail', id=client.id))
        return render_template('clients/form.html', form=form, title='Edit Client')

    @app.route('/clients/<int:id>/delete', methods=['POST'])
    def client_delete(id):
        client = Client.query.get_or_404(id)
        db.session.delete(client)
        db.session.commit()
        flash('Client deleted successfully.', 'success')
        return redirect(url_for('client_list'))

    # -------------------------------------------------------------------
    # Contacts
    # -------------------------------------------------------------------
    @app.route('/contacts')
    def contact_list():
        contacts = Contact.query.order_by(Contact.name).all()
        return render_template('contacts/list.html', contacts=contacts)

    @app.route('/contacts/new', methods=['GET', 'POST'])
    def contact_new():
        form = ContactForm()
        form.client_id.choices = [(c.id, c.company_name) for c in Client.query.order_by(Client.company_name).all()]
        if form.validate_on_submit():
            contact = Contact(
                name=form.name.data,
                email=form.email.data,
                phone=form.phone.data,
                position=form.position.data,
                client_id=form.client_id.data,
            )
            db.session.add(contact)
            db.session.commit()
            flash('Contact created successfully.', 'success')
            return redirect(url_for('contact_list'))
        return render_template('contacts/form.html', form=form, title='New Contact')

    @app.route('/contacts/<int:id>/edit', methods=['GET', 'POST'])
    def contact_edit(id):
        contact = Contact.query.get_or_404(id)
        form = ContactForm(obj=contact)
        form.client_id.choices = [(c.id, c.company_name) for c in Client.query.order_by(Client.company_name).all()]
        if form.validate_on_submit():
            form.populate_obj(contact)
            db.session.commit()
            flash('Contact updated successfully.', 'success')
            return redirect(url_for('contact_list'))
        return render_template('contacts/form.html', form=form, title='Edit Contact')

    @app.route('/contacts/<int:id>/delete', methods=['POST'])
    def contact_delete(id):
        contact = Contact.query.get_or_404(id)
        db.session.delete(contact)
        db.session.commit()
        flash('Contact deleted successfully.', 'success')
        return redirect(url_for('contact_list'))

    # -------------------------------------------------------------------
    # Products
    # -------------------------------------------------------------------
    @app.route('/products')
    def product_list():
        products = Product.query.order_by(Product.name).all()
        return render_template('products/list.html', products=products)

    @app.route('/products/new', methods=['GET', 'POST'])
    def product_new():
        form = ProductForm()
        if form.validate_on_submit():
            product = Product(
                name=form.name.data,
                description=form.description.data,
                unit_price=float(form.unit_price.data),
                unit=form.unit.data or 'unit',
            )
            db.session.add(product)
            db.session.commit()
            flash('Product created successfully.', 'success')
            return redirect(url_for('product_list'))
        return render_template('products/form.html', form=form, title='New Product')

    @app.route('/products/<int:id>/edit', methods=['GET', 'POST'])
    def product_edit(id):
        product = Product.query.get_or_404(id)
        form = ProductForm(obj=product)
        if form.validate_on_submit():
            product.name = form.name.data
            product.description = form.description.data
            product.unit_price = float(form.unit_price.data)
            product.unit = form.unit.data or 'unit'
            db.session.commit()
            flash('Product updated successfully.', 'success')
            return redirect(url_for('product_list'))
        return render_template('products/form.html', form=form, title='Edit Product')

    @app.route('/products/<int:id>/delete', methods=['POST'])
    def product_delete(id):
        product = Product.query.get_or_404(id)
        db.session.delete(product)
        db.session.commit()
        flash('Product deleted successfully.', 'success')
        return redirect(url_for('product_list'))

    # -------------------------------------------------------------------
    # Proforma Invoices
    # -------------------------------------------------------------------
    @app.route('/proforma-invoices')
    def invoice_list():
        invoices = ProformaInvoice.query.order_by(ProformaInvoice.created_at.desc()).all()
        return render_template('invoices/list.html', invoices=invoices)

    @app.route('/proforma-invoices/new', methods=['GET', 'POST'])
    def invoice_new():
        form = InvoiceForm()
        form.client_id.choices = [(c.id, c.company_name) for c in Client.query.order_by(Client.company_name).all()]
        products = Product.query.order_by(Product.name).all()

        if request.method == 'POST' and form.validate():
            invoice = ProformaInvoice(
                invoice_number=generate_invoice_number(),
                client_id=form.client_id.data,
                date_issued=datetime.strptime(form.date_issued.data, '%Y-%m-%d').date(),
                status=form.status.data,
                notes=form.notes.data,
                tax_rate=float(form.tax_rate.data) if form.tax_rate.data else 16.0,
            )
            if form.valid_until.data:
                invoice.valid_until = datetime.strptime(form.valid_until.data, '%Y-%m-%d').date()

            descriptions = request.form.getlist('item_description')
            quantities = request.form.getlist('item_quantity')
            unit_prices = request.form.getlist('item_unit_price')
            product_ids = request.form.getlist('item_product_id')

            for i in range(len(descriptions)):
                if not descriptions[i]:
                    continue
                qty = float(quantities[i]) if quantities[i] else 1
                price = float(unit_prices[i]) if unit_prices[i] else 0
                item = InvoiceItem(
                    description=descriptions[i],
                    quantity=qty,
                    unit_price=price,
                    total=round(qty * price, 2),
                    product_id=int(product_ids[i]) if product_ids[i] else None,
                )
                invoice.items.append(item)

            db.session.add(invoice)
            db.session.flush()
            recalculate_invoice(invoice)
            db.session.commit()
            flash('Proforma invoice created successfully.', 'success')
            return redirect(url_for('invoice_detail', id=invoice.id))

        today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        valid = (datetime.now(timezone.utc) + timedelta(days=30)).strftime('%Y-%m-%d')
        return render_template('invoices/form.html', form=form, title='New Proforma Invoice',
                               products=products, today=today, valid=valid)

    @app.route('/proforma-invoices/<int:id>')
    def invoice_detail(id):
        invoice = ProformaInvoice.query.get_or_404(id)
        return render_template('invoices/detail.html', invoice=invoice)

    @app.route('/proforma-invoices/<int:id>/edit', methods=['GET', 'POST'])
    def invoice_edit(id):
        invoice = ProformaInvoice.query.get_or_404(id)
        form = InvoiceForm(obj=invoice)
        form.client_id.choices = [(c.id, c.company_name) for c in Client.query.order_by(Client.company_name).all()]
        products = Product.query.order_by(Product.name).all()

        if request.method == 'POST' and form.validate():
            invoice.client_id = form.client_id.data
            invoice.date_issued = datetime.strptime(form.date_issued.data, '%Y-%m-%d').date()
            invoice.status = form.status.data
            invoice.notes = form.notes.data
            invoice.tax_rate = float(form.tax_rate.data) if form.tax_rate.data else 16.0
            if form.valid_until.data:
                invoice.valid_until = datetime.strptime(form.valid_until.data, '%Y-%m-%d').date()
            else:
                invoice.valid_until = None

            # Clear existing items
            InvoiceItem.query.filter_by(proforma_invoice_id=invoice.id).delete()

            descriptions = request.form.getlist('item_description')
            quantities = request.form.getlist('item_quantity')
            unit_prices = request.form.getlist('item_unit_price')
            product_ids = request.form.getlist('item_product_id')

            for i in range(len(descriptions)):
                if not descriptions[i]:
                    continue
                qty = float(quantities[i]) if quantities[i] else 1
                price = float(unit_prices[i]) if unit_prices[i] else 0
                item = InvoiceItem(
                    description=descriptions[i],
                    quantity=qty,
                    unit_price=price,
                    total=round(qty * price, 2),
                    product_id=int(product_ids[i]) if product_ids[i] else None,
                )
                invoice.items.append(item)

            db.session.flush()
            recalculate_invoice(invoice)
            db.session.commit()
            flash('Proforma invoice updated successfully.', 'success')
            return redirect(url_for('invoice_detail', id=invoice.id))

        if request.method == 'GET':
            form.date_issued.data = invoice.date_issued.strftime('%Y-%m-%d') if invoice.date_issued else ''
            form.valid_until.data = invoice.valid_until.strftime('%Y-%m-%d') if invoice.valid_until else ''

        return render_template('invoices/form.html', form=form, title='Edit Proforma Invoice',
                               products=products, invoice=invoice,
                               today=None, valid=None)

    @app.route('/proforma-invoices/<int:id>/delete', methods=['POST'])
    def invoice_delete(id):
        invoice = ProformaInvoice.query.get_or_404(id)
        db.session.delete(invoice)
        db.session.commit()
        flash('Proforma invoice deleted successfully.', 'success')
        return redirect(url_for('invoice_list'))

    @app.route('/proforma-invoices/<int:id>/pdf')
    def invoice_pdf(id):
        invoice = ProformaInvoice.query.get_or_404(id)
        html = render_template('invoices/pdf.html', invoice=invoice)
        try:
            from weasyprint import HTML
            pdf = HTML(string=html).write_pdf()
            from flask import make_response
            response = make_response(pdf)
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = \
                f'inline; filename={invoice.invoice_number}.pdf'
            return response
        except (ImportError, OSError):
            flash('PDF generation is not available. Showing HTML preview.', 'warning')
            return html

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=os.environ.get('FLASK_DEBUG', 'false').lower() == 'true')
