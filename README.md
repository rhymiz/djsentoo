# Django Sentoo (djsentoo)

[![PyPI version](https://badge.fury.io/py/djsentoo.svg)](https://badge.fury.io/py/djsentoo)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Django app for integrating with the Sentoo payment gateway.

## Overview

`djsentoo` is a Django reusable application that provides seamless integration with the Sentoo payment gateway service. This library simplifies the process of accepting payments, tracking transaction statuses, and handling webhook callbacks from the Sentoo payment platform.

## Features

- Simple API for creating payment transactions
- Automatic tracking of transaction status
- Webhook handling for payment status updates
- Support for multiple currencies
- QR code payment support
- Django admin integration

## Quick Start

### 1. Install the package

```bash
pip install djsentoo
```

### 2. Add to INSTALLED_APPS

```python
INSTALLED_APPS = [
    # ...
    'djsentoo',
    # ...
]
```

### 3. Configure settings

```python
# settings.py
SENTOO = {
    'SECRET': os.getenv('SENTOO_SECRET'),
    'MERCHANT_ID': os.getenv('SENTOO_MERCHANT_ID'),
    'SANDBOX': True,  # Set to False for production
    'DEFAULT_CURRENCY': 'USD',
}
```

### 4. Include URLs

```python
# urls.py
urlpatterns = [
    # ...
    path('sentoo/', include('djsentoo.urls', namespace='djsentoo')),
    # ...
]
```

### 5. Run migrations

```bash
python manage.py migrate djsentoo
```

## Basic Usage

### Creating a payment

```python
from djsentoo.service import SentooPaymentService

# Create a payment
service = SentooPaymentService()
response = service.create_payment(
    amount=5000,  # 50.00 in cents
    currency='USD',
    description='Payment for Order #12345',
    return_url='https://example.com/payment/return/',
    customer='customer@example.com'  # Optional
)

# Redirect to payment page
redirect(response.url)

# Or use QR code
qr_code_url = response.qr_code_url

# Store transaction ID for later reference
transaction_id = response.transaction_id
```

### Handling webhooks

```python
from django.dispatch import receiver
from djsentoo.signals import sentoo_transaction_status_changed
from djsentoo.models import TransactionStatusChoices

@receiver(sentoo_transaction_status_changed)
def handle_payment_update(sender, transaction, **kwargs):
    if transaction.status == TransactionStatusChoices.SUCCESS:
        # Handle successful payment
        order = Order.objects.get(payment_id=transaction.transaction_id)
        order.mark_as_paid()
        
    elif transaction.status == TransactionStatusChoices.FAILED:
        # Handle failed payment
        notify_customer_about_failed_payment(transaction)
```

## Documentation

For detailed documentation, see the [full documentation](link-to-your-docs).

## Support

If you encounter any issues or have questions, please [open an issue](link-to-issues) on GitHub.

## License

MIT License
