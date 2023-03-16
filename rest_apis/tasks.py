from celery import shared_task
from .models import TransactionRecord, User


@shared_task
def calculate_credit_score(user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return

    transactions = TransactionRecord.objects.filter(aadhar_id=user.aadhar_id)

    account_balance = 0
    for transaction in transactions:
        if transaction.transaction_type == 'CREDIT':
            account_balance += transaction.amount
        elif transaction.transaction_type == 'DEBIT':
            account_balance -= transaction.amount

    if account_balance >= 1000000:
        credit_score = 900
    elif account_balance <= 100000:
        credit_score = 300
    else:
        bonus = (account_balance - 100000) // 15000
        credit_score = 300 + (bonus * 10)

    user.credit_score = credit_score
    user.save()
