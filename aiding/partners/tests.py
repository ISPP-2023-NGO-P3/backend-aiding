from rest_framework.test import APITestCase
from .models import Partners,Donation
from rest_framework.renderers import JSONRenderer


class PartnerTests(APITestCase):

    ################################################## GETS ##################################################

    def test_list_positive_partners_status_OK(self):
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

    def test_show_negative_partners_status_NOT_FOUND(self):
        response = self.client.get('/partners/1')
        data = {"message": "partner not found..."}
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, data)

    ################################################## POSTS ##################################################

    def test_create_positive_partner_status_CREATED(self):
        data = JSONRenderer().render({"name":"Persona1","last_name": "Apellido1", "dni":"25604599X", "phone1":"999999997", "phone2":"888888877"
                        ,"birthdate":"2001-11-06", "sex":"men", "email":"persona1@gmail.com", "address":"Mi casa",
                        "postal_code":"41960", "township":"Gines", "province":"Sevilla", "language":"catalan",
                        "iban":"ES2114650100722030876288", "account_holder":"Persona1", "state":"Inactivo"}).decode("utf-8")
        response = self.client.post(
            '/partners/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)
    
    def test_create_negative_partner_status_CONFLICT(self):
        Partners.objects.create(name="Persona1",last_name= "Apellido1", dni="25604599X", phone1="999999997", phone2="888888877"
                ,birthdate="2001-11-06", sex="men", email="persona1@gmail.com", address="Mi casa",
                postal_code="41960", township="Gines", province="Sevilla", language="catalan",
                iban="ES2114650100722030876288", account_holder="Persona1", state="Inactivo")
        data = JSONRenderer().render({"name":"Persona1","last_name": "Apellido1", "dni":"25604599X", "phone1":"999999997", "phone2":"888888877"
                        ,"birthdate":"2001-11-06", "sex":"men", "email":"persona1@gmail.com", "address":"Mi casa",
                        "postal_code":"41960", "township":"Gines", "province":"Sevilla", "language":"catalan",
                        "iban":"ES2114650100722030876288", "account_holder":"Persona1", "state":"Inactivo"}).decode("utf-8")
        response = self.client.post(
            '/partners/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 409)
        dataMessage = {
            "error": "There is already a partner with a field equal to the one you are trying to add, please check the data."}
        self.assertEqual(response.data, dataMessage)

    def test_create_negative_partner_status_INCORRECT_IBAN(self):
        data = JSONRenderer().render({"name":"Persona1","last_name": "Apellido1", "dni":"25604599X", "phone1":"999999997", "phone2":"888888877"
                        ,"birthdate":"2001-11-06", "sex":"men", "email":"persona1@gmail.com", "address":"Mi casa",
                        "postal_code":"41960", "township":"Gines", "province":"Sevilla", "language":"catalan",
                        "iban":"IBANMALO", "account_holder":"Persona1", "state":"Inactivo"}).decode("utf-8")
        response = self.client.post(
            '/partners/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 409)
        dataMessage = {
            "error": "El IBAN no es valido."}
        self.assertEqual(response.data, dataMessage)
    
    def test_create_negative_partner_status_INCORRECT_DNI(self):
        data = JSONRenderer().render({"name":"Persona1","last_name": "Apellido1", "dni":"25604599O", "phone1":"999999997", "phone2":"888888877"
                        ,"birthdate":"2001-11-06", "sex":"men", "email":"persona1@gmail.com", "address":"Mi casa",
                        "postal_code":"41960", "township":"Gines", "province":"Sevilla", "language":"catalan",
                        "iban":"ES2114650100722030876288", "account_holder":"Persona1", "state":"Inactivo"}).decode("utf-8")
        response = self.client.post(
            '/partners/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 409)
        dataMessage = {
            "error": "La letra del DNI no es correcta"}
        self.assertEqual(response.data, dataMessage)

    def test_create_negative_partner_status_INCORRECT_DNI_2(self):
        data = JSONRenderer().render({"name":"Persona1","last_name": "Apellido1", "dni":"DNIMALO", "phone1":"999999997", "phone2":"888888877"
                        ,"birthdate":"2001-11-06", "sex":"men", "email":"persona1@gmail.com", "address":"Mi casa",
                        "postal_code":"41960", "township":"Gines", "province":"Sevilla", "language":"catalan",
                        "iban":"ES2114650100722030876288", "account_holder":"Persona1", "state":"Inactivo"}).decode("utf-8")
        response = self.client.post(
            '/partners/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 409)
        dataMessage = {
            "error": "El formato del DNI no es correcto"}
        self.assertEqual(response.data, dataMessage)

    def test_create_negative_partner_status_INCORRECT_BIRTHDATE(self):
        data = JSONRenderer().render({"name":"Persona1","last_name": "Apellido1", "dni":"25604599X", "phone1":"999999997", "phone2":"888888877"
                        ,"birthdate":"2022-11-06", "sex":"men", "email":"persona1@gmail.com", "address":"Mi casa",
                        "postal_code":"41960", "township":"Gines", "province":"Sevilla", "language":"catalan",
                        "iban":"ES2114650100722030876288", "account_holder":"Persona1", "state":"Inactivo"}).decode("utf-8")
        response = self.client.post(
            '/partners/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 409)
        dataMessage = {
            "error": "Debe ser mayor de edad."}
        self.assertEqual(response.data, dataMessage)

    ################################################## PUTS ##################################################

    def test_update_positive_partner_status_OK(self):
        partner = Partners.objects.create(name="Persona1",last_name= "Apellido1", dni="25604599X", phone1="999999997", phone2="888888877"
                ,birthdate="2001-11-06", sex="men", email="persona1@gmail.com", address="Mi casa",
                postal_code="41960", township="Gines", province="Sevilla", language="catalan",
                iban="ES2114650100722030876288", account_holder="Persona1", state="Inactivo")
        data = JSONRenderer().render(
            {"name":"PersonaTest","last_name": "Apellido1", "dni":"25604599X", "phone1":"999999997", "phone2":"888888877"
                        ,"birthdate":"2001-11-06", "sex":"men", "email":"persona1@gmail.com", "address":"Mi casa",
                        "postal_code":"41960", "township":"Gines", "province":"Sevilla", "language":"catalan",
                        "iban":"ES2114650100722030876288", "account_holder":"Persona1", "state":"Inactivo"}).decode("utf-8")
        response = self.client.put(
            f'/partners/{partner.id}', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)

    def test_update_negative_partner_status_NOT_FOUND(self):
        data = JSONRenderer().render({"name":"PersonaTest","last_name": "Apellido1", "dni":"25604599X", "phone1":"999999997", "phone2":"888888877"
                        ,"birthdate":"2001-11-06", "sex":"men", "email":"persona1@gmail.com", "address":"Mi casa",
                        "postal_code":"41960", "township":"Gines", "province":"Sevilla", "language":"catalan",
                        "iban":"ES2114650100722030876288", "account_holder":"Persona1", "state":"Inactivo"}).decode("utf-8")
        response = self.client.put(
            '/partners/1', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        dataMessage = {'message': 'Partner not found...'}
        self.assertEqual(response.data, dataMessage)

    def test_update_negative_partner_status_CONFLICT(self):
        Partners.objects.create(name="Persona1",last_name= "Apellido1", dni="25604599X", phone1="999999997", phone2="888888877"
                ,birthdate="2001-11-06", sex="men", email="persona1@gmail.com", address="Mi casa",
                postal_code="41960", township="Gines", province="Sevilla", language="catalan",
                iban="ES2114650100722030876288", account_holder="Persona1", state="Inactivo")
        partner = Partners.objects.create(name="Persona2",last_name= "Apellido2", dni="91184694K", phone1="999999996", phone2="888888876"
                ,birthdate="2001-11-06", sex="men", email="persona2@gmail.com", address="Mi casa",
                postal_code="41960", township="Gines", province="Sevilla", language="catalan",
                iban="ES2114650100722030876280", account_holder="Persona2", state="Inactivo")
        data = JSONRenderer().render(
            {"name":"Persona2","last_name": "Apellido2", "dni":"91184694K", "phone1":"999999997", "phone2":"888888876"
                        ,"birthdate":"2001-11-06", "sex":"men", "email":"persona2@gmail.com", "address":"Mi casa",
                        "postal_code":"41960", "township":"Gines", "province":"Sevilla", "language":"catalan",
                        "iban":"ES2114650100722030876280", "account_holder":"Persona2", "state":"Inactivo"}).decode("utf-8")
        response = self.client.put(
            f'/partners/{partner.id}', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 409)
        dataMessage = {
            "error": "There is already a partner with a field equal to the one you are trying to add, please check the data."}
        self.assertEqual(response.data, dataMessage)




class DonationTests(APITestCase):


    ################################################## GETS ##################################################

    def test_list_positive_partners_donations_OK(self):
        partner_test=Partners.objects.create(name="Persona1",last_name= "Apellido1", dni="25604599X", phone1="999999997", phone2="888888877"
                ,birthdate="2001-11-06", sex="men", email="persona1@gmail.com", address="Mi casa",
                postal_code="41960", township="Gines", province="Sevilla", language="catalan",
                iban="ES2114650100722030876288", account_holder="Persona1", state="Inactivo")
        Donation.objects.create(partner=partner_test,date= "2001-11-06", amount="200.0", periodicity="MENSUAL")
        
        response = self.client.get(f'/partners/{partner_test.id}/donation')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.content).__contains__("200.0"), True)
    
    def test_list_negative_donations_status_NOT_FOUND(self):
        partner_test=Partners.objects.create(name="Persona1",last_name= "Apellido1", dni="25604599X", phone1="999999997", phone2="888888877"
                ,birthdate="2001-11-06", sex="men", email="persona1@gmail.com", address="Mi casa",
                postal_code="41960", township="Gines", province="Sevilla", language="catalan",
                iban="ES2114650100722030876288", account_holder="Persona1", state="Inactivo")
        response = self.client.get(f'/partners/{partner_test.id}/donation')
        data = {"message": "donation not found..."}
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, data)
'''
    def test_show_positive_donations_status_OK(self):
        partner=Partners.objects.create(name="Persona1",last_name= "Apellido1", dni="25604599X", phone1="999999997", phone2="888888877"
                        ,birthdate="2001-11-06", sex="men", email="persona1@gmail.com", address="Mi casa",
                        postal_code="41960", township="Gines", province="Sevilla", language="catalan",
                        iban="ES2114650100722030876288", account_holder="Persona1", state="Inactivo")
        response = self.client.get(f'/partners/{partner.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Persona1")

    def test_show_negative_donations_status_NOT_FOUND(self):
        response = self.client.get('/partners/1')
        data = {"message": "partner not found..."}
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, data)
'''