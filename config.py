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
