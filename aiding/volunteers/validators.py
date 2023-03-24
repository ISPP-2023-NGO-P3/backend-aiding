

from django.forms import ValidationError


def validate_nif(nif):
    nif_letters = 'TRWAGMYFPDXBNJZSQVHLCKE'
    try:
        nif_number = int(nif[:-1])
        nif_letter = nif[-1].upper()
        if nif_letter != nif_letters[nif_number % 23]:
            raise ValidationError('La letra del NIF no es correcta')
    except ValueError:
        raise ValidationError('El formato del NIF no es correcto')