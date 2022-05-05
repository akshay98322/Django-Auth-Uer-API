
# Django Authentication App

This app provides API for complete authentication (ie; sign up, log in, reset password, etc)

## Installation

Install Python 3.9.0

```bash
  pip install virtualenvwrapper-win==1.2.7
  mkvirtualenv <your_virtual_env_name>  
```
    
## Run Locally

Clone the project

```bash
  git clone https://github.com/akshay98322/Django-Auth-Uer-API
```

Go to the project directory

```bash
  cd Django-Auth-Uer-API
```

Rename .env-sample file to .env and add your email credentaials

Install dependencies

```bash
  pip install requirements.txt
```

Create DB and Tables

```bash
  python manage.py makemigrations
  python manage.py migrate
```

Start the server

```bash
  python manage.py runserver
```

