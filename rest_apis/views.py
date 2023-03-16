from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_apis.models import *
from .serializers import *
from django.utils import timezone
from datetime import datetime
from .tasks import calculate_credit_score


@api_view(['POST'])
def registerUser(request):
    try:
        # Adding User to db
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            calculate_credit_score.delay(user.id)
            serializer.save(credit_score=1000)
            return Response({"id": user.id})
        else:
            return Response({"error": serializer.errors})
    except Exception as exception:
        return Response({"error": str(exception)}, status=400)


@api_view(['POST'])
def applyLoan(request):
    try:
        # Validating Loan Type
        loan_type = request.data.get('loan_type')
        loan_types = ['Car', 'Home', 'Educational', 'Personal']
        if (loan_type not in loan_types):
            return Response({'error': "Invalid loan type"}, status=400)

        # Validating Loan Amount
        loan_amount = request.data.get('loan_amount')
        loan_type_max = {
            'Car': 750000, 'Home': 8500000, 'Educational': 5000000, 'Personal': 1000000
        }

        if (loan_type_max[loan_type] < loan_amount):
            return Response({'error': "Loan amount greater than allowed by type"}, status=400)

        # Validating User
        user_id = request.data.get('unique_user_id')
        user = User.objects.get(id=user_id)
        if user.credit_score < 450:
            return Response({'error': "Credit score below threshhold: 450"}, status=400)

        # Calculating and Validating EMI
        interest_rate = request.data.get('interest_rate')
        term_period = request.data.get('term_period')
        if (interest_rate < 14):
            return Response({'error': "Interest rate not high enough: 14%"}, status=400)

        emi_amount = loan_amount * interest_rate * \
            ((1 + interest_rate) ** term_period /
             ((1 + interest_rate)**term_period - 1))

        if (emi_amount > float(user.annual_income)*(0.6)):
            return Response({'error': "Monthly EMI exceeds 60% of income"}, status=400)
        total_interest = emi_amount*term_period
        if (total_interest <= 10000):
            return Response({'error': "Total interest earned is low"}, status=400)

        # Adding Loan to db
        loan = {}
        serializer = LoanSerializer(data=request.data)
        if serializer.is_valid():
            loan = serializer.save()
        else:
            return Response({"error": serializer.errors})

        # Creating EMIs and adding them

        emis_due = []
        date = loan.disbursement_date
        next_month = date.replace(day=1) + timezone.timedelta(days=32)
        for i in range(term_period):
            emis_due.append(EMI(
                loan_id=loan,
                due_amount=emi_amount,
                due_date=next_month.replace(month=((
                    next_month.month + i) % 12)+1, year=next_month.year + ((next_month.month + i - 1) // 12))
            ))
        EMI.objects.bulk_create(emis_due)

        # Returning response
        return Response({'loan_id': loan.id}, status=200)

    except Exception as exception:
        return Response({'error': str(exception)}, status=400)


@ api_view(['POST'])
def makePayment(request):
    try:
        loan_id = request.data.get('loan_id')
        emis_due = EMI.objects.filter(loan_id=loan_id).order_by('due_date')

        # Validating if loan is open
        if (len(emis_due) == 0):
            return Response({'error': "Loan is cleared, Payment rejected"}, status=400)

        # Validating if loan is overdue
        last_emi = emis_due[0]
        if (datetime.date(timezone.now()) > last_emi.due_date):
            return Response({'error': "Loan is overdue, Payment rejected"}, status=400)

        # Validating payment amount
        amount = request.data.get('amount')
        if (amount != last_emi.due_amount):
            return Response({'error': "Amount is incorrect, Payment rejected"}, status=400)

        # Adding payment to db
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            payment = serializer.save(date=datetime.date(timezone.now()))
            last_emi.delete()
            return Response({"id": payment.id}, status=200)
        else:
            return Response({"error": serializer.errors}, status=400)
    except Exception as exception:
        return Response({'error': str(exception)}, status=400)


@ api_view(['GET'])
def getStatement(request, loan_id):
    try:
        # Fetching past payments and upcoming emis
        past_payments = Payment.objects.filter(
            loan_id=loan_id)
        upcoming_emis = EMI.objects.filter(
            loan_id=loan_id).order_by('due_date')

        # Checking if loan is open
        if (len(upcoming_emis) == 0):
            return Response({"error": "Loan is closed"}, status=400)

        statement = {
            'past_transactions': PaymentSerializer(past_payments, many=True).data,
            'upcoming_transactions': EMISerializer(upcoming_emis, many=True).data
        }

        # sending statement
        return Response(statement, status=200)

    except Exception as exception:
        return Response({'error': str(exception)}, status=400)
