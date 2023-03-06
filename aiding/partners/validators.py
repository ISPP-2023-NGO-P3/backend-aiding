from django.forms import ValidationError

def validate_dni(dni):
    dni_letters = 'TRWAGMYFPDXBNJZSQVHLCKE'
    try:
        dni_number = int(dni[:-1])
        dni_letter = dni[-1].upper()
        if dni_letter != dni_letters[dni_number % 23]:
            raise ValidationError('La letra del DNI no es correcta')
    except ValueError:
        raise ValidationError('El formato del DNI no es correcto')
    
def validate_iban(value):
    value = value.replace(' ', '').replace('-', '').upper()
    if len(value) != 24 or not value[:2] == 'ES' or not value[2:].isdigit():
        raise ValidationError('The IBAN is not valid.')