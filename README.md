You can find a hosted version of this app on :

https://shopifycrudchallenge.herokuapp.com/

For local execution:

1. Make sure to have all the dependencies installed like Python3, Flask, SQLAlchemy.
2. To make a test.db environment (if you dont already see one in your working dir), launch a python3 shell in the working directory and write the following.
   - from app import db
   - db.create_all()
     This will create a testdb instance
3. Now you're all set the run the application.
4. The instance of application runs on http://127.0.0.1:5000.
