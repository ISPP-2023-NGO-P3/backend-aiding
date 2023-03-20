from rest_framework.test import APITestCase
from .models import Partners
from rest_framework.renderers import JSONRenderer


class PartnerTests(APITestCase):

    ################################################## GETS ##################################################

    def test_list_positive_partners_status_OK(self):
        # Para probar que la respuesta HTTP de un código 200, se debe de crear previamente un socio
        Partners.objects.create(name="Persona1",last_name= "Apellido1", dni="25604599X", phone1="999999997", phone2="888888877"
                                ,birthdate="2001-11-06", sex="men", email="persona1@gmail.com", address="Mi casa",
                                postal_code="41960", township="Gines", province="Sevilla", language="catalan",
                                iban="ES2114650100722030876288", account_holder="Persona1", state="Inactivo")
        
        response = self.client.get('/partners/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_list_negative_partners_status_NOT_FOUND(self):
        response = self.client.get('/partners/')
        data = {"message": "partners not found..."}
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, data)

    def test_show_positive_partners_status_OK(self):
        partner=Partners.objects.create(name="Persona1",last_name= "Apellido1", dni="25604599X", phone1="999999997", phone2="888888877"
                        ,birthdate="2001-11-06", sex="men", email="persona1@gmail.com", address="Mi casa",
                        postal_code="41960", township="Gines", province="Sevilla", language="catalan",
                        iban="ES2114650100722030876288", account_holder="Persona1", state="Inactivo")
        response = self.client.get(f'/partners/{partner.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Persona1")

    def test_show_negative_section_status_NOT_FOUND(self):
        response = self.client.get('/partners/1')
        data = {"message": "partner not found..."}
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, data)