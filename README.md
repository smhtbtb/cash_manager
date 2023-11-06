# Cash Management System

## Summary
The Cash Management System is a Django-based application with a RESTful API that allows users to manage their cash flow. Users can create and update transactions, track balances, and generate reports based on their financial activities. The application is designed to provide a convenient way for users to keep track of their income, expenses, and overall financial health.

## Endpoints

### User Authentication
- `POST /customer/register/`: Register a new user with a username and password.
Payload format is like:
```bash
{
    "username": "test",
    "password": "test-123",
    "email": "test@yahoo.com"
}
```
- `POST /customer/login/`: Authenticate and obtain a token for accessing protected endpoints.
Payload format is like:
```bash
{
    "username": "test",
    "password": "test-123"
}
```
- `POST /customer/logout/`: Log out the authenticated user.

### Transaction Management
- `GET /transaction/`: Retrieve a list of transactions.
- `POST /transaction/`: Create a new transaction.
- `GET /transaction/{transaction_id}/`: Retrieve details of a specific transaction.
- `PUT /transaction/{transaction_id}/`: Update a specific transaction.
- `DELETE /transaction/{transaction_id}/`: Delete a specific transaction.

### Balance Tracking
- `GET /transaction/get-balance/`: Calculate and retrieve the cumulative balance based on all transactions.

### Reports
- `GET /transaction/get-report/?report_type=monthly_summary`: Generate a monthly summary report.
- `GET /transaction/get-report/?report_type=category_summary`: Generate a report that categorizes expenses based on categories.

## Tests
Unit tests and integration tests have been written to ensure the reliability and correctness of the application. You can run the tests to validate the functionality of the components and endpoints.

To run the tests, use the following command in your project directory:

```bash
python manage.py test transaction/tests
```

## How to Run the Project

### Running Without Docker
1. Set up a Python environment with the required dependencies. You can use virtual environments for this purpose.
2. Install project dependencies using pip:
```bash
pip install -r requirements.txt
```
3. Apply database migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```
4. Start the development server:
```bash
python manage.py runserver
```
5. Access the application at http://localhost:8000.

### Running With Docker
1. Make sure you have Docker installed on your system.
2. Build the Docker image from the project directory (replace my-django-app with your desired image name):
```bash
docker build -t my-django-app .
```
3. Run a Docker container based on the image:
```bash
docker run -p 8000:8000 my-django-app
```
4. Access the application at http://localhost:8000.

#### 06/11/2023
