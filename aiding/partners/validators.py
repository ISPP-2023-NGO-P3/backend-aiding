import datetime
from django.forms import ValidationError
from dateutil.parser import parse

def validate_dni(dni):
    dni_letters = 'TRWAGMYFPDXBNJZSQVHLCKE'
    try:
        dni_number = int(dni[:-1])
        dni_letter = dni[-1].upper()
        if dni_letter != dni_letters[dni_number % 23]:
            raise ValidationError('La letra del DNI no es correcta')
    except ValueError:
        raise ValidationError('El formato del DNI no es correcto')
def validate_iban(iban):
    iban = iban.replace(' ', '').replace('-', '').upper()
    if len(iban) != 24 or not iban[:2] == 'ES' or not iban[2:].isdigit():
        raise ValidationError('El IBAN no es valido.')
def validate_date(date):
    date = str(date)
    parsed_date = parse(date).strftime('%Y-%m-%d')
    year = datetime.datetime.strptime(str(parsed_date), "%Y-%m-%d")
    age = datetime.datetime.now().year - year.year
    if age < 18:
        raise ValidationError("Debe ser mayor de edad.")

#Estos validadores están hechos porque el blank=false solo se valida cuando es un formulario y hace falta para
#la importación de socios

def validate_name(name):
    if len(name) <1:
        raise ValidationError('El nombre no puede estar vacío')

def validate_last_name(last_name):
    if len(last_name) <1:
        raise ValidationError('Los apellidos no puede estar vacíos')

def validate_dni_blank(dni):
    if len(dni) <1:
        raise ValidationError('El dni no puede estar vacío')

def validate_phone1(phone1):
    if len(phone1) <1:
        raise ValidationError('El teléfono no puede estar vacío')

def validate_birthdate(birthdate):
    if len(birthdate) <1:
        raise ValidationError('El cumpleaños no puede estar vacío')

def validate_address(address):
    if len(address) <1:
        raise ValidationError('La dirección no puede estar vacía')

def validate_postal_code(postal_code):
    if len(postal_code) <1:
        raise ValidationError('El código postal no puede estar vacío')

def validate_township(township):
    if len(township) <1:
        raise ValidationError('El municipio no puede estar vacío')

def validate_province(province):
    if len(province) <1:
        raise ValidationError('La provincia no puede estar vacía')

def validate_language(language):
    if len(language) <1:
        raise ValidationError('El idioma no puede estar vacío')
 
def validate_iban_blank(iban):
    if len(iban) <1:
        raise ValidationError('El iban no puede estar vacío')

def validate_account_holder(account_holder):
    if len(account_holder) <1:
        raise ValidationError('El titular de la cuenta no puede estar vacío')