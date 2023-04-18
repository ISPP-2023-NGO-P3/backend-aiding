from rest_framework.test import APITestCase
from .models import Partners,Donation,Communication
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APIClient
from base.models import User

class PartnerTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="ispp",
            password="ispp"
        )
        self.client.force_authenticate(user=self.user)
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
        self.assertEqual(response.status_code, 409)
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

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="ispp", 
            password="ispp"
        )
        self.client.force_authenticate(user=self.user)

    ################################################## GETS ##################################################

    def test_show_positive_partner_donation_status_OK(self):
        partner_test=Partners.objects.create(name="Persona1",last_name= "Apellido1", dni="25604599X", phone1="999999997", phone2="888888877"
                ,birthdate="2001-11-06", sex="men", email="persona1@gmail.com", address="Mi casa",
                postal_code="41960", township="Gines", province="Sevilla", language="catalan",
                iban="ES2114650100722030876288", account_holder="Persona1", state="Activo")
        Donation.objects.create(partner=partner_test,start_date= "2001-11-06", amount="200.0", periodicity="MENSUAL")
        
        response = self.client.get(f'/partners/{partner_test.id}/donation')

        self.assertEqual(response.status_code, 200)
    
    def test_list_positive_partners_donations_status_OK(self):
        partner_test=Partners.objects.create(name="Persona1",last_name= "Apellido1", dni="25604599X", phone1="999999997", phone2="888888877"
                ,birthdate="2001-11-06", sex="men", email="persona1@gmail.com", address="Mi casa",
                postal_code="41960", township="Gines", province="Sevilla", language="catalan",
                iban="ES2114650100722030876288", account_holder="Persona1", state="Activo")
        Donation.objects.create(partner=partner_test,start_date= "2001-11-06", amount="200.0", periodicity="MENSUAL")
        
        response = self.client.get('/partners/0/donation')

        self.assertEqual(response.status_code, 200)

    ################################################## POSTS ##################################################

    def test_create_positive_partner_donation_status_OK(self):
        partner_test=Partners.objects.create(name="Persona1",last_name= "Apellido1", dni="25604599X", phone1="999999997", phone2="888888877"
                ,birthdate="2001-11-06", sex="men", email="persona1@gmail.com", address="Mi casa",
                postal_code="41960", township="Gines", province="Sevilla", language="catalan",
                iban="ES2114650100722030876288", account_holder="Persona1", state="Activo")
        data = JSONRenderer().render({"partner_id":"1","start_date": "2001-11-06", "amount":"200.0", "periodicity":"MENSUAL",
                                       "year":"2020"}).decode("utf-8")
        response = self.client.post(
            f'/partners/{partner_test.id}/donation', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)
    
    def test_create_negative_partner_donation_status_NOT_FOUND(self):

        data = JSONRenderer().render({"partner_id":"1","start_date": "2001-11-06", "amount":"200.0", "periodicity":"MENSUAL",
                                       "year":"2020"}).decode("utf-8")
        response = self.client.post(
            '/partners/1/donation', data=data, content_type='application/json')
        
        self.assertEqual(response.status_code, 404)
        dataMessage = {'message': 'Partner not found or not active'}
        self.assertEqual(response.data, dataMessage)

    def test_create_negative_partner_donation_status_PARTNER_NOT_ACTIVE(self):
        partner_test=Partners.objects.create(name="Persona1",last_name= "Apellido1", dni="25604599X", phone1="999999997", phone2="888888877"
                ,birthdate="2001-11-06", sex="men", email="persona1@gmail.com", address="Mi casa",
                postal_code="41960", township="Gines", province="Sevilla", language="catalan",
                iban="ES2114650100722030876288", account_holder="Persona1", state="Inactivo")
        
        data = JSONRenderer().render({"partner_id":"1","start_date": "2001-11-06", "amount":"200.0", "periodicity":"MENSUAL",
                                       "year":"2020"}).decode("utf-8")
        response = self.client.post(
            f'/partners/{partner_test.id}/donation', data=data, content_type='application/json')
        
        self.assertEqual(response.status_code, 404)
        dataMessage = {'message': 'Partner not found or not active'}
        self.assertEqual(response.data, dataMessage)

    ################################################## DELETES ##################################################
    
    def test_delete_positive_partner_donation_status_OK(self):
        partner_test=Partners.objects.create(name="Persona1",last_name= "Apellido1", dni="25604599X", phone1="999999997", phone2="888888877"
                ,birthdate="2001-11-06", sex="men", email="persona1@gmail.com", address="Mi casa",
                postal_code="41960", township="Gines", province="Sevilla", language="catalan",
                iban="ES2114650100722030876288", account_holder="Persona1", state="Activo")
        Donation.objects.create(partner=partner_test,start_date= "2001-11-06", amount="200.0", periodicity="MENSUAL")

        response=self.client.delete(f'/partners/{partner_test.id}/donation', content_type='application/json')

        self.assertEqual(response.status_code, 200)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)

    def test_delete_negative_partner_donation_status_NOT_FOUND(self):
        partner_test=Partners.objects.create(name="Persona1",last_name= "Apellido1", dni="25604599X", phone1="999999997", phone2="888888877"
                ,birthdate="2001-11-06", sex="men", email="persona1@gmail.com", address="Mi casa",
                postal_code="41960", township="Gines", province="Sevilla", language="catalan",
                iban="ES2114650100722030876288", account_holder="Persona1", state="Activo")

        response=self.client.delete(f'/partners/{partner_test.id}/donation', content_type='application/json')

        self.assertEqual(response.status_code, 404)
        dataMessage = {'message': 'Donation not found...'}
        self.assertEqual(response.data, dataMessage)

    ################################################## PUTS ##################################################
    def test_update_positive_partner_donation_status_OK(self):
        partner_test = Partners.objects.create(name="Persona1",last_name= "Apellido1", dni="25604599X", phone1="999999997", phone2="888888877"
                ,birthdate="2001-11-06", sex="men", email="persona1@gmail.com", address="Mi casa",
                postal_code="41960", township="Gines", province="Sevilla", language="catalan",
                iban="ES2114650100722030876288", account_holder="Persona1", state="Activo")
        Donation.objects.create(partner=partner_test,start_date= "2001-11-06", amount="200.0", periodicity="MENSUAL")

        data = JSONRenderer().render({"partner_id":"1","start_date": "2001-11-06", "amount":"200.0", "periodicity":"MENSUAL",
                                       "year":"2021"}).decode("utf-8")
        response = self.client.put(
            f'/partners/{partner_test.id}/donation', data=data, content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)

    def test_update_negative_partner_donation_status_PARTNER_NOT_FOUND(self):
        partner_test = Partners.objects.create(name="Persona1",last_name= "Apellido1", dni="25604599X", phone1="999999997", phone2="888888877"
                ,birthdate="2001-11-06", sex="men", email="persona1@gmail.com", address="Mi casa",
                postal_code="41960", township="Gines", province="Sevilla", language="catalan",
                iban="ES2114650100722030876288", account_holder="Persona1", state="Inactivo")
        Donation.objects.create(partner=partner_test,start_date= "2001-11-06", amount="200.0", periodicity="MENSUAL")

        data = JSONRenderer().render({"partner_id":"1","start_date": "2001-11-06", "amount":"200.0", "periodicity":"MENSUAL",
                                       "year":"2021"}).decode("utf-8")
        response = self.client.put(
            f'/partners/{partner_test.id}/donation', data=data, content_type='application/json')
        
        self.assertEqual(response.status_code, 404)
        dataMessage = {'message': 'Partner not found or not active'}
        self.assertEqual(response.data, dataMessage)

    def test_update_negative_partner_donation_status_DONATION_NOT_FOUND(self):
        partner_test = Partners.objects.create(name="Persona1",last_name= "Apellido1", dni="25604599X", phone1="999999997", phone2="888888877"
                ,birthdate="2001-11-06", sex="men", email="persona1@gmail.com", address="Mi casa",
                postal_code="41960", township="Gines", province="Sevilla", language="catalan",
                iban="ES2114650100722030876288", account_holder="Persona1", state="Activo")

        data = JSONRenderer().render({"partner_id":"1","start_date": "2001-11-06", "amount":"200.0", "periodicity":"MENSUAL",
                                       "year":"2021"}).decode("utf-8")
        response = self.client.put(
            f'/partners/{partner_test.id}/donation', data=data, content_type='application/json')
        
        self.assertEqual(response.status_code, 404)
        dataMessage = {'message': 'Donation not found...'}
        self.assertEqual(response.data, dataMessage)

class CommunicationTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="ispp", 
            password="ispp"
        )
        self.client.force_authenticate(user=self.user)

    ################################################## GETS ##################################################

    def test_list_positive_partners_communications_status_OK(self):
        partner_test=Partners.objects.create(name="Persona1",last_name= "Apellido1", dni="25604599X", phone1="999999997", phone2="888888877"
                ,birthdate="2001-11-06", sex="men", email="persona1@gmail.com", address="Mi casa",
                postal_code="41960", township="Gines", province="Sevilla", language="catalan",
                iban="ES2114650100722030876288", account_holder="Persona1", state="Activo")
        comunication_test=Communication.objects.create(partner=partner_test,date= "2001-11-06", communication_type="EMAIL", description="Comunicacion de pruebas")
        
        response = self.client.get(f'/partners/0/communication/{comunication_test.id}')

        self.assertEqual(response.status_code, 200)

    def test_show_positive_partner_communication_status_OK(self):
        partner_test=Partners.objects.create(name="Persona1",last_name= "Apellido1", dni="25604599X", phone1="999999997", phone2="888888877"
                ,birthdate="2001-11-06", sex="men", email="persona1@gmail.com", address="Mi casa",
                postal_code="41960", township="Gines", province="Sevilla", language="catalan",
                iban="ES2114650100722030876288", account_holder="Persona1", state="Activo")
        comunication_test=Communication.objects.create(partner=partner_test,date= "2001-11-06", communication_type="EMAIL", description="Comunicacion de pruebas")

        response = self.client.get(f'/partners/{partner_test.id}/communication/{comunication_test.id}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_list_positive_partner_communications_status_OK(self):
        partner_test=Partners.objects.create(name="Persona1",last_name= "Apellido1", dni="25604599X", phone1="999999997", phone2="888888877"
                ,birthdate="2001-11-06", sex="men", email="persona1@gmail.com", address="Mi casa",
                postal_code="41960", township="Gines", province="Sevilla", language="catalan",
                iban="ES2114650100722030876288", account_holder="Persona1", state="Activo")

        response = self.client.get(f'/partners/{partner_test.id}/communication/0')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    ################################################## POSTS ##################################################
    
    def test_create_positive_partner_communication_status_OK(self):
        partner_test=Partners.objects.create(name="Persona1",last_name= "Apellido1", dni="25604599X", phone1="999999997", phone2="888888877"
                ,birthdate="2001-11-06", sex="men", email="persona1@gmail.com", address="Mi casa",
                postal_code="41960", township="Gines", province="Sevilla", language="catalan",
                iban="ES2114650100722030876288", account_holder="Persona1", state="Activo")
        
        data = JSONRenderer().render({"partner_id":"1","date": "2001-11-06", "communication_type":"EMAIL", "description":"Comunicacion de pruebas"}).decode("utf-8")
        response = self.client.post(
            f'/partners/{partner_test.id}/communication/', data=data, content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)

    def test_create_negative_partner_communication_status_NOT_FOUND(self):
        data = JSONRenderer().render({"partner_id":"1","date": "2001-11-06", "communication_type":"EMAIL", "description":"Comunicacion de pruebas"}).decode("utf-8")
        response = self.client.post(
            '/partners/1/communication/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        dataMessage = {'message': 'Partner not found'}
        self.assertEqual(response.data, dataMessage)

    ################################################## PUTS ##################################################
    def test_update_positive_partner_communication_status_OK(self):
        partner_test = Partners.objects.create(name="Persona1",last_name= "Apellido1", dni="25604599X", phone1="999999997", phone2="888888877"
                ,birthdate="2001-11-06", sex="men", email="persona1@gmail.com", address="Mi casa",
                postal_code="41960", township="Gines", province="Sevilla", language="catalan",
                iban="ES2114650100722030876288", account_holder="Persona1", state="Activo")
        comunication_test=Communication.objects.create(partner=partner_test,date= "2001-11-06", communication_type="EMAIL", description="Comunicacion de pruebas")

        data = JSONRenderer().render({"partner_id":"1","date": "2001-11-06", "communication_type":"EMAIL", "description":"Comunicacion de pruebas"}).decode("utf-8")
        response = self.client.put(f'/partners/{partner_test.id}/communication/{comunication_test.id}', data=data, content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)

    def test_update_negative_partner_communication_status_PARTNER_NOT_FOUND(self):
        partner_test = Partners.objects.create(name="Persona1",last_name= "Apellido1", dni="25604599X", phone1="999999997", phone2="888888877"
                ,birthdate="2001-11-06", sex="men", email="persona1@gmail.com", address="Mi casa",
                postal_code="41960", township="Gines", province="Sevilla", language="catalan",
                iban="ES2114650100722030876288", account_holder="Persona1", state="Activo")
        comunication_test=Communication.objects.create(partner=partner_test,date= "2001-11-06", communication_type="EMAIL", description="Comunicacion de pruebas")
        
        data = JSONRenderer().render({"partner_id":"1","date": "2001-11-06", "communication_type":"EMAIL", "description":"Comunicacion de pruebas"}).decode("utf-8")
        response = self.client.put(f'/partners/3/communication/{comunication_test.id}', data=data, content_type='application/json')
        
        self.assertEqual(response.status_code, 404)
        dataMessage = {'message': 'Partner not found...'}
        self.assertEqual(response.data, dataMessage)

    def test_update_negative_partner_communication_status_DONATION_NOT_FOUND(self):
        partner_test = Partners.objects.create(name="Persona1",last_name= "Apellido1", dni="25604599X", phone1="999999997", phone2="888888877"
                ,birthdate="2001-11-06", sex="men", email="persona1@gmail.com", address="Mi casa",
                postal_code="41960", township="Gines", province="Sevilla", language="catalan",
                iban="ES2114650100722030876288", account_holder="Persona1", state="Activo")

        data = JSONRenderer().render({"partner_id":"1","date": "2001-11-06", "communication_type":"EMAIL", "description":"Comunicacion de pruebas"}).decode("utf-8")
        response = self.client.put(f'/partners/{partner_test.id}/communication/2', data=data, content_type='application/json')
 
        
        self.assertEqual(response.status_code, 404)
        dataMessage = {'message': 'Communication not found...'}
        self.assertEqual(response.data, dataMessage)


class IntegrationTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="ispp", 
            password="ispp"
        )
        self.client.force_authenticate(user=self.user)

    def test_positive_create_partner_donation_and_communications(self):
        #Se crea un socio
        partner_data = JSONRenderer().render({"name":"Persona1","last_name": "Apellido1", "dni":"25604599X", "phone1":"999999997", "phone2":"888888877"
                        ,"birthdate":"2001-11-06", "sex":"men", "email":"persona1@gmail.com", "address":"Mi casa",
                        "postal_code":"41960", "township":"Gines", "province":"Sevilla", "language":"catalan",
                        "iban":"ES2114650100722030876288", "account_holder":"Persona1", "state":"Activo"}).decode("utf-8")
        response = self.client.post(
            '/partners/', data=partner_data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)
        
        partner_test=Partners.objects.get(name="Persona1")
        
        #Se crea una donacion
        donation_data = JSONRenderer().render({"partner_id":"1","start_date": "2001-11-06", "amount":"200.0", "periodicity":"MENSUAL",
                                       "year":"2020"}).decode("utf-8")
        response = self.client.post(
            f'/partners/{partner_test.id}/donation', data=donation_data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)

        #Se crea una comunicacion

        communication_data = JSONRenderer().render({"partner_id":"1","date": "2001-11-06", "communication_type":"EMAIL", "description":"Comunicacion de pruebas"}).decode("utf-8")
        response = self.client.post(
            f'/partners/{partner_test.id}/communication/', data=communication_data, content_type='application/json')
        
        communication_test1=Communication.objects.get(description="Comunicacion de pruebas")

        self.assertEqual(response.status_code, 200)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)

        #Se crea una segunda comunicacion

        communication_data = JSONRenderer().render({"partner_id":"1","date": "2001-11-07", "communication_type":"EMAIL", "description":"Comunicacion de pruebas 2"}).decode("utf-8")
        response = self.client.post(
            f'/partners/{partner_test.id}/communication/', data=communication_data, content_type='application/json')
        
        communication_test2=Communication.objects.get(description="Comunicacion de pruebas 2")

        self.assertEqual(response.status_code, 200)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)

        #Se muestra la primera comunicacion
        response = self.client.get(f'/partners/{partner_test.id}/communication/{communication_test1.id}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        #Se muestra la segunda comunicacion
        response = self.client.get(f'/partners/{partner_test.id}/communication/{communication_test2.id}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        #Se muestra las dos comunicaciones
        response = self.client.get(f'/partners/{partner_test.id}/communication/0')
        
        self.assertEqual(response.status_code, 200)
        dataMessage = {'message': 'Success'}
        self.assertEqual(len(response.data), 2)

    def test_positive_update_partner_with_donation_and_communication(self):
        partner_test=Partners.objects.create(name="Persona1",last_name= "Apellido1", dni="25604599X", phone1="999999997", phone2="888888877"
                                ,birthdate="2001-11-06", sex="men", email="persona1@gmail.com", address="Mi casa",
                                postal_code="41960", township="Gines", province="Sevilla", language="catalan",
                                iban="ES2114650100722030876288", account_holder="Persona1", state="Inactivo")

        partner_data = JSONRenderer().render(
            {"name":"PersonaTest","last_name": "Apellido1", "dni":"25604599X", "phone1":"999999997", "phone2":"888888877"
                        ,"birthdate":"2001-11-06", "sex":"men", "email":"persona1@gmail.com", "address":"Mi casa",
                        "postal_code":"41960", "township":"Gines", "province":"Sevilla", "language":"catalan",
                        "iban":"ES2114650100722030876288", "account_holder":"Persona1", "state":"Activo"}).decode("utf-8")

        response = self.client.put(
            f'/partners/{partner_test.id}', data=partner_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)
    '''
    def test_negative_show_communication_of_other_partner(self):
        partner_test1=Partners.objects.create(name="Persona1",last_name= "Apellido1", dni="25604599X", phone1="999999997", phone2="888888877"
                                ,birthdate="2001-11-06", sex="men", email="persona1@gmail.com", address="Mi casa",
                                postal_code="41960", township="Gines", province="Sevilla", language="catalan",
                                iban="ES2114650100722030876288", account_holder="Persona1", state="Activo")
        
        partner_test2=Partners.objects.create(name="Persona2",last_name= "Apellido2", dni="38608033A", phone1="999999979", phone2="888888000"
                                ,birthdate="2001-11-06", sex="men", email="persona2@gmail.com", address="Mi casa",
                                postal_code="41960", township="Gines", province="Sevilla", language="catalan",
                                iban="ES5420801587748635250719", account_holder="Persona2", state="Activo")
        
        comunication_test1=Communication.objects.create(partner=partner_test1,date= "2001-11-06", communication_type="EMAIL", description="Comunicacion de pruebas")
        comunication_test2=Communication.objects.create(partner=partner_test2,date= "2001-11-06", communication_type="EMAIL", description="Comunicacion de pruebas")

        response = self.client.get(f'/partners/{partner_test1.id}/communication/{comunication_test2.id}')

        self.assertEqual(response.status_code, 404)
        dataMessage = {'message': 'Communication not found...'}
        self.assertEqual(response.data, dataMessage)

        response = self.client.get(f'/partners/{partner_test2.id}/communication/{comunication_test1.id}')
        self.assertEqual(response.status_code, 404)
        dataMessage = {'message': 'Communication not found...'}
        self.assertEqual(response.data, dataMessage)
    '''