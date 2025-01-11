import requests
from django.conf import settings
from django.shortcuts import render, redirect
from .models import Payment

def initiate_payment(request):
    if request.method == 'POST':
        amount = request.POST['amount']
        transaction_id = 'unique_transaction_id'
        payload = {
            'appId': settings.TELEBIRR_APP_ID,
            'appKey': settings.TELEBIRR_APP_KEY,
            'nonce': 'unique_nonce',
            'notifyUrl': settings.TELEBIRR_NOTIFY_URL,
            'outTradeNo': transaction_id,
            'returnUrl': settings.TELEBIRR_RETURN_URL,
            'shortCode': 'your_short_code',
            'subject': 'Payment for Order',
            'totalAmount': amount,
        }
        response = requests.post('https://api.telebirr.com/payment', json=payload)
        if response.status_code == 200:
            Payment.objects.create(transaction_id=transaction_id, amount=amount, status='Pending')
            return redirect(response.json()['paymentUrl'])
    return render(request, 'initiate_payment.html')
from django.http import JsonResponse
from .models import Payment

def payment_notification(request):
    if request.method == 'POST':
        data = request.POST
        transaction_id = data['outTradeNo']
        status = data['status']
        payment = Payment.objects.get(transaction_id=transaction_id)
        payment.status = status
        payment.save()
        return JsonResponse({'message': 'Payment status updated'})
    return JsonResponse({'error': 'Invalid request'}, status=400)
