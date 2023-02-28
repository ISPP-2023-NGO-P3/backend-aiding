# backend-aiding

## Configure the enviroment

Check your python version (3.10.7 recommended)
```
    $ python --version
```

Create a virtual enviroment
```
    $ python -m venv venv
```

You must activate your virtual enviroment in order to install dependencies. VScode detecs the venv located at root. If you are using windows you may need to allow unsigned script execution in powershell.
```
    $ (windows powershell)>> .\venv\Scripts\activate
    $ (windows cmd)>> .\venv\Scripts\activate.bat
    $ (linux)>> source venv/bin/activate
```

When you activate your venv, you can install project dependencies by using
```
    $ pip install -r requirements.txt
```

## Django useful commands

Setup database
```
    $ ./manage.py makemigrations
    $ ./manage.py migrate
```

Run development server
```
    $ ./manage.py runserver
```

Create super user
```
    $ ./manage.py createsuperuser
```