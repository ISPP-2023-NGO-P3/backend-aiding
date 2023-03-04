from django.db import models

class Partners(models.Model):
    STATE_CHOICES = (
        ('ALTA', 'alta'),
        ('BAJA', 'baja'),
    )

    name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    dni = models.CharField(max_length=9, unique=True, blank=False)
    phone = models.CharField(max_length=15, unique=True, blank=False)
    email = models.EmailField(unique=True, blank=False)
    province = models.CharField(max_length=50, blank=False)
    iban = models.CharField(max_length=34, unique=True, blank=False)
    state = models.CharField(max_length=4, choices=STATE_CHOICES, default="alta")

    def clean(self):
        super().clean()
        dni_letters = 'TRWAGMYFPDXBNJZSQVHLCKE'
        dni_number = int(self.dni[:-1])
        dni_letter = self.dni[-1].upper()

        if dni_letter != dni_letters[dni_number % 23]:
            raise ValidationError("The entered DNI is not valid.")

        if self.email and "@gmail.com" not in self.email:
            raise ValidationError("The entered email is not valid.")

        if self.iban and not self._validate_iban(self.iban):
            raise ValidationError("The entered IBAN is not valid.")

    def _validate_iban(self, iban):
        iban = iban.upper().replace(' ', '').replace('-', '')
        if not iban.isalnum():
            return False
        if len(iban) != 24:
            return False
        if iban[:2] != 'ES':
            return False
        return True

    def __str__(self):
        return f"{self.name} {self.last_name}"
