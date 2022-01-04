![logo](https://i.ibb.co/2KDC9tj/github-logo.png)

# Computer Security Final Project

![enter image description here](https://img.shields.io/badge/Uptime-100%25-blue) ![enter image description here](https://img.shields.io/badge/Version-Beta-green) ![enter image description here](https://img.shields.io/badge/Contributors-5-orange)

This project is a dummy telecommunication site that is vulnerable to SQL injection and XSS attacks. This was made to demonstrate the power of those attack vector. 

## How to install?

1. Clone the GitHub repository to your local machine

2. Install the required dependencies. Run the following: `pip install -r requirements.txt`

3. Install MySQL server that will host all the data.

4. In the code, go to the view.py and settings.py files and change the following sections to match your settings:

   ```python
   'NAME': 'computersecurity',
   'USER': 'root',
   'PASSWORD': 'root',
   ```

5. Migrate all the DBs `python manage.py makemigrations` and then `python manage.py migrate`

6. Run the server `python manage.py runserver`

7. Run the server with TLS `python manage.py runserver_plus --cert-file cert.pem --key-file key.pem`

8. If you try to reset your password and you dont see the mail please check your Trash mail




