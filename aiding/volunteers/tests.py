from django.test import TestCase
from rest_framework.test import APITestCase
from .models import Volunteer, Turn, VolunteerTurn
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APIClient
from base.models import User
from django.contrib.auth.models import Group
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
        Volunteer.objects.create(name="Persona1",last_name= "Apellido1", nif="25604599X", place="Sevilla",
                                 phone="888888877" ,email="persona1@gmail.com", state="Activo", situation = "necesitaFormacion",
                                rol="Voluntario",  postal_code = "41001", observations="Persona1 es voluntario", computerKnowledge = True,
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
        volunteer=Volunteer.objects.create(name="Persona1",last_name= "Apellido1", nif="25604599X", place="Sevilla",
                                 phone="888888877" ,email="persona1@gmail.com", state="Activo", situation = "necesitaFormacion",
                                rol="Voluntario",  postal_code = "41001", observations="Persona1 es voluntario", computerKnowledge = True,
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
        data = JSONRenderer().render({"name":"Persona1","last_name": "Apellido1", "nif":"25604599X", "place":"Sevilla",
                                 "phone":"888888877" ,"email":"persona1@gmail.com", "state":"Activo", "situation":"necesitaFormacion",
                                "rol":"Voluntario", "postal_code" : "41001", "observations":"Persona1 es voluntario", "computerKnowledge" :"True",
                                "truckKnowledge":"False", "warehouseKnowledge":"True","otherKnowledge":"Limpieza"}).decode("utf-8")
        response = self.client.post(
            '/volunteers/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)

    def test_create_negative_volunteer_status_CONFLICT(self):
        Volunteer.objects.create(name="Persona1",last_name= "Apellido1", nif="25604599X", place="Sevilla",
                                 phone="888888877" ,email="persona1@gmail.com", state="Activo", situation = "necesitaFormacion",
                                rol="Voluntario",  postal_code = "41001", observations="Persona1 es voluntario", computerKnowledge = True,
                                truckKnowledge=False, warehouseKnowledge="True",otherKnowledge="Limpieza")
        data = JSONRenderer().render({"name":"Persona1","last_name": "Apellido1", "nif":"25604599X", "place":"Sevilla",
                                 "phone":"888888877" ,"email":"persona1@gmail.com", "state":"Activo", "situation":"necesitaFormacion",
                                "rol":"Voluntario", "postal_code":"41001", "observations":"Persona1 es voluntario", "computerKnowledge" :"True",
                                "truckKnowledge":"False", "warehouseKnowledge":"True","otherKnowledge":"Limpieza"}).decode("utf-8")
        response = self.client.post(
            '/volunteers/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 409)
        dataMessage = {
            "error": "There is already a volunteer with a field equal to the one you are trying to add, please check the data."}
        self.assertEqual(response.data, dataMessage)


    def test_create_negative_volunteer_validate_DNI_incorrect_letter(self):
        data = JSONRenderer().render({"name":"Persona1","last_name": "Apellido1", "nif":"25604599L", "place":"Sevilla",
                                 "phone":"888888877" ,"email":"persona1@gmail.com", "state":"Activo", "situation":"necesitaFormacion",
                                "rol":"Voluntario", "postal_code": "41001", "observations":"Persona1 es voluntario", "computerKnowledge" :"True",
                                "truckKnowledge":"False", "warehouseKnowledge":"True","otherKnowledge":"Limpieza"}).decode("utf-8")
        response = self.client.post(
            '/volunteers/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 409)
        data = {"error": "La letra del NIF no es correcta"}
        self.assertEqual(response.data, data)

    def test_create_negative_volunteer_validate_DNI_incorrect_format(self):
        data = JSONRenderer().render({"name":"Persona1","last_name": "Apellido1", "nif":"2", "place":"Sevilla",
                                 "phone":"888888877" ,"email":"persona1@gmail.com", "state":"Activo", "situation":"necesitaFormacion",
                                "rol":"Voluntario",  "postal_code" : "41001", "observations":"Persona1 es voluntario", "computerKnowledge" :"True",
                                "truckKnowledge":"False", "warehouseKnowledge":"True","otherKnowledge":"Limpieza"}).decode("utf-8")
        response = self.client.post(
            '/volunteers/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 409)
        data = {"error": "El formato del NIF no es correcto"}
        self.assertEqual(response.data, data)

 ################################################## PUTS ##################################################

    def test_update_positive_volunteer_status_OK(self):
        volunteer = Volunteer.objects.create(name="Persona1",last_name= "Apellido1", nif="25604599X", place="Sevilla",
                                 phone="888888877" ,email="persona1@gmail.com", state="Activo", situation = "necesitaFormacion",
                                rol="Voluntario",  postal_code= "41001", observations="Persona1 es voluntario", computerKnowledge = True,
                                truckKnowledge=False, warehouseKnowledge="True",otherKnowledge="Limpieza")
        data = JSONRenderer().render({"name":"Persona2","last_name": "Apellido2","nif":"25604599X", "place":"Córdoba",
                                 "phone":"882288877" ,"email":"persona2@gmail.com", "state":"Inactivo", "situation":"Necesita complemento",
                                "rol":"Supervisor",  "postal_code" : "41001","observations":"Persona2 es supervisor", "computerKnowledge" :"False",
                                "truckKnowledge":"True", "warehouseKnowledge":"False","otherKnowledge":"Conductor experto"}).decode("utf-8")

        response = self.client.put(
            f'/volunteers/{volunteer.id}', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)

    def test_update_negative_volunteer_status_NOT_FOUND(self):
        data = JSONRenderer().render({"name":"Persona2","last_name": "Apellido2","nif":"25604599X", "place":"Córdoba",
                                 "phone":"882288877" ,"email":"persona2@gmail.com", "state":"Inactivo", "situation":"Necesita complemento",
                                "rol":"Supervisor",  "postal_code" : "41001", "observations":"Persona2 es supervisor", "computerKnowledge" :"False",
                                "truckKnowledge":"True", "warehouseKnowledge":"False","otherKnowledge":"Conductor experto"}).decode("utf-8")
        response = self.client.put(
            '/volunteers/1', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 409)
        dataMessage = {'error': 'Volunteer not found...'}
        self.assertEqual(response.data, dataMessage)

    def test_update_negative_volunteer_status_CONFLICT(self):
        Volunteer.objects.create(name="Persona1",last_name= "Apellido1", nif="25604599X", place="Sevilla",
                                 phone="888888877" ,email="persona1@gmail.com", state="Activo", situation = "necesitaFormacion",
                                rol="Voluntario",  postal_code = "41001",observations="Persona1 es voluntario", computerKnowledge = True,
                                truckKnowledge=False, warehouseKnowledge="True",otherKnowledge="Limpieza")
        volunteer = Volunteer.objects.create(name="Persona2",last_name= "Apellido2", nif="97232595A", place="Granada",
                                 phone="888888899" ,email="persona2@gmail.com", state="Inactivo", situation = "necesitaFormacion",
                                rol="Voluntario", postal_code = "41001", observations="Persona2 es voluntario", computerKnowledge = True,
                                truckKnowledge=False, warehouseKnowledge="True",otherKnowledge="Limpieza")
        data = JSONRenderer().render({"name":"Persona1","last_name": "Apellido1", "nif":"25604599X", "place":"Sevilla",
                                 "phone":"888888877" ,"email":"persona1@gmail.com", "state":"Activo", "situation":"necesitaFormacion",
                                "rol":"Voluntario",  "postal_code": "41001", "observations":"Persona1 es voluntario", "computerKnowledge" :"True",
                                "truckKnowledge":"False", "warehouseKnowledge":"True","otherKnowledge":"Limpieza"}).decode("utf-8")
        response = self.client.put(
            f'/volunteers/{volunteer.id}', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 409)
        dataMessage = {
            "error": "There is already a volunteer with a field equal to the one you are trying to add, please check the data."}
        self.assertEqual(response.data, dataMessage)

    def test_update_positive_volunteer_validate_DNI_incorrect_letter(self):
        volunteer = Volunteer.objects.create(name="Persona1",last_name= "Apellido1", nif="25604599X", place="Sevilla",
                                 phone="888888877" ,email="persona1@gmail.com", state="Activo", situation = "necesitaFormacion",
                                rol="Voluntario",  postal_code = "41001", observations="Persona1 es voluntario", computerKnowledge = True,
                                truckKnowledge=False, warehouseKnowledge="True",otherKnowledge="Limpieza")
        data = JSONRenderer().render({"name":"Persona2","last_name": "Apellido2", "nif":"25604599L", "place":"Córdoba",
                                 "phone":"882288877" ,"email":"persona2@gmail.com", "state":"Inactivo", "situation":"Necesita complemento",
                                "rol":"Supervisor", "postal_code" : "41001", "observations":"Persona2 es supervisor", "computerKnowledge" :"False",
                                "truckKnowledge":"True", "warehouseKnowledge":"False","otherKnowledge":"Conductor experto"}).decode("utf-8")
        
        response = self.client.put(
            f'/volunteers/{volunteer.id}', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 409)
        dataMessage = {'error': 'La letra del NIF no es correcta'}
        self.assertEqual(response.data, dataMessage)

    def test_update_positive_volunteer_validate_DNI_incorrect_format(self):
        volunteer = Volunteer.objects.create(name="Persona1",last_name= "Apellido1",  nif="25604599X", place="Sevilla",
                                 phone="888888877" ,email="persona1@gmail.com", state="Activo", situation = "necesitaFormacion",
                                rol="Voluntario", postal_code = "41001", observations="Persona1 es voluntario", computerKnowledge = True,
                                truckKnowledge=False, warehouseKnowledge="True",otherKnowledge="Limpieza")
        data = JSONRenderer().render({"name":"Persona2","last_name": "Apellido2", "nif":"2", "place":"Córdoba",
                                 "phone":"882288877" ,"email":"persona2@gmail.com", "state":"Inactivo", "situation":"Necesita complemento",
                                "rol":"Supervisor", "postal_code":"41001", "observations":"Persona2 es supervisor", "computerKnowledge" :"False",
                                "truckKnowledge":"True", "warehouseKnowledge":"False","otherKnowledge":"Conductor experto"}).decode("utf-8")
        
        response = self.client.put(
            f'/volunteers/{volunteer.id}', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 409)
        dataMessage = {'error': 'El formato del NIF no es correcto'}
        self.assertEqual(response.data, dataMessage)
        
 ################################################## DELETES ##################################################

    def test_delete_positive_volunteers_status_OK(self):
        volunteer = Volunteer.objects.create(name="Persona1",last_name= "Apellido1", nif="25604599X", place="Sevilla", 
                                 phone="888888877" ,email="persona1@gmail.com", state="Activo", situation = "necesitaFormacion",
                                rol="Voluntario", postal_code = "41001", observations="Persona1 es voluntario", computerKnowledge = True,
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
        role = Group.objects.get_or_create(name="supervisor")[0]
        self.user = User.objects.create(
            username="ispp",
            password="ispp",
            roles=role
        )
        self.client.force_authenticate(user=self.user)
        ################################################## GETS ##################################################

    def test_list_positive_turns_status_OK(self):
        supevisor_id = self.user
        Turn.objects.create(date="2023-05-02", startTime="08:00", endTime="14:00", title="Turno1", supervisor=supevisor_id, draft=False)
        Turn.objects.create(date="2023-05-02", startTime="14:00", endTime="20:00", title="Turno2", supervisor=supevisor_id, draft=False)
        response = self.client.get('/volunteers/turns/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)), 2)
        
    def test_list_negative_turns_status_NOT_FOUND(self):
        response = self.client.get('/volunteers/turns/')
        data = {"message": "turn not found..."}
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.content), data)
        
    def test_show_positive_turns_status_OK(self):
        turn=Turn.objects.create(date="2023-05-02", startTime="08:00", endTime="14:00", title="Turno1", supervisor=self.user, draft=False)
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
                                      "startTime":"08:00", "endTime":"14:00", "title":"Turno1", "supervisor": "id", "draft":"False"}).decode("utf-8")
        response = self.client.post('/volunteers/turns/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)
    
    def test_create_negative_turns_wrong_date(self):
        id = self.user
        data = JSONRenderer().render({"date":"2023-05-02", "startTime":"08:00", "endTime":"7:00",
                                      "title":"Turno1", "supervisor": "id", "draft":"True"}).decode("utf-8")
        response = self.client.post('/volunteers/turns/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 409)
        dataMessage = {'error': 'La hora de inicio debe ser anterior a la hora de fin'}
        self.assertEqual(response.data, dataMessage)
        
        ################################################## PUTS ##################################################
        
    def test_update_positive_turns_status_OK(self):
        id =self.user
        turn = Turn.objects.create(date="2023-05-02", startTime="08:00", endTime="14:00", title="Turno1", supervisor=id, draft=False)
        data = JSONRenderer().render({"date":"2023-05-02", "startTime":"08:00", "endTime":"14:00",
                                      "title":"Turno1", "supervisor": "id", "draft":"False"}).decode("utf-8")
        response = self.client.put(f'/volunteers/turns/{turn.id}/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)
    
    def test_update_negative_turns_status_NOT_FOUND(self):
        id =self.user
        data = JSONRenderer().render({"date":"2023-05-02", "startTime":"08:00", "endTime":"14:00",
                                      "title":"Turno1", "supervisor": "id", "draft":"False"}).decode("utf-8")
        response = self.client.put('/volunteers/turns/1/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        dataMessage = {'message': 'Turn not found...'}
        
        self.assertEqual(response.data, dataMessage)
        
    def test_update_negative_turns_wrong_date(self):
        id =self.user
        turn = Turn.objects.create(date="2023-05-02", startTime="08:00", endTime="14:00", title="Turno1", supervisor=id, draft=False)
        data = JSONRenderer().render({"date":"2023-05-02", "startTime":"08:00", "endTime":"7:00",
                                      "title":"Turno1", "supervisor": "id", "draft":"False"}).decode("utf-8")
        response = self.client.put(f'/volunteers/turns/{turn.id}/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 409)
        dataMessage = {'error': 'La hora de inicio debe ser anterior a la hora de fin'}
        self.assertEqual(response.data, dataMessage)
    
    ################################################## DELETES ##################################################
    
    def test_delete_positive_turns_status_OK(self):
        turn = Turn.objects.create(date="2023-05-02", startTime="08:00", endTime="14:00", title="Turno1", supervisor=self.user, draft=False)
        response = self.client.delete(f'/volunteers/turns/{turn.id}/')
        self.assertEqual(response.status_code, 204)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)
        
    def test_delete_negative_turns_status_NOT_FOUND(self):
        response = self.client.delete('/volunteers/turns/1/')
        self.assertEqual(response.status_code, 409)
        dataMessage = {'message': 'Turn not found...'}
        self.assertEqual(response.data, dataMessage)

class VolunteerTurnTests(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        role = Group.objects.get_or_create(name="supervisor")[0]
        self.user = User.objects.create(
            username="ispp",
            password="ispp",
            roles=role
        )
        self.client.force_authenticate(user=self.user)
        
        ################################################## GETS ##################################################
        
    def test_list_positive_volunteer_turns_status_OK(self):
        turn = Turn.objects.create(date="2023-05-02", startTime="08:00", endTime="14:00", title="Turno1", supervisor=self.user, draft=False)
        volunteer = Volunteer.objects.create(name="Persona1",last_name= "Apellido1", nif="25604599X", place="Sevilla",
                            phone="888888877" ,email="persona1@gmail.com", state="Activo", situation = "necesitaFormacion",
                        rol="Voluntario", observations="Persona1 es voluntario", computerKnowledge = True,
                        truckKnowledge=False, warehouseKnowledge="True",otherKnowledge="Limpieza")
        VolunteerTurn.objects.create(volunteer=volunteer, turn=turn)
        response = self.client.get('/volunteers/volunteerTurns/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)), 1)
        
    def test_list_negative_volunteer_turns_status_NOT_FOUND(self):
        response = self.client.get('/volunteers/volunteerTurns/')
        data = {"message": "Volunteer turn not found..."}
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.content), data)
    
    def test_show_positive_volunteer_turns_status_OK(self):
        turn = Turn.objects.create(date="2023-05-02", startTime="08:00", endTime="14:00", title="Turno1", supervisor=self.user, draft=False)
        volunteer = Volunteer.objects.create(name="Persona1",last_name= "Apellido1", nif="25604599X", place="Sevilla",
                            phone="888888877" ,email="persona1@gmail.com", state="Activo", situation = "necesitaFormacion",
                        rol="Voluntario", observations="Persona1 es voluntario", computerKnowledge = True,
                        truckKnowledge=False, warehouseKnowledge="True",otherKnowledge="Limpieza")
        vt = VolunteerTurn.objects.create(volunteer=volunteer, turn=turn)
        response = self.client.get(f'/volunteers/volunteerTurns/{vt.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["volunteer_id"], volunteer.id)
        
    def test_show_negative_volunteer_turns_status_NOT_FOUND(self):
        response = self.client.get('/volunteers/volunteerTurns/1/')
        data = {"message": "Volunteer turn not found..."}
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.content), data)
    
    def test_show_positive_volunteers_in_turn_status_OK(self):
        turn = Turn.objects.create(date="2023-05-02", startTime="08:00", endTime="14:00", title="Turno1", supervisor=self.user, draft=False)
        volunteer = Volunteer.objects.create(name="Persona1",last_name= "Apellido1", nif="25604599X", place="Sevilla",
                            phone="888888877" ,email="persona1@gmail.com", state="Activo", situation = "necesitaFormacion",
                        rol="Voluntario", observations="Persona1 es voluntario", computerKnowledge = True,
                        truckKnowledge=False, warehouseKnowledge="True",otherKnowledge="Limpieza")
        volunteer2 = Volunteer.objects.create(name="Persona2",last_name= "Apellido2", nif="54181998R", place="Sevilla",
                    phone="888888879" ,email="persona2@gmail.com", state="Activo", situation = "necesitaFormacion",
                rol="Voluntario", observations="Persona1 es voluntario", computerKnowledge = True,
                truckKnowledge=False, warehouseKnowledge="True",otherKnowledge="Limpieza")
        VolunteerTurn.objects.create(volunteer=volunteer, turn=turn)
        VolunteerTurn.objects.create(volunteer=volunteer2, turn=turn)
        response = self.client.get(f'/volunteers/turns/{turn.id}/volunteers')
        self.assertEqual(response.status_code, 200)
        res = json.loads(response.content)
        self.assertEqual(len(res['volunteerTurn']), 2)
    
    def test_show_negative_volunteers_in_turn_status_NOT_FOUND(self):
        response = self.client.get(f'/volunteers/turns/1/volunteers')
        data = {"message": "Turn not found..."}
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.content), data)
        
    def test_show_positive_turns_in_volunteer_status_OK(self):
        turn = Turn.objects.create(date="2023-05-02", startTime="08:00", endTime="14:00", title="Turno1", supervisor=self.user, draft=False)
        turn2 = Turn.objects.create(date="2023-05-03", startTime="08:00", endTime="14:00", title="Turno2", supervisor=self.user, draft=False)
        volunteer = Volunteer.objects.create(name="Persona1",last_name= "Apellido1", nif="25604599X", place="Sevilla",
                            phone="888888877" ,email="persona1@gmail.com", state="Activo", situation = "necesitaFormacion",
                        rol="Voluntario", observations="Persona1 es voluntario", computerKnowledge = True,
                        truckKnowledge=False, warehouseKnowledge="True",otherKnowledge="Limpieza")
        VolunteerTurn.objects.create(volunteer=volunteer, turn=turn)
        VolunteerTurn.objects.create(volunteer=volunteer, turn=turn2)
        response = self.client.get(f'/volunteers/{volunteer.id}/turns')
        self.assertEqual(response.status_code, 200)
        res = json.loads(response.content)
        self.assertEqual(len(res['volunteerTurn']), 2)
        
    def test_show_negative_turns_in_volunteer_status_NOT_FOUND(self):
        response = self.client.get(f'/volunteers/1/turns')
        data = {"message": "Volunteer not found..."}
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.content), data)
        
    ################################################## POSTS ####################################################
    
    def test_post_positive_volunteer_turns_status_OK(self):
        turn = Turn.objects.create(date="2023-05-02", startTime="08:00", endTime="14:00", title="Turno1", supervisor=self.user, draft=False)
        volunteer = Volunteer.objects.create(name="Persona1",last_name= "Apellido1", nif="25604599X", place="Sevilla", 
                            phone="888888877" ,email="persona1@gmail.com", state="Activo", situation = "necesitaFormacion",
                        rol="Voluntario", observations="Persona1 es voluntario", computerKnowledge = True,
                        truckKnowledge=False, warehouseKnowledge="True",otherKnowledge="Limpieza")
        data = JSONRenderer().render({"volunteer_id":volunteer.id, "turn_id":turn.id}).decode("utf-8")
        response = self.client.post('/volunteers/volunteerTurns/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)
    
    def test_post_negative_volunteer_turns_status_NOT_FOUND_volunteer(self):
        turn = Turn.objects.create(date="2023-05-02", startTime="08:00", endTime="14:00", title="Turno1", supervisor=self.user, draft=False)
        data = JSONRenderer().render({"volunteer_id":"2", "turn_id":turn.id}).decode("utf-8")
        response = self.client.post('/volunteers/volunteerTurns/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        dataMessage = {'message': 'Volunteer not found...'}
        self.assertEqual(response.data, dataMessage)

    def test_post_negative_volunteer_turns_status_NOT_FOUND_turn(self):
        volunteer = Volunteer.objects.create(name="Persona1",last_name= "Apellido1", nif="25604599X", place="Sevilla", 
                        phone="888888877" ,email="persona1@gmail.com", state="Activo", situation = "necesitaFormacion",
                    rol="Voluntario", observations="Persona1 es voluntario", computerKnowledge = True,
                    truckKnowledge=False, warehouseKnowledge="True",otherKnowledge="Limpieza")
        data = JSONRenderer().render({"volunteer_id":volunteer.id, "turn_id":"2"}).decode("utf-8")
        response = self.client.post('/volunteers/volunteerTurns/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        dataMessage = {'message': 'Turn not found...'}
        self.assertEqual(response.data, dataMessage)
    
    def test_post_negative_volunteer_turns_status_DUPLICATE(self):
        #Creamos los datos
        turn = Turn.objects.create(date="2023-05-02", startTime="08:00", endTime="14:00", title="Turno1", supervisor=self.user, draft=False)
        volunteer = Volunteer.objects.create(name="Persona1",last_name= "Apellido1", nif="25604599X", place="Sevilla", 
                            phone="888888877" ,email="persona1@gmail.com", state="Activo", situation = "necesitaFormacion",
                        rol="Voluntario", observations="Persona1 es voluntario", computerKnowledge = True,
                        truckKnowledge=False, warehouseKnowledge="True",otherKnowledge="Limpieza")
        #Introducimos el primer dato
        data = JSONRenderer().render({"volunteer_id":volunteer.id, "turn_id":turn.id}).decode("utf-8")
        self.client.post('/volunteers/volunteerTurns/', data=data, content_type='application/json')
        #Introducimos el segundo dato, que es el mismo que el primero
        data2 = JSONRenderer().render({"volunteer_id":volunteer.id, "turn_id":turn.id}).decode("utf-8")
        response = self.client.post('/volunteers/volunteerTurns/', data=data2, content_type='application/json')
        self.assertEqual(response.status_code, 409)
        dataMessage = {'error': 'Este voluntario ya tiene asignado el mismo turno'}
        self.assertEqual(response.data, dataMessage)
        
    ################################################## PUTS #####################################################
        
    def test_update_positive_volunteer_turns_status_OK(self):
        turn = Turn.objects.create(date="2023-05-02", startTime="08:00", endTime="14:00", title="Turno1", supervisor=self.user, draft=False)
        edited_turn = Turn.objects.create(date="2023-05-03", startTime="08:00", endTime="14:00", title="Turno2", supervisor=self.user, draft=False)
        volunteer = Volunteer.objects.create(name="Persona1",last_name= "Apellido1", nif="25604599X", place="Sevilla", 
                            phone="888888877" ,email="persona1@gmail.com", state="Activo", situation = "necesitaFormacion",
                        rol="Voluntario", observations="Persona1 es voluntario", computerKnowledge = True,
                        truckKnowledge=False, warehouseKnowledge="True",otherKnowledge="Limpieza")
        vt = VolunteerTurn.objects.create(volunteer=volunteer, turn=turn)
        data = JSONRenderer().render({"volunteer_id":volunteer.id, "turn_id":edited_turn.id}).decode("utf-8")
        response = self.client.put(f'/volunteers/volunteerTurns/{vt.id}/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)
        
    def test_update_negative_volunteer_turns_status_NOT_FOUND_volunteer(self):
        turn = Turn.objects.create(date="2023-05-02", startTime="08:00", endTime="14:00", title="Turno1", supervisor=self.user, draft=False)
        volunteer = Volunteer.objects.create(name="Persona1",last_name= "Apellido1", nif="25604599X", place="Sevilla", 
                    phone="888888877" ,email="persona1@gmail.com", state="Activo", situation = "necesitaFormacion",
                rol="Voluntario", observations="Persona1 es voluntario", computerKnowledge = True,
                truckKnowledge=False, warehouseKnowledge="True",otherKnowledge="Limpieza")
        vt = VolunteerTurn.objects.create(volunteer=volunteer, turn=turn)
        data = JSONRenderer().render({"volunteer_id":"99", "turn_id":turn.id}).decode("utf-8")
        response = self.client.put(f'/volunteers/volunteerTurns/{vt.id}/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        dataMessage = {'message': 'Volunteer not found...'}
        self.assertEqual(response.data, dataMessage)
    
    def test_update_negative_volunteer_turns_status_NOT_FOUND_turn(self):
        turn = Turn.objects.create(date="2023-05-02", startTime="08:00", endTime="14:00", title="Turno1", supervisor=self.user, draft=False)
        volunteer = Volunteer.objects.create(name="Persona1",last_name= "Apellido1", nif="25604599X", place="Sevilla", 
                    phone="888888877" ,email="persona1@gmail.com", state="Activo", situation = "necesitaFormacion",
                rol="Voluntario", observations="Persona1 es voluntario", computerKnowledge = True,
                truckKnowledge=False, warehouseKnowledge="True",otherKnowledge="Limpieza")
        vt = VolunteerTurn.objects.create(volunteer=volunteer, turn=turn)
        data = JSONRenderer().render({"volunteer_id":volunteer.id, "turn_id":"99"}).decode("utf-8")
        response = self.client.put(f'/volunteers/volunteerTurns/{vt.id}/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        dataMessage = {'message': 'Turn not found...'}
        self.assertEqual(response.data, dataMessage)

    def test_update_negative_volunteer_turns_status_NOT_FOUND_volunteerTurn(self):
        data = JSONRenderer().render({"volunteer_id":"1", "turn_id":"1"}).decode("utf-8")
        response = self.client.put('/volunteers/volunteerTurns/1/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 409)
        dataMessage = {'message': 'Volunteer Turn not found...'}
        self.assertEqual(response.data, dataMessage)

    ################################################## DELETES ##################################################
    
    def test_delete_positive_turns_status_OK(self):
        turn = Turn.objects.create(date="2023-05-02", startTime="08:00", endTime="14:00", title="Turno1", supervisor=self.user, draft=False)
        volunteer = Volunteer.objects.create(name="Persona1",last_name= "Apellido1",  nif="25604599X", place="Sevilla", 
                            phone="888888877" ,email="persona1@gmail.com", state="Activo", situation = "necesitaFormacion",
                        rol="Voluntario", observations="Persona1 es voluntario", computerKnowledge = True,
                        truckKnowledge=False, warehouseKnowledge="True",otherKnowledge="Limpieza")
        vt = VolunteerTurn.objects.create(volunteer=volunteer, turn=turn)
        response = self.client.delete(f'/volunteers/volunteerTurns/{vt.id}/')
        self.assertEqual(response.status_code, 204)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)
        
    def test_delete_negative_turns_status_NOT_FOUND(self):
        response = self.client.delete('/volunteers/volunteerTurns/1/')
        self.assertEqual(response.status_code, 409)
        dataMessage = {'message': 'Volunteer Turn not found...'}
        self.assertEqual(response.data, dataMessage)  


class IntegrationTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        role = Group.objects.get_or_create(name="supervisor")[0]
        self.user = User.objects.create(
            username="ispp",
            password="ispp",
            is_admin=True,
            roles=role
        )
        self.client.force_authenticate(user=self.user)

    def test_1(self):
        # Creo dos voluntarios, creo dos turnos y los asigno

        volunteer1=Volunteer.objects.create(name="Persona1",last_name= "Apellido1", num_volunteer="1", nif="25604599X", place="Sevilla",
                                 phone="888888877" ,email="persona1@gmail.com", state="Activo", situation = "necesitaFormacion",
                                rol="Voluntario",  postal_code = "41001", observations="Persona1 es voluntario", computerKnowledge = True,
                                truckKnowledge=False, warehouseKnowledge="True",otherKnowledge="Limpieza")
        volunteer2=Volunteer.objects.create(name="Persona2",last_name= "Apellido2", num_volunteer="2", nif="29567219Y", place="Sevilla",
                                 phone="888888878" ,email="persona2@gmail.com", state="Activo", situation = "necesitaFormacion",
                                rol="Voluntario",  postal_code = "41001", observations="Persona1 es voluntario", computerKnowledge = True,
                                truckKnowledge=False, warehouseKnowledge="True",otherKnowledge="Limpieza")
        
        turn = Turn.objects.create(date="2023-05-02", startTime="08:00", endTime="14:00", title="Turno1", supervisor=self.user, draft=False)
        turn2 = Turn.objects.create(date="2023-05-03", startTime="08:00", endTime="14:00", title="Turno2", supervisor=self.user, draft=False)
 
        data = JSONRenderer().render({"volunteer_id":volunteer1.id, "turn_id":turn.id}).decode("utf-8")
        response = self.client.post('/volunteers/volunteerTurns/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)

        vt1=VolunteerTurn.objects.get(id=1)

        data = JSONRenderer().render({"volunteer_id":volunteer2.id, "turn_id":turn2.id}).decode("utf-8")
        response = self.client.post('/volunteers/volunteerTurns/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)

        # Muevo a un voluntario a otro turno
        data = JSONRenderer().render({"volunteer_id":volunteer1.id, "turn_id":turn2.id}).decode("utf-8")
        response = self.client.post('/volunteers/volunteerTurns/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)

        vt3=VolunteerTurn.objects.get(id=3)
        response = self.client.delete(f'/volunteers/volunteerTurns/{vt1.id}/')
        self.assertEqual(response.status_code, 204)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)

        # Borro un turno y compruebo que las asignaciones de voluntarios han desaparecido
        vts_before=VolunteerTurn.objects.filter(turn=turn2)
        response = self.client.delete(f'/volunteers/turns/{turn2.id}/')
        self.assertEqual(response.status_code, 204)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)
        vts_after=VolunteerTurn.objects.filter(turn=turn2)

        self.assertEqual(len(vts_before)>len(vts_after),0)


        








