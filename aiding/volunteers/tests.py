from django.test import TestCase
from rest_framework.test import APITestCase
from .models import Volunteer, Turn, VolunteerTurn
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APIClient
from base.models import User
import json
import datetime

class VolunteerTests(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="ispp", 
            password="ispp"
        )
        self.client.force_authenticate(user=self.user)

    ################################################## GETS ##################################################

    def test_list_positive_volunteers_status_OK(self):
        # Para probar que la respuesta HTTP de un código 200, se debe de crear previamente un voluntario
        Volunteer.objects.create(name="Persona1",last_name= "Apellido1", num_volunteer="999999997", nif="25604599X", place="Sevilla", 
                                 phone="888888877" ,email="persona1@gmail.com", state="Activo", situation = "necesitaFormacion",
                                rol="Voluntario", observations="Persona1 es voluntario", computerKnowledge = True,
                                truckKnowledge=False, warehouseKnowledge="True",otherKnowledge="Limpieza")
        
        response = self.client.get('/volunteers/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_list_negative_volunteers_status_NOT_FOUND(self):
        response = self.client.get('/volunteers/')
        data = {"message": "Volunteers not found..."}
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, data)

    def test_show_positive_volunteers_status_OK(self):
        volunteer=Volunteer.objects.create(name="Persona1",last_name= "Apellido1", num_volunteer="999", nif="25604599X", place="Sevilla", 
                                 phone="888888877" ,email="persona1@gmail.com", state="Activo", situation = "necesitaFormacion",
                                rol="Voluntario", observations="Persona1 es voluntario", computerKnowledge = True,
                                truckKnowledge=False, warehouseKnowledge="True",otherKnowledge="Limpieza")
        response = self.client.get(f'/volunteers/{volunteer.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Persona1")

    def test_show_negative_volunteers_status_NOT_FOUND(self):
        response = self.client.get('/volunteers/1')
        data = {"message": "Volunteer not found..."}
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, data)

    ################################################## POSTS ##################################################

    def test_create_positive_volunteer_status_CREATED(self):
        data = JSONRenderer().render({"name":"Persona1","last_name": "Apellido1", "num_volunteer":"999", "nif":"25604599X", "place":"Sevilla", 
                                 "phone":"888888877" ,"email":"persona1@gmail.com", "state":"Activo", "situation":"necesitaFormacion",
                                "rol":"Voluntario", "observations":"Persona1 es voluntario", "computerKnowledge" :"True",
                                "truckKnowledge":"False", "warehouseKnowledge":"True","otherKnowledge":"Limpieza"}).decode("utf-8")
        response = self.client.post(
            '/volunteers/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)

    def test_create_negative_volunteer_status_CONFLICT(self):
        Volunteer.objects.create(name="Persona1",last_name= "Apellido1", num_volunteer="999", nif="25604599X", place="Sevilla", 
                                 phone="888888877" ,email="persona1@gmail.com", state="Activo", situation = "necesitaFormacion",
                                rol="Voluntario", observations="Persona1 es voluntario", computerKnowledge = True,
                                truckKnowledge=False, warehouseKnowledge="True",otherKnowledge="Limpieza")
        data = JSONRenderer().render({"name":"Persona1","last_name": "Apellido1", "num_volunteer":"999", "nif":"25604599X", "place":"Sevilla", 
                                 "phone":"888888877" ,"email":"persona1@gmail.com", "state":"Activo", "situation":"necesitaFormacion",
                                "rol":"Voluntario", "observations":"Persona1 es voluntario", "computerKnowledge" :"True",
                                "truckKnowledge":"False", "warehouseKnowledge":"True","otherKnowledge":"Limpieza"}).decode("utf-8")
        response = self.client.post(
            '/volunteers/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 409)
        dataMessage = {
            "error": "There is already a volunteer with a field equal to the one you are trying to add, please check the data."}
        self.assertEqual(response.data, dataMessage)

    
    def test_create_negative_volunteer_validate_DNI_incorrect_letter(self):
        data = JSONRenderer().render({"name":"Persona1","last_name": "Apellido1", "num_volunteer":"999", "nif":"25604599L", "place":"Sevilla", 
                                 "phone":"888888877" ,"email":"persona1@gmail.com", "state":"Activo", "situation":"necesitaFormacion",
                                "rol":"Voluntario", "observations":"Persona1 es voluntario", "computerKnowledge" :"True",
                                "truckKnowledge":"False", "warehouseKnowledge":"True","otherKnowledge":"Limpieza"}).decode("utf-8")
        response = self.client.post(
            '/volunteers/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 409)
        data = {"error": "La letra del NIF no es correcta"}
        self.assertEqual(response.data, data)

    def test_create_negative_volunteer_validate_DNI_incorrect_format(self):
        data = JSONRenderer().render({"name":"Persona1","last_name": "Apellido1", "num_volunteer":"999", "nif":"2", "place":"Sevilla", 
                                 "phone":"888888877" ,"email":"persona1@gmail.com", "state":"Activo", "situation":"necesitaFormacion",
                                "rol":"Voluntario", "observations":"Persona1 es voluntario", "computerKnowledge" :"True",
                                "truckKnowledge":"False", "warehouseKnowledge":"True","otherKnowledge":"Limpieza"}).decode("utf-8")
        response = self.client.post(
            '/volunteers/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 409)
        data = {"error": "El formato del NIF no es correcto"}
        self.assertEqual(response.data, data)

 ################################################## PUTS ##################################################

    def test_update_positive_volunteer_status_OK(self):
        volunteer = Volunteer.objects.create(name="Persona1",last_name= "Apellido1", num_volunteer="999", nif="25604599X", place="Sevilla", 
                                 phone="888888877" ,email="persona1@gmail.com", state="Activo", situation = "necesitaFormacion",
                                rol="Voluntario", observations="Persona1 es voluntario", computerKnowledge = True,
                                truckKnowledge=False, warehouseKnowledge="True",otherKnowledge="Limpieza")
        data = JSONRenderer().render({"name":"Persona2","last_name": "Apellido2", "num_volunteer":"998", "nif":"25604599X", "place":"Córdoba", 
                                 "phone":"882288877" ,"email":"persona2@gmail.com", "state":"Inactivo", "situation":"Necesita complemento",
                                "rol":"Supervisor", "observations":"Persona2 es supervisor", "computerKnowledge" :"False",
                                "truckKnowledge":"True", "warehouseKnowledge":"False","otherKnowledge":"Conductor experto"}).decode("utf-8")
        
        response = self.client.put(
            f'/volunteers/{volunteer.id}', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)

    def test_update_negative_volunteer_status_NOT_FOUND(self):
        data = JSONRenderer().render({"name":"Persona2","last_name": "Apellido2", "num_volunteer":"998", "nif":"25604599X", "place":"Córdoba", 
                                 "phone":"882288877" ,"email":"persona2@gmail.com", "state":"Inactivo", "situation":"Necesita complemento",
                                "rol":"Supervisor", "observations":"Persona2 es supervisor", "computerKnowledge" :"False",
                                "truckKnowledge":"True", "warehouseKnowledge":"False","otherKnowledge":"Conductor experto"}).decode("utf-8")
        response = self.client.put(
            '/volunteers/1', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 409)
        dataMessage = {'error': 'Volunteer not found...'}
        self.assertEqual(response.data, dataMessage)

    def test_update_negative_volunteer_status_CONFLICT(self):
        Volunteer.objects.create(name="Persona1",last_name= "Apellido1", num_volunteer="999", nif="25604599X", place="Sevilla", 
                                 phone="888888877" ,email="persona1@gmail.com", state="Activo", situation = "necesitaFormacion",
                                rol="Voluntario", observations="Persona1 es voluntario", computerKnowledge = True,
                                truckKnowledge=False, warehouseKnowledge="True",otherKnowledge="Limpieza")
        volunteer = Volunteer.objects.create(name="Persona2",last_name= "Apellido2", num_volunteer="998", nif="97232595A", place="Granada", 
                                 phone="888888899" ,email="persona2@gmail.com", state="Inactivo", situation = "necesitaFormacion",
                                rol="Voluntario", observations="Persona2 es voluntario", computerKnowledge = True,
                                truckKnowledge=False, warehouseKnowledge="True",otherKnowledge="Limpieza")
        data = JSONRenderer().render({"name":"Persona1","last_name": "Apellido1", "num_volunteer":"999", "nif":"25604599X", "place":"Sevilla", 
                                 "phone":"888888877" ,"email":"persona1@gmail.com", "state":"Activo", "situation":"necesitaFormacion",
                                "rol":"Voluntario", "observations":"Persona1 es voluntario", "computerKnowledge" :"True",
                                "truckKnowledge":"False", "warehouseKnowledge":"True","otherKnowledge":"Limpieza"}).decode("utf-8")
        response = self.client.put(
            f'/volunteers/{volunteer.id}', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 409)
        dataMessage = {
            "error": "There is already a volunteer with a field equal to the one you are trying to add, please check the data."}
        self.assertEqual(response.data, dataMessage)

    def test_update_positive_volunteer_validate_DNI_incorrect_letter(self):
        volunteer = Volunteer.objects.create(name="Persona1",last_name= "Apellido1", num_volunteer="999", nif="25604599X", place="Sevilla", 
                                 phone="888888877" ,email="persona1@gmail.com", state="Activo", situation = "necesitaFormacion",
                                rol="Voluntario", observations="Persona1 es voluntario", computerKnowledge = True,
                                truckKnowledge=False, warehouseKnowledge="True",otherKnowledge="Limpieza")
        data = JSONRenderer().render({"name":"Persona2","last_name": "Apellido2", "num_volunteer":"998", "nif":"25604599L", "place":"Córdoba", 
                                 "phone":"882288877" ,"email":"persona2@gmail.com", "state":"Inactivo", "situation":"Necesita complemento",
                                "rol":"Supervisor", "observations":"Persona2 es supervisor", "computerKnowledge" :"False",
                                "truckKnowledge":"True", "warehouseKnowledge":"False","otherKnowledge":"Conductor experto"}).decode("utf-8")
        
        response = self.client.put(
            f'/volunteers/{volunteer.id}', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 409)
        dataMessage = {'error': 'La letra del NIF no es correcta'}
        self.assertEqual(response.data, dataMessage)

    def test_update_positive_volunteer_validate_DNI_incorrect_format(self):
        volunteer = Volunteer.objects.create(name="Persona1",last_name= "Apellido1", num_volunteer="999", nif="25604599X", place="Sevilla", 
                                 phone="888888877" ,email="persona1@gmail.com", state="Activo", situation = "necesitaFormacion",
                                rol="Voluntario", observations="Persona1 es voluntario", computerKnowledge = True,
                                truckKnowledge=False, warehouseKnowledge="True",otherKnowledge="Limpieza")
        data = JSONRenderer().render({"name":"Persona2","last_name": "Apellido2", "num_volunteer":"998", "nif":"2", "place":"Córdoba", 
                                 "phone":"882288877" ,"email":"persona2@gmail.com", "state":"Inactivo", "situation":"Necesita complemento",
                                "rol":"Supervisor", "observations":"Persona2 es supervisor", "computerKnowledge" :"False",
                                "truckKnowledge":"True", "warehouseKnowledge":"False","otherKnowledge":"Conductor experto"}).decode("utf-8")
        
        response = self.client.put(
            f'/volunteers/{volunteer.id}', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 409)
        dataMessage = {'error': 'El formato del NIF no es correcto'}
        self.assertEqual(response.data, dataMessage)
        
 ################################################## DELETES ##################################################

    def test_delete_positive_volunteers_status_OK(self):
        volunteer = Volunteer.objects.create(name="Persona1",last_name= "Apellido1", num_volunteer="999", nif="25604599X", place="Sevilla", 
                                 phone="888888877" ,email="persona1@gmail.com", state="Activo", situation = "necesitaFormacion",
                                rol="Voluntario", observations="Persona1 es voluntario", computerKnowledge = True,
                                truckKnowledge=False, warehouseKnowledge="True",otherKnowledge="Limpieza")
        response = self.client.delete(f'/volunteers/{volunteer.id}')
        self.assertEqual(response.status_code, 204)
        dataMessage = {'message': 'Successfully deleted'}
        self.assertEqual(response.data, dataMessage)

    def test_delete_negative_volunteer_status_NOT_FOUND(self):
        response = self.client.delete('/volunteers/1')
        self.assertEqual(response.status_code, 404)
        dataMessage = {'error': 'Volunteer not found...'}
        self.assertEqual(response.data, dataMessage) 

class TurnTests(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="rosa", 
            password="rosa"
        )
        self.client.force_authenticate(user=self.user)

        ################################################## GETS ##################################################

    def test_list_positive_turns_status_OK(self):
        Turn.objects.create(date="2023-05-02", startTime="08:00", endTime="14:00")
        Turn.objects.create(date="2023-05-02", startTime="14:00", endTime="20:00")
        response = self.client.get('/volunteers/turns/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)), 2)
        
    def test_list_negative_turns_status_NOT_FOUND(self):
        response = self.client.get('/volunteers/turns/')
        data = {"message": "turn not found..."}
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.content), data)
        
    def test_show_positive_turns_status_OK(self):
        turn=Turn.objects.create(date="2023-05-02", startTime="08:00", endTime="14:00")
        response = self.client.get(f'/volunteers/turns/{turn.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["date"], datetime.date(2023, 5, 2))
        
    def test_show_negative_turns_status_NOT_FOUND(self):
        response = self.client.get('/volunteers/turns/1/')
        data = {"message": "turn not found..."}
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, data)
        
        ################################################## POSTS ##################################################
        
    def test_create_positive_turns_CREATED(self):
        data = JSONRenderer().render({"date":"2023-05-02", 
                                      "startTime":"08:00", "endTime":"14:00"}).decode("utf-8")
        response = self.client.post('/volunteers/turns/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)
    
    def test_create_negative_turns_wrong_date(self):
        data = JSONRenderer().render({"date":"2023-05-02", "startTime":"08:00", "endTime":"7:00"}).decode("utf-8")
        response = self.client.post('/volunteers/turns/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 409)
        dataMessage = {'error': 'La hora de inicio debe ser anterior a la hora de fin'}
        self.assertEqual(response.data, dataMessage)
        
        ################################################## PUTS ##################################################
        
    def test_update_positive_turns_status_OK(self):
        turn = Turn.objects.create(date="2023-05-02", startTime="08:00", endTime="14:00")
        data = JSONRenderer().render({"date":"2023-05-03", "startTime":"08:00", "endTime":"14:00"}).decode("utf-8")
        response = self.client.put(f'/volunteers/turns/{turn.id}/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)
    
    def test_update_negative_turns_status_NOT_FOUND(self):
        data = JSONRenderer().render({"date":"2023-05-02", "startTime":"08:00", "endTime":"14:00"}).decode("utf-8")
        response = self.client.put('/volunteers/turns/1/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 409)
        dataMessage = {'message': 'Turn not found...'}
        
        self.assertEqual(response.data, dataMessage)
        
    def test_update_negative_turns_wrong_date(self):
        turn = Turn.objects.create(date="2023-05-02", startTime="08:00", endTime="14:00")
        data = JSONRenderer().render({"date":"2023-05-02", "startTime":"08:00", "endTime":"7:00"}).decode("utf-8")
        response = self.client.put(f'/volunteers/turns/{turn.id}/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 409)
        dataMessage = {'error': 'La hora de inicio debe ser anterior a la hora de fin'}
        self.assertEqual(response.data, dataMessage)
    
    ################################################## DELETES ##################################################
    
    def test_delete_positive_turns_status_OK(self):
        turn = Turn.objects.create(date="2023-05-02", startTime="08:00", endTime="14:00")
        response = self.client.delete(f'/volunteers/turns/{turn.id}/')
        self.assertEqual(response.status_code, 204)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)
        
    def test_delete_negative_turns_status_NOT_FOUND(self):
        response = self.client.delete('/volunteers/turns/1/')
        self.assertEqual(response.status_code, 409)
        dataMessage = {'message': 'Turn not found...'}
        self.assertEqual(response.data, dataMessage) 
