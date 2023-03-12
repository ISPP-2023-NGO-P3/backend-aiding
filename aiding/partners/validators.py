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
    parsed_date = parse(date.strftime('%Y-%m-%d'))
    year = datetime.datetime.strptime(str(parsed_date), "%Y-%m-%d %H:%M:%S")
    age = datetime.datetime.now().year - year.year
    if age < 18:
        raise ValidationError("Debe ser mayor de edad.")