from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255)
    email_id = models.EmailField(unique=True)
    aadhar_id = models.CharField(max_length=12, unique=True)
    annual_income = models.DecimalField(max_digits=12, decimal_places=2)
    credit_score = models.IntegerField(blank=True, null=True)


class TransactionRecord(models.Model):
    aadhar_id = models.CharField(max_length=12)
    date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=12)


class Loan(models.Model):
    unique_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    loan_type = models.CharField(max_length=12)
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.IntegerField()
    term_period = models.IntegerField()
    disbursement_date = models.DateField()


class EMI(models.Model):
    loan_id = models.ForeignKey(Loan, on_delete=models.CASCADE)
    due_amount = models.DecimalField(max_digits=12, decimal_places=2)
    due_date = models.DateField()


class Payment(models.Model):
    loan_id = models.ForeignKey(Loan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date: models.DateField()
