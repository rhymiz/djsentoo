from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from djsentoo.forms import WebhookForm
from djsentoo.models import Transaction
from djsentoo.signals import sentoo_transaction_status_changed
from djsentoo.wrapper import get_sentoo_client


@require_POST
@csrf_exempt
def sentoo_webhook(request: HttpRequest) -> JsonResponse:
    form = WebhookForm(request.POST)
    if not form.is_valid():
        return JsonResponse({"status": "invalid"}, status=400)

    transaction: Transaction = form.cleaned_data["transaction_id"]
    client = get_sentoo_client()
    response = client.transaction_status(transaction_id=transaction.transaction_id)
    if response.status_code == 200:
        data = response.json()
        status: str = data.get("success", {}).get("message", "pending")

        transaction.status = status
        transaction.save(update_fields=["status"])
        sentoo_transaction_status_changed.send(
            sender=None,
            transaction=transaction,
        )
        return JsonResponse({"status": "success"}, status=200)

    return JsonResponse({"status": "error"}, status=500)
