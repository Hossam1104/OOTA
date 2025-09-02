import json
import os
from datetime import datetime

import pyodbc  # For database connection
import requests
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# API URLs with descriptive names
API_URLS = {
    "Adam Pharmacy - Production": "http://10.2.1.6/RmsMainServerApi/api/Order/CreateAndAssignOrder",
    "Adam Pharmacy - Testing": "http://10.2.1.6:8080/RmsMainServerApi/api/Order/CreateAndAssignOrder",
    "UPC Pharmacy - Production": "http://10.10.10.181/RmsMainServerApi/api/Order/CreateAndAssignOrder",
    "UPC Pharmacy - Testing": "http://10.10.9.181:8080/RmsMainServerApi/api/Order/CreateAndAssignOrder",
    "Whites Pharmacy - Production": "https://10.10.20.200/Gateway/RmsMainServerApi/api/Order/CreateAndAssignOrder",
    "Whites Pharmacy - Testing": "http://10.10.20.126:8090/RmsMainServerApi/api/Order/CreateAndAssignOrder"
}

# Default API endpoint
DEFAULT_API_ENDPOINT = "UPC Pharmacy - Testing"

# Updated Payment options
PAYMENT_METHODS = ["Visa", "Points", "Tamara", "Tabby", "MisPay", "Emkan", "YouGotaGift", "OgMoney", "PostToCredit"]
PAYMENT_STATUSES = ["done_payment", "partially_paid", "not_payment", "failed_payment", "refunded_payment"]
PAYMENT_OPTIONS = {
    "Visa": ["visa", "mastercard", "mada", "other"],
    "Points": ["points"],
    "Tamara": ["tamara"],
    "Tabby": ["tabby"],
    "MisPay": ["MisPay"],
    "Emkan": ["Emkan"],
    "YouGotaGift": ["YouGotaGift"],
    "OgMoney": ["OgMoney"],
    "PostToCredit": ["PostToCredit"]
}

# Updated Default data
DEFAULT_DATA = {
    "branch_code": "2000",
    "order_code": "Order_1",
    "parent_order_code": "",
    "order_creation_date": "2025-05-18T12:23:10.323Z",
    "order_notes": "Don't Ring the bell",
    "order_product_total_value": 73.75,
    "is_delivery": 1,
    "order_delivery_cost": 10.0,
    "order_total_discount": 45.0,
    "order_final_total_value": 83.75,
    "order_payment_method": "PostToCredit",
    "order_status": "new",
    "client_country_code": "966",
    "client_phone": "556028080",
    "client_first_name": "Hossam",
    "client_middle_name": "Mohamed",
    "client_last_name": "Abdallah",
    "client_email": "Hossam.Mohamed@dbsmena.com",
    "client_birthdate": "1989-04-11T12:23:10.323Z",
    "client_gender": "Male",
    "order_address": "Tabarak City",
    "address_code": "1104",
    "order_country_code": "966",
    "order_phone": "556028080",
    "order_payment_status": "not_payment",
    "order_gps": [29.980759787217856, 31.33627436833347],
    "delivery_date": "2025-09-01",
    "delivery_from_time": "12:23:10.323",
    "delivery_to_time": "03:23:10",
    "shipping_address_2": "Cairo",
    "fullfilment_plant": "1000",
    "order_products": [
        {
            "item_code": "000000000000021252",
            "item_name": "J&J Tb Reach Interdntl Full Me",
            "quantity": 2.0,
            "unit_price": 11.00,
            "unit_vat_amount": 0.0,
            "total_vat_amount": 0.0,
            "vat_percentage": 0.0,
            "offer_code": "",
            "offer_message": "",
            "row_total_discount": 0.0,
            "row_net_total": 22.0
        },
        {
            "item_code": "000000000000021241",
            "item_name": "The Balm Meet Matt Hughes - Brilliant",
            "quantity": 1.0,
            "unit_price": 90.00,
            "unit_vat_amount": 6.75,
            "total_vat_amount": 6.75,
            "vat_percentage": 0.15,
            "offer_code": "000000000011",
            "offer_message": "Buy One Get One",
            "row_total_discount": 45.0,
            "row_net_total": 51.75
        }
    ],
    "payment_methods_with_options": [
        {
            "payment_method": "PostToCredit",
            "payment_amount": 83.75,
            "transaction_id": "",
            "payment_option": "",
            "card_name": "null",
            "bank_code": "null",
            "option_commission": 0.0,
            "credit_customer_info": {
                "customer_number": "0057000096",
                "customer_name": "Moller Customer"
            }
        }
    ]
}


# Database connection function
def get_db_connection():
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=.;'
            'DATABASE=RMSCashierSrv;'
            'UID=sa;'
            'PWD=P@ssw0rd'
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {str(e)}")
        return None


# Initialize session data
@app.before_request
def before_request():
    if 'order_data' not in session:
        # Try to load from saved data, otherwise use default
        saved_data = session.get('saved_order_data', {})
        if saved_data:
            session['order_data'] = saved_data
        else:
            session['order_data'] = DEFAULT_DATA.copy()

    if 'products' not in session:
        saved_products = session.get('saved_products', [])
        if saved_products:
            session['products'] = saved_products
        else:
            session['products'] = DEFAULT_DATA['order_products'].copy()

    if 'payments' not in session:
        saved_payments = session.get('saved_payments', [])
        if saved_payments:
            session['payments'] = saved_payments
        else:
            session['payments'] = DEFAULT_DATA['payment_methods_with_options'].copy()

    if 'api_endpoint' not in session:
        session['api_endpoint'] = DEFAULT_API_ENDPOINT


@app.route('/')
def index():
    return redirect(url_for('order_details'))


@app.route('/order-details')
def order_details():
    return render_template('order_details.html',
                           api_urls=API_URLS,
                           payment_methods=PAYMENT_METHODS,
                           payment_statuses=PAYMENT_STATUSES,
                           data=session.get('order_data', DEFAULT_DATA),
                           products=session.get('products', []),
                           payments=session.get('payments', []))


@app.route('/payment-methods')
def payment_methods():
    return render_template('payment_methods.html',
                           api_urls=API_URLS,
                           payment_methods=PAYMENT_METHODS,
                           payment_statuses=PAYMENT_STATUSES,
                           payment_options=PAYMENT_OPTIONS,
                           data=session.get('order_data', DEFAULT_DATA),
                           payments=session.get('payments', []))


@app.route('/api-configuration')
def api_configuration():
    return render_template('api_configuration.html',
                           api_urls=API_URLS,
                           data=session.get('order_data', DEFAULT_DATA),
                           selected_endpoint=session.get('api_endpoint', DEFAULT_API_ENDPOINT))


@app.route('/database-connection')
def database_connection():
    return render_template('database_connection.html',
                           api_urls=API_URLS,
                           data=session.get('order_data', DEFAULT_DATA))


@app.route('/add-product', methods=['POST'])
def add_product():
    try:
        product = {
            "item_code": request.form.get('item_code'),
            "item_name": request.form.get('item_name'),
            "quantity": float(request.form.get('quantity', 0)),
            "unit_price": float(request.form.get('unit_price', 0)),
            "vat_percentage": float(request.form.get('vat_percentage', 0)),
            "row_total_discount": float(request.form.get('discount', 0)),
            "total_vat_amount": float(request.form.get('vat_percentage', 0)) * float(request.form.get('quantity', 0)) * float(
                request.form.get('unit_price', 0)) / 100,
            "row_net_total": (float(request.form.get('quantity', 0)) * float(request.form.get('unit_price', 0)) - float(
                request.form.get('discount', 0))) +
                             (float(request.form.get('vat_percentage', 0)) * float(request.form.get('quantity', 0)) * float(
                                 request.form.get('unit_price', 0)) / 100),
            "unit_vat_amount": 0.0,
            "offer_code": request.form.get('offer_code', ''),
            "offer_message": request.form.get('offer_message', '')
        }

        products = session.get('products', [])
        products.append(product)
        session['products'] = products
        session['saved_products'] = products  # Save for next session

        flash('Product added successfully!', 'success')
        return redirect(url_for('order_details'))

    except Exception as e:
        flash(f'Error adding product: {str(e)}', 'danger')
        return redirect(url_for('order_details'))


@app.route('/remove-product/<int:index>')
def remove_product(index):
    try:
        products = session.get('products', [])
        if 0 <= index < len(products):
            products.pop(index)
            session['products'] = products
            session['saved_products'] = products  # Save for next session
            flash('Product removed successfully!', 'success')
        else:
            flash('Invalid product index!', 'danger')

        return redirect(url_for('order_details'))

    except Exception as e:
        flash(f'Error removing product: {str(e)}', 'danger')
        return redirect(url_for('order_details'))


@app.route('/add-payment', methods=['POST'])
def add_payment():
    try:
        payment = {
            "payment_method": request.form.get('payment_method'),
            "payment_status": request.form.get('payment_status'),
            "payment_amount": float(request.form.get('payment_amount', 0)),
            "transaction_id": request.form.get('transaction_id'),
            "payment_option": request.form.get('payment_option'),
            "option_commission": float(request.form.get('option_commission', 0)),
            "card_name": request.form.get('card_name', ''),
            "bank_code": request.form.get('bank_code', ''),
            "credit_customer_info": {
                "customer_number": request.form.get('customer_number', ''),
                "customer_name": request.form.get('customer_name', '')
            } if request.form.get('payment_method') == 'PostToCredit' else None
        }

        payments = session.get('payments', [])
        payments.append(payment)
        session['payments'] = payments
        session['saved_payments'] = payments  # Save for next session

        # If payment status is done_payment, update order payment status
        if payment['payment_status'] == 'done_payment':
            order_data = session.get('order_data', DEFAULT_DATA.copy())
            order_data['order_payment_status'] = 'done_payment'
            session['order_data'] = order_data
            session['saved_order_data'] = order_data  # Save for next session

        flash('Payment method added successfully!', 'success')
        return redirect(url_for('payment_methods'))

    except Exception as e:
        flash(f'Error adding payment method: {str(e)}', 'danger')
        return redirect(url_for('payment_methods'))


@app.route('/remove-payment/<int:index>')
def remove_payment(index):
    try:
        payments = session.get('payments', [])
        if 0 <= index < len(payments):
            payments.pop(index)
            session['payments'] = payments
            session['saved_payments'] = payments  # Save for next session
            flash('Payment method removed successfully!', 'success')
        else:
            flash('Invalid payment method index!', 'danger')

        return redirect(url_for('payment_methods'))

    except Exception as e:
        flash(f'Error removing payment method: {str(e)}', 'danger')
        return redirect(url_for('payment_methods'))


@app.route('/update-order', methods=['POST'])
def update_order():
    try:
        order_data = session.get('order_data', DEFAULT_DATA.copy())

        # Update order information
        order_data['branch_code'] = request.form.get('branch_code', order_data['branch_code'])
        order_data['order_code'] = request.form.get('order_code', order_data['order_code'])
        order_data['order_delivery_cost'] = float(request.form.get('delivery_cost', order_data['order_delivery_cost']))
        order_data['is_delivery'] = int(request.form.get('is_delivery', order_data['is_delivery']))
        order_data['order_status'] = request.form.get('order_status', order_data['order_status'])
        order_data['order_payment_status'] = request.form.get('order_payment_status', order_data['order_payment_status'])

        # Update delivery information
        order_data['delivery_date'] = request.form.get('delivery_date', order_data['delivery_date'])
        order_data['delivery_from_time'] = request.form.get('delivery_from_time', order_data['delivery_from_time'])
        order_data['delivery_to_time'] = request.form.get('delivery_to_time', order_data['delivery_to_time'])
        order_data['shipping_address_2'] = request.form.get('shipping_address_2', order_data['shipping_address_2'])
        order_data['fullfilment_plant'] = request.form.get('fulfillment_plant', order_data['fullfilment_plant'])

        # Update client information
        order_data['client_first_name'] = request.form.get('first_name', order_data['client_first_name'])
        order_data['client_middle_name'] = request.form.get('middle_name', order_data['client_middle_name'])
        order_data['client_last_name'] = request.form.get('last_name', order_data['client_last_name'])
        order_data['client_phone'] = request.form.get('phone', order_data['client_phone'])
        order_data['client_email'] = request.form.get('email', order_data['client_email'])
        order_data['order_address'] = request.form.get('address', order_data['order_address'])
        order_data['client_birthdate'] = request.form.get('birthdate', order_data['client_birthdate'])
        order_data['client_gender'] = request.form.get('gender', order_data['client_gender'])

        session['order_data'] = order_data
        session['saved_order_data'] = order_data  # Save for next session

        flash('Order details updated successfully!', 'success')
        return redirect(url_for('order_details'))

    except Exception as e:
        flash(f'Error updating order: {str(e)}', 'danger')
        return redirect(url_for('order_details'))


@app.route('/calculate-totals')
def calculate_totals():
    try:
        products = session.get('products', [])
        order_data = session.get('order_data', DEFAULT_DATA.copy())

        order_product_total_value = sum(product.get('row_net_total', 0) for product in products)
        order_total_discount = sum(product.get('row_total_discount', 0) for product in products)
        delivery_cost = order_data.get('order_delivery_cost', 0)
        order_final_total_value = order_product_total_value + delivery_cost

        return jsonify({
            'products_total': round(order_product_total_value, 2),
            'order_discount': round(order_total_discount, 2),
            'delivery_cost': round(delivery_cost, 2),
            'final_total': round(order_final_total_value, 2)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/export-json')
def export_json():
    try:
        order_data = prepare_order_data()
        return jsonify(order_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/load-default')
def load_default():
    try:
        session['order_data'] = DEFAULT_DATA.copy()
        session['products'] = DEFAULT_DATA['order_products'].copy()
        session['payments'] = DEFAULT_DATA['payment_methods_with_options'].copy()

        # Clear saved data
        session.pop('saved_order_data', None)
        session.pop('saved_products', None)
        session.pop('saved_payments', None)

        flash('Default data loaded successfully!', 'success')
        return redirect(url_for('order_details'))

    except Exception as e:
        flash(f'Error loading default data: {str(e)}', 'danger')
        return redirect(url_for('order_details'))


@app.route('/clear-all')
def clear_all():
    try:
        session['order_data'] = {
            "branch_code": "",
            "order_code": "",
            "order_delivery_cost": 0,
            "is_delivery": 1,
            "order_status": "new",
            "order_payment_status": "not_payment",
            "delivery_date": datetime.now().strftime("%Y-%m-%d"),
            "delivery_from_time": "",
            "delivery_to_time": "",
            "shipping_address_2": "",
            "fullfilment_plant": "",
            "client_first_name": "",
            "client_middle_name": "",
            "client_last_name": "",
            "client_phone": "",
            "client_email": "",
            "client_birthdate": "1992-07-30T12:23:10.323Z",
            "client_gender": "Male",
            "order_address": ""
        }
        session['products'] = []
        session['payments'] = []

        # Clear saved data
        session.pop('saved_order_data', None)
        session.pop('saved_products', None)
        session.pop('saved_payments', None)

        flash('All data cleared successfully!', 'success')
        return redirect(url_for('order_details'))

    except Exception as e:
        flash(f'Error clearing data: {str(e)}', 'danger')
        return redirect(url_for('order_details'))


@app.route('/send-request', methods=['POST'])
def send_request():
    try:
        selected_endpoint = request.form.get('api_endpoint')
        custom_url = request.form.get('custom_url', '').strip()

        # Use custom URL if provided, otherwise use the selected endpoint
        if custom_url:
            url = custom_url
        elif selected_endpoint in API_URLS:
            url = API_URLS[selected_endpoint]
        else:
            flash('Please select a valid API endpoint or provide a custom URL', 'danger')
            return redirect(url_for('api_configuration'))

        # Save the selected endpoint for next time
        session['api_endpoint'] = selected_endpoint

        # Create the JSON data to send
        order_data = prepare_order_data()

        # Validate the data before sending
        validation_errors = validate_order_data(order_data)
        if validation_errors:
            flash('Validation errors found:', 'danger')
            for error in validation_errors:
                flash(error, 'danger')
            return redirect(url_for('api_configuration'))

        # Log the request data for debugging
        print("=== SENDING REQUEST DATA ===")
        print(json.dumps(order_data, indent=2))
        print("============================")

        # Send POST request
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, json=order_data, headers=headers, timeout=30)

        # Prepare response data
        response_data = {
            'status_code': response.status_code,
            'response_text': response.text,
            'url_sent': url
        }

        # Try to parse JSON response
        try:
            response_data['response_json'] = response.json()
        except:
            response_data['response_json'] = None

        # Handle different response statuses
        if response.status_code == 200:
            save_json_file(order_data)
            flash('Request sent successfully! Order created.', 'success')
        elif response.status_code == 400:
            # Try to extract detailed error information
            try:
                error_data = response.json()
                error_message = "Validation Error (400): "

                if 'errors' in error_data:
                    error_message += "Field validation errors detected. "
                    # Format field errors for display
                    for field, errors in error_data['errors'].items():
                        error_message += f"{field}: {', '.join(errors)}. "
                elif 'title' in error_data:
                    error_message += error_data['title']

                flash(error_message, 'warning')

            except:
                flash(f'Validation Error (400): {response.text}', 'warning')

        else:
            flash(f'Server returned status code: {response.status_code}', 'warning')

        return render_template('api_configuration.html',
                               api_urls=API_URLS,
                               data=session.get('order_data', DEFAULT_DATA),
                               selected_endpoint=selected_endpoint,
                               response=response_data)

    except requests.exceptions.RequestException as e:
        error_msg = f'Request Error: {str(e)}'
        if hasattr(e, 'response') and e.response is not None:
            error_msg += f' | Response: {e.response.text}'
        flash(error_msg, 'danger')
        return redirect(url_for('api_configuration'))
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'danger')
        return redirect(url_for('api_configuration'))


@app.route('/test-minimal-request')
def test_minimal_request():
    """Send a minimal request to test API connectivity"""
    minimal_data = {
        "branch_code": "2000",
        "order_code": f"TEST_{datetime.now().strftime('%H%M%S')}",
        "order_creation_date": datetime.now().isoformat() + 'Z',
        "order_notes": "Test order",
        "order_product_total_value": 10.0,
        "is_delivery": 0,
        "order_delivery_cost": 0.0,
        "order_total_discount": 0.0,
        "order_final_total_value": 10.0,
        "order_payment_method": "cash",
        "order_status": "new",
        "client_country_code": "966",
        "client_phone": "555123456",
        "client_first_name": "Test",
        "client_last_name": "User",
        "client_email": "test@example.com",
        "client_gender": "Male",
        "order_address": "Test Address",
        "order_payment_status": "done_payment",
        "order_gps": [21.779006345949554, 39.08578576461103],
        "order_products": [
            {
                "item_code": "TEST001",
                "item_name": "Test Product",
                "quantity": 1.0,
                "unit_price": 10.0,
                "unit_vat_amount": 0.0,
                "total_vat_amount": 0.0,
                "vat_percentage": 0.0,
                "offer_code": "",
                "offer_message": "",
                "row_total_discount": 0.0,
                "row_net_total": 10.0
            }
        ],
        "payment_methods_with_options": [
            {
                "payment_method": "cash",
                "payment_amount": 10.0,
                "transaction_id": "TEST123",
                "payment_option": "cash",
                "card_name": "",
                "bank_code": "",
                "option_commission": 0.0
            }
        ]
    }

    url = API_URLS.get("Whites Pharmacy - Testing")
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, json=minimal_data, headers=headers, timeout=10)
        return jsonify({
            'status_code': response.status_code,
            'response': response.text,
            'url': url,
            'request_data': minimal_data
        })
    except Exception as e:
        return jsonify({'error': str(e), 'url': url}), 500


@app.route('/get-item-details', methods=['GET'])
def get_item_details():
    try:
        material_number = request.args.get('material_number', type=str)
        if not material_number or not material_number.isdigit() or len(material_number) != 6:
            return jsonify({'error': 'Material number must be 6 digits'}), 400

        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500

        cursor = conn.cursor()

        query = r"""
        -- Input
        DECLARE @MaterialNumber VARCHAR(6) = ?;
        DECLARE @SapTaxCodeFilter VARCHAR(MAX) = '';
        DECLARE @FilterToDate DATETIME = GETDATE();
        DECLARE @DiscountFilterDate DATETIME = GETDATE();
        DECLARE @CustomerNumber VARCHAR(20) = '';
        DECLARE @SapMatGenericFilter VARCHAR(50) = '';

        -- Pad to 18 digits (12 zeros + 6 digits)
        DECLARE @PaddedMaterialNumber VARCHAR(18)
            = RIGHT(REPLICATE('0', 12) + @MaterialNumber, 18);

        ;WITH ValidDiscounts AS (
            SELECT *,
                   ROW_NUMBER() OVER (
                       PARTITION BY MaterialNumber, Customer
                       ORDER BY ValidFrom DESC
                   ) AS rn
            FROM RmsCashierSrv.dbo.sapMatWithCustDiscount_FltTbl
            WHERE @DiscountFilterDate BETWEEN ValidFrom AND ValidTo
                  AND CondPrice IS NOT NULL
                  AND (@CustomerNumber = '' OR Customer = @CustomerNumber)
        )
        SELECT
            I.Id AS ItemId,
            RIGHT(I.MaterialNumber, 6) AS MaterialNumber,
            IUOMB.UniversalBarCode AS ItemBarcode,
            I.Name AS EnglishName,
            I.NativeName AS ArabicName,
            I.SapMaterialType AS MaterialType,
            I.SapMatGeneric,
            I.SapTaxCode,
            IUM.IsBase AS IsBaseUnit,
            IP.Price AS UnitPrice,
            CAST(ROUND(((IP.Price * TT.Rate)/100) + IP.Price, 2) AS DECIMAL(10,2)) AS NetPrice,
            IUM.Numerator,
            IUM.Denominator,
            C.CustomerNumber,
            C.Name AS CustomerName,
            D.CondPrice,
            IP.FromDate AS ValidFrom,
            IP.ToDate AS ValidTo,
            TT.Rate AS VatRate
        FROM RmsCashierSrv.dbo.Items AS I
        LEFT JOIN RmsCashierSrv.dbo.TaxTypes AS TT 
            ON I.SapTaxCode = TT.Code
        INNER JOIN RmsCashierSrv.dbo.ItemUnitOfMeasures AS IUM 
            ON I.Id = IUM.ItemId
        INNER JOIN RmsCashierSrv.dbo.ItemUnitOfMeasureBarCodes AS IUOMB 
            ON IUM.Id = IUOMB.ItemUnitOfMeasureId
        LEFT JOIN RmsCashierSrv.dbo.ItemPrices AS IP 
            ON IUM.Id = IP.ItemUnitOfMeasureId
            AND IP.IsActive = 1
            AND IP.Price IS NOT NULL
            AND (@FilterToDate IS NULL OR IP.ToDate > @FilterToDate)
        LEFT JOIN (
            SELECT CustomerNumber, Name
            FROM RmsCashierSrv.dbo.Customers
            WHERE IsActive = 1 AND (@CustomerNumber = '' OR CustomerNumber = @CustomerNumber)
        ) AS C
            ON C.CustomerNumber = @CustomerNumber
        LEFT JOIN ValidDiscounts AS D 
            ON D.MaterialNumber = I.MaterialNumber
            AND D.Customer = C.CustomerNumber
            AND D.rn = 1
        WHERE
            I.MaterialNumber = @PaddedMaterialNumber
            AND (@SapTaxCodeFilter = '' OR I.SapTaxCode = @SapTaxCodeFilter)
            AND (@SapMatGenericFilter = '' OR I.SapMatGeneric = @SapMatGenericFilter)
            AND IP.Price IS NOT NULL
        ORDER BY I.Id DESC;
        """

        cursor.execute(query, material_number)
        row = cursor.fetchone()
        if not row:
            return jsonify({'error': 'No item found with this material number'}), 404

        item_details = {
            'item_code': row[1],
            'item_Barcode': row[2],
            'item_AR_Name': row[3],
            'item_EN_Name': row[4],  # barcode fallback, else English name
            'unit_price': float(row[9]),
            'vat_percentage': float(row[18]) if row[18] is not None else 0.0,  # TT.Rate
            'net_price': float(row[10]),
        }

        conn.close()
        return jsonify(item_details)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/update-product/<int:index>', methods=['GET', 'POST'])
def update_product(index):
    try:
        products = session.get('products', [])

        if request.method == 'GET':
            if 0 <= index < len(products):
                product = products[index]
                return jsonify(product)
            else:
                return jsonify({'error': 'Invalid product index'}), 404

        # POST request - update product
        product = {
            "item_code": request.form.get('item_code'),
            "item_name": request.form.get('item_name'),
            "quantity": float(request.form.get('quantity', 0)),
            "unit_price": float(request.form.get('unit_price', 0)),
            "vat_percentage": float(request.form.get('vat_percentage', 0)),
            "row_total_discount": float(request.form.get('discount', 0)),
            "total_vat_amount": float(request.form.get('vat_percentage', 0)) * float(request.form.get('quantity', 0)) * float(
                request.form.get('unit_price', 0)) / 100,
            "row_net_total": (float(request.form.get('quantity', 0)) * float(request.form.get('unit_price', 0)) - float(
                request.form.get('discount', 0))) +
                             (float(request.form.get('vat_percentage', 0)) * float(request.form.get('quantity', 0)) * float(
                                 request.form.get('unit_price', 0)) / 100),
            "unit_vat_amount": 0.0,
            "offer_code": request.form.get('offer_code', ''),
            "offer_message": request.form.get('offer_message', '')
        }

        if 0 <= index < len(products):
            products[index] = product
            session['products'] = products
            session['saved_products'] = products
            flash('Product updated successfully!', 'success')
            return redirect(url_for('order_details'))
        else:
            flash('Invalid product index!', 'danger')
            return redirect(url_for('order_details'))

    except Exception as e:
        flash(f'Error updating product: {str(e)}', 'danger')
        return redirect(url_for('order_details'))


@app.route('/update-payment/<int:index>', methods=['GET', 'POST'])
def update_payment(index):
    try:
        payments = session.get('payments', [])

        if request.method == 'GET':
            if 0 <= index < len(payments):
                payment = payments[index]
                return jsonify(payment)
            else:
                return jsonify({'error': 'Invalid payment index'}), 404

        # POST request - update payment
        payment = {
            "payment_method": request.form.get('payment_method'),
            "payment_status": request.form.get('payment_status'),
            "payment_amount": float(request.form.get('payment_amount', 0)),
            "transaction_id": request.form.get('transaction_id'),
            "payment_option": request.form.get('payment_option'),
            "option_commission": float(request.form.get('option_commission', 0)),
            "card_name": request.form.get('card_name', ''),
            "bank_code": request.form.get('bank_code', ''),
            "credit_customer_info": {
                "customer_number": request.form.get('customer_number', ''),
                "customer_name": request.form.get('customer_name', '')
            } if request.form.get('payment_method') == 'PostToCredit' else None
        }

        if 0 <= index < len(payments):
            payments[index] = payment
            session['payments'] = payments
            session['saved_payments'] = payments

            # If payment status is done_payment, update order payment status
            if payment['payment_status'] == 'done_payment':
                order_data = session.get('order_data', DEFAULT_DATA.copy())
                order_data['order_payment_status'] = 'done_payment'
                session['order_data'] = order_data
                session['saved_order_data'] = order_data

            flash('Payment method updated successfully!', 'success')
            return redirect(url_for('payment_methods'))
        else:
            flash('Invalid payment index!', 'danger')
            return redirect(url_for('payment_methods'))

    except Exception as e:
        flash(f'Error updating payment method: {str(e)}', 'danger')
        return redirect(url_for('payment_methods'))


def save_json_file(order_data):
    try:
        # Create JSON files directory if it doesn't exist
        if not os.path.exists('JSON files'):
            os.makedirs('JSON files')

        # Generate filename
        client_name = order_data.get('client_first_name', 'unknown') + '_' + order_data.get('client_last_name', 'client')
        payment_method = order_data.get('order_payment_method', 'unknown')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{client_name}_{payment_method}_{timestamp}.json"

        # Save the file with the new JSON structure
        filepath = os.path.join('JSON files', filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(order_data, f, indent=2, ensure_ascii=False)

        return True
    except Exception as e:
        print(f"Error saving JSON file: {str(e)}")
        return False


def prepare_order_data():
    order_data = session.get('order_data', DEFAULT_DATA.copy())
    products = session.get('products', [])
    payments = session.get('payments', [])

    # Calculate totals
    order_product_total_value = sum(product.get('row_net_total', 0) for product in products)
    order_total_discount = sum(product.get('row_total_discount', 0) for product in products)
    delivery_cost = order_data.get('order_delivery_cost', 0)
    order_final_total_value = order_product_total_value + delivery_cost

    # Format time values for API compatibility - ensure proper format
    delivery_from_time = order_data.get('delivery_from_time', '')
    delivery_to_time = order_data.get('delivery_to_time', '')

    # Convert time format to ensure it's in HH:MM:SS format
    if delivery_from_time:
        if len(delivery_from_time) == 5:  # HH:MM format
            delivery_from_time += ":00"
        elif '.' in delivery_from_time:  # HH:MM:SS.mmm format
            delivery_from_time = delivery_from_time.split('.')[0]  # Remove milliseconds

    if delivery_to_time:
        if len(delivery_to_time) == 5:  # HH:MM format
            delivery_to_time += ":00"
        elif '.' in delivery_to_time:  # HH:MM:SS.mmm format
            delivery_to_time = delivery_to_time.split('.')[0]  # Remove milliseconds

            # Remove None values


# Prepare final order data with the new structure
final_order_data = {
    "branch_code": order_data.get('branch_code', ''),
    "order_code": order_data.get('order_code', ''),
    "parent_order_code": order_data.get('parent_order_code', ''),
    "order_creation_date": datetime.now().isoformat() + 'Z',  # ISO format with Zulu time
    "order_notes": order_data.get('order_notes', "Don't Ring the bell"),
    "order_product_total_value": order_product_total_value,
    "is_delivery": order_data.get('is_delivery', 1),
    "order_delivery_cost": delivery_cost,
    "order_total_discount": order_total_discount,
    "order_final_total_value": order_final_total_value,
    "order_payment_method": ",".join([payment.get('payment_method', '') for payment in payments]),
    "order_status": order_data.get('order_status', 'new'),
    "client_country_code": order_data.get('client_country_code', '966'),
    "client_phone": order_data.get('client_phone', ''),
    "client_first_name": order_data.get('client_first_name', ''),
    "client_middle_name": order_data.get('client_middle_name', ''),
    "client_last_name": order_data.get('client_last_name', ''),
    "client_email": order_data.get('client_email', ''),
    "client_birthdate": order_data.get('client_birthdate', ''),
    "client_gender": order_data.get('client_gender', 'Male'),
    "order_address": order_data.get('order_address', ''),
    "address_code": order_data.get('address_code', ''),
    "order_country_code": order_data.get('order_country_code', ''),
    "order_phone": order_data.get('order_phone', ''),
    "order_payment_status": order_data.get('order_payment_status', 'not_payment'),
    "order_gps": order_data.get('order_gps', [21.779006345949554, 39.08578576461103]),
    "order_products": products,
    "payment_methods_with_options": payments,
    "delivery_date": order_data.get('delivery_date', ''),
    "delivery_from_time": delivery_from_time,
    "delivery_to_time": delivery_to_time,
    "shipping_address_2": order_data.get('shipping_address_2', ''),
    "fullfilment_plant": order_data.get('fullfilment_plant', '')
}

final_order_data = {k: v for k, v in final_order_data.items() if v is not None}

return final_order_data


def validate_order_data(order_data):
    """Validate order data before sending to API"""
    errors = []

    # Required fields validation
    required_fields = ['branch_code', 'order_code', 'client_phone', 'client_first_name',
                       'client_last_name', 'order_address']

    for field in required_fields:
        if not order_data.get(field):
            errors.append(f"Missing required field: {field}")

    # Products validation
    if not order_data.get('order_products'):
        errors.append("No products in the order")

    # Payment validation if order requires payment
    if order_data.get('order_final_total_value', 0) > 0 and not order_data.get('payment_methods_with_options'):
        errors.append("Order has value but no payment methods")

    return errors


@app.route('/test-endpoints')
def test_endpoints():
    results = {}
    for name, url in API_URLS.items():
        try:
            from urllib.parse import urlparse
            import socket

            parsed = urlparse(url)
            host = parsed.hostname
            port = parsed.port or (80 if parsed.scheme == 'http' else 443)

            # Test connection
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex((host, port))
            sock.close()

            results[name] = {
                'url': url,
                'status': 'Online' if result == 0 else 'Offline',
                'error_code': result if result != 0 else None
            }
        except Exception as e:
            results[name] = {
                'url': url,
                'status': 'Error',
                'error': str(e)
            }

    return render_template('test_endpoints.html', results=results)


@app.context_processor
def inject_global_variables():
    return dict(
        api_urls=API_URLS,
        payment_methods=PAYMENT_METHODS,
        payment_statuses=PAYMENT_STATUSES,
        payment_options=PAYMENT_OPTIONS
    )


@app.context_processor
def inject_session_data():
    return dict(
        data=session.get('order_data', DEFAULT_DATA),
        products=session.get('products', []),
        payments=session.get('payments', [])
    )


if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Changed to port 5001
