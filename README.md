# loan-app
Hello Everyone!
I have made this project as an assignment.

**API Documentation:**

-   POST /api/register-user/ to register a user and calculate their credit score.
-   POST /api/apply-loan/ to apply for a loan.
-   POST /api/make-payment/ to make a payment towards an EMI.
-   GET /api/get-statement/ to get statement of paid amounts and upcoming EMIs for a loan.


## How to run this project locally

To run this project on your local machine, follow these steps:

1.  Clone the repository and install dependencies with `$ pip3 install -r requirements.txt`
2.  Create migrations with `$ python manage.py makemigrations` and apply them with `$ python manage.py migrate`
3.  Install and configure Redis by running `$ sudo apt-get install redis-server` 
4.  Start the Django server with `$ python manage.py runserver`, the Celery worker with `$ celery -A loan_api_project worker -l info`, and Redis with `$ redis-server`
5.  Test the project by using the API endpoints to register users, apply for loans, and make payments.
