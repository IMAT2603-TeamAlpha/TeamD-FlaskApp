# TeamD-FlaskApp
Code for Team D's (car sales brief) website. Developed by Team C.

## Setting up the Flask webserver (including environment variables)

Open up Command prompt, and ensure that you have Python and pip installed. Then check that you are on no version lower than `3.8.6` for Python and `20.2.3` for pip - use `python --version` and `pip --version` to verify this.

Next, navigate to the web folder.

In the `web` folder, open command prompt and run the following commands:
1. `python -m venv venv` to setup the virtual environment.
2. `venv\Scripts\activate` to enter the virtual enviornment.
3. `pip install -r requirements.txt` to install the dependencies.

**If you have already setup your virtual environment, or see a `venv` folder, then you can skip the above three steps -- unless something broke in your virtual environment.**

After the requirements have been installed, you can now run the server:

4. `set FLASK_APP=run.py` set the Flask server application to the run.py script.
5. `set FLASK_DEBUG=1` to enable debug mode for the Flask server.
6. `flask run` to run the server.

You should now be able to visit the website on port 5000 (http://localhost:5000).

## Sign in credentials

Use these account credentials for developing/testing user specific functions (i.e. accounts).

Username: `test`

Password: `test`
