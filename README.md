![logo](https://i.ibb.co/2KDC9tj/github-logo.png)

# Computer Security Final Project

![enter image description here](https://img.shields.io/badge/Uptime-100%25-blue) ![enter image description here](https://img.shields.io/badge/Version-Beta-green) ![enter image description here](https://img.shields.io/badge/Contributors-5-orange)

This project is a dummy telecommunication site that is vulnerable to SQL injection and XSS attacks. This was made to demonstrate the power of those attack vector. 

## Versions

Our site has 2 versions:

### Vulnerable version V3.0

You can download it [HERE](https://github.com/Sagi313/computerSecurity/tree/v3.0)

### Safe version V3.1

You can download it [HERE](https://github.com/Sagi313/computerSecurity/tree/V3.1)

## How to run simple?

*********** NOA WILL UPDATE ***************

## How to install?

1. Clone the GitHub repository to your local machine (choose the tag you will to download)

2. Install the required dependencies. Run the following: `pip install -r requirements.txt`

3. Install MySQL server that will host all the data.

4. In the code, go to the view.py and settings.py files and change the following sections to match your settings:

   ```python
   'NAME': 'computersecurity',
   'USER': 'root',
   'PASSWORD': 'root',
   ```

5. Migrate all the DBs `python manage.py makemigrations` and then `python manage.py migrate`

6. Run the server: 
- Without TLS: `python manage.py runserver` and go to http://127.0.0.1:8000/
- With TLS: `python manage.py runserver_plus --cert-file cert.pem --key-file key.pem` and go to https://127.0.0.1:8000/

## Touble Shooting

- If you try to reset your password and you don't see an email please check your Spam inbox.
- After changing the pass.json conf file, you need to rerun the server inorder for the changes to apply.


## Vulenrable fields
### XSS
- http://127.0.0.1:8000/chat/ The 'message field'
- http://127.0.0.1:8000/ The 'Customer name' and 'Info' fields

### SQL injection
- http://127.0.0.1:8000/ and any other view, the vulnerable field is the 'Search' bar

## STRIDE Analysis

You can find all the vulnerabilites in the attached PDF file on the root dir

## Bonus tasks

**TLS protected**- The app can be used using TLS

**XSS Vulenrability**- We made the some fields vulnerable to the XSS attack vector

**DREAD analysis**- We analyzed each vulnerabily using this model in the PDF file

## Requirements

- Python3
- Pip3
- MySQL server






