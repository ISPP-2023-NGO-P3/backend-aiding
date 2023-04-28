from rest_framework.test import APITestCase
from .models import Event
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APIClient
from base.models import User
import pytz
import datetime
from aiding.settings import TIME_ZONE

class EventTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="ispp",
            password="ispp"
        )
        self.client.force_authenticate(user=self.user)

        ################################################## GETS ##################################################

    def test_list_positive_events_status_OK(self):
        Event.objects.create(title="evento1", description="descripcion1", start_date="2024-04-21", end_date="2024-04-22",
                             places=15, street="calle1", number="20", city="ciudad1", latitude=55, longitude=55)

        response = self.client.get('/events/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_list_negative_events_status_NOT_FOUND(self):
        response = self.client.get('/events/')
        data = {"message": "No events found..."}
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, data)

    def test_show_positive_event_status_OK(self):
        event=Event.objects.create(title="evento1", description="descripcion1", start_date="2024-04-21", end_date="2024-04-22",
                             places=15, street="calle1", number="20", city="ciudad1", latitude=55, longitude=55)
        response = self.client.get(f'/events/{event.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "evento1")

    def test_show_negative_event_status_NOT_FOUND(self):
        response = self.client.get('/events/1')
        data = {"message": "Event not found..."}
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, data)

    def test_listFuture_positive_events_status_OK(self):
        Event.objects.create(title="evento1", description="descripcion1", start_date="2024-04-21", end_date="2024-04-22",
                             places=15, street="calle1", number="20", city="ciudad1", latitude=55, longitude=55)

        response = self.client.get('/events/programed/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_listFuture_negative_events_status_NOT_FOUND(self):
        Event.objects.create(title="evento1", description="descripcion1", start_date="2022-04-21", end_date="2022-04-22",
                             places=15, street="calle1", number="20", city="ciudad1", latitude=55, longitude=55)

        response = self.client.get('/events/programed/')
        data = {"message": "No events found..."}
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, data)

    def test_listStarted_positive_events_status_OK(self):
        now = datetime.datetime.utcnow()
        tz = pytz.timezone(TIME_ZONE)
        now_aware = pytz.utc.localize(now).astimezone(tz)

        Event.objects.create(title="evento1", description="descripcion1", start_date=now_aware, end_date="2030-04-22",
                             places=15, street="calle1", number="20", city="ciudad1", latitude=55, longitude=55)

        response = self.client.get('/events/started/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_listStarted_negative_events_status_NOT_FOUND(self):
        Event.objects.create(title="evento1", description="descripcion1", start_date="2024-04-21", end_date="2024-04-22",
                             places=15, street="calle1", number="20", city="ciudad1", latitude=55, longitude=55)

        response = self.client.get('/events/started/')
        data = {"message": "No events found..."}
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, data)

    ################################################## POSTS ##################################################

    def test_create_positive_event_status_CREATED(self):
        data = JSONRenderer().render({"title":"Evento1","description": "Descripcion1", "start_date":"2024-04-21 14:00:00",
                                      "end_date":"2024-04-22 14:00:00","places":"15","street":"P.º de Cristóbal Colón",
                                      "number":"12","city":"Sevilla", "userTimezone":"UTC"}).decode("utf-8")
        response = self.client.post(
            '/events/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)

    def test_create_negative_event_status_PAST_START(self):
        data = JSONRenderer().render({"title":"Evento1","description": "Descripcion1", "start_date":"2022-04-21 14:00:00",
                                      "end_date":"2024-04-22 14:00:00","places":"15","street":"P.º de Cristóbal Colón",
                                      "number":"12","city":"Sevilla", "userTimezone":"UTC"}).decode("utf-8")
        response = self.client.post(
            '/events/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_create_negative_event_status_END_BEFORE_START(self):
        data = JSONRenderer().render({"title":"Evento1","description": "Descripcion1", "start_date":"2024-04-21 14:00:00",
                                      "end_date":"2022-04-22 14:00:00","places":"15","street":"P.º de Cristóbal Colón",
                                      "number":"12","city":"Sevilla", "userTimezone":"UTC"}).decode("utf-8")
        response = self.client.post(
            '/events/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_create_negative_event_status_PAST_DATES(self):
        data = JSONRenderer().render({"title":"Evento1","description": "Descripcion1", "start_date":"2022-04-21 14:00:00",
                                      "end_date":"2022-04-22 14:00:00","places":"15","street":"P.º de Cristóbal Colón",
                                      "number":"12","city":"Sevilla", "userTimezone":"UTC"}).decode("utf-8")
        response = self.client.post(
            '/events/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    ################################################## PUTS ##################################################

    def test_update_positive_event_status_OK(self):
        data1 = JSONRenderer().render({"title":"Evento1","description": "Descripcion1", "start_date":"2024-04-21 14:00:00",
                                      "end_date":"2024-04-22 14:00:00","places":"15","street":"P.º de Cristóbal Colón",
                                      "number":"12","city":"Sevilla", "userTimezone":"UTC"}).decode("utf-8")
        response = self.client.post(
            '/events/', data=data1, content_type='application/json')
        event = Event.objects.get(title="Evento1")
        data2 = JSONRenderer().render({"title":"EventoActualizado","description": "Descripcion1", "start_date":"2024-04-21 14:00:00",
                                      "end_date":"2024-04-22 14:00:00","places":"15","street":"P.º de Cristóbal Colón",
                                      "number":"12","city":"Sevilla", "userTimezone":"UTC"}).decode("utf-8")
        response = self.client.put(
            f'/events/{event.id}', data=data2, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)

    def test_update_negative_event_status_PAST_START(self):
        data1 = JSONRenderer().render({"title":"Evento1","description": "Descripcion1", "start_date":"2024-04-21 14:00:00",
                                      "end_date":"2024-04-22 14:00:00","places":"15","street":"P.º de Cristóbal Colón",
                                      "number":"12","city":"Sevilla", "userTimezone":"UTC"}).decode("utf-8")
        response = self.client.post(
            '/events/', data=data1, content_type='application/json')
        event = Event.objects.get(title="Evento1")
        data2 = JSONRenderer().render({"title":"Evento1","description": "Descripcion1", "start_date":"2022-04-21 14:00:00",
                                      "end_date":"2024-04-22 14:00:00","places":"15","street":"P.º de Cristóbal Colón",
                                      "number":"12","city":"Sevilla", "userTimezone":"UTC"}).decode("utf-8")
        response = self.client.put(
            f'/events/{event.id}', data=data2, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_update_negative_event_status_END_BEFORE_START(self):
        data1 = JSONRenderer().render({"title":"Evento1","description": "Descripcion1", "start_date":"2024-04-21 14:00:00",
                                      "end_date":"2024-04-22 14:00:00","places":"15","street":"P.º de Cristóbal Colón",
                                      "number":"12","city":"Sevilla", "userTimezone":"UTC"}).decode("utf-8")
        response = self.client.post(
            '/events/', data=data1, content_type='application/json')
        event = Event.objects.get(title="Evento1")
        data2 = JSONRenderer().render({"title":"Evento1","description": "Descripcion1", "start_date":"2024-04-21 14:00:00",
                                      "end_date":"2022-04-22 14:00:00","places":"15","street":"P.º de Cristóbal Colón",
                                      "number":"12","city":"Sevilla", "userTimezone":"UTC"}).decode("utf-8")
        response = self.client.put(
            f'/events/{event.id}', data=data2, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_update_negative_event_status_PAST_DATES(self):
        data1 = JSONRenderer().render({"title":"Evento1","description": "Descripcion1", "start_date":"2024-04-21 14:00:00",
                                      "end_date":"2024-04-22 14:00:00","places":"15","street":"P.º de Cristóbal Colón",
                                      "number":"12","city":"Sevilla", "userTimezone":"UTC"}).decode("utf-8")
        response = self.client.post(
            '/events/', data=data1, content_type='application/json')
        event = Event.objects.get(title="Evento1")
        data2 = JSONRenderer().render({"title":"Evento1","description": "Descripcion1", "start_date":"2022-04-21 14:00:00",
                                      "end_date":"2022-04-22 14:00:00","places":"15","street":"P.º de Cristóbal Colón",
                                      "number":"12","city":"Sevilla", "userTimezone":"UTC"}).decode("utf-8")
        response = self.client.put(
            f'/events/{event.id}', data=data2, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    ################################################## DELETES ##################################################

    def test_delete_positive_event_status_OK(self):
        data1 = JSONRenderer().render({"title":"Evento1","description": "Descripcion1", "start_date":"2024-04-21 14:00:00",
                                      "end_date":"2024-04-22 14:00:00","places":"15","street":"P.º de Cristóbal Colón",
                                      "number":"12","city":"Sevilla", "userTimezone":"UTC"}).decode("utf-8")
        response = self.client.post(
            '/events/', data=data1, content_type='application/json')
        event = Event.objects.get(title="Evento1")

        response = self.client.delete(
            f'/events/{event.id}')
        self.assertEqual(response.status_code, 204)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)

    def test_delete_negative_event_status_NOT_FOUND(self):
        data1 = JSONRenderer().render({"title":"Evento1","description": "Descripcion1", "start_date":"2024-04-21 14:00:00",
                                      "end_date":"2024-04-22 14:00:00","places":"15","street":"P.º de Cristóbal Colón",
                                      "number":"12","city":"Sevilla", "userTimezone":"UTC"}).decode("utf-8")
        response = self.client.post(
            '/events/', data=data1, content_type='application/json')
        event = Event.objects.get(title="Evento1")

        response = self.client.delete(
            f'/events/{event.id + 1}')
        self.assertEqual(response.status_code, 404)
        dataMessage = {'message': 'Event not found...'}
        self.assertEqual(response.data, dataMessage)

    ################################################## EVENTBOOKING ##################################################

    def test_post_positive_eventBooking_status_OK(self):
        data1 = JSONRenderer().render({"title":"Evento1","description": "Descripcion1", "start_date":"2024-04-21 14:00:00",
                                      "end_date":"2024-04-22 14:00:00","places":"15","street":"P.º de Cristóbal Colón",
                                      "number":"12","city":"Sevilla", "userTimezone":"UTC"}).decode("utf-8")
        response = self.client.post(
            '/events/', data=data1, content_type='application/json')
        event = Event.objects.get(title="Evento1")

        data2 = JSONRenderer().render({"name":"Asistente","phone": "666555444", "last_name":"Apellido"}).decode("utf-8")

        response = self.client.post(
            f'/events/{event.id}/booking/', data=data2, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        dataMessage = {'success': 'Booking created.'}
        self.assertEqual(response.data, dataMessage)

    def test_post_negative_eventBooking_status_EMPTY_FIELDS(self):
        data1 = JSONRenderer().render({"title":"Evento1","description": "Descripcion1", "start_date":"2024-04-21 14:00:00",
                                      "end_date":"2024-04-22 14:00:00","places":"15","street":"P.º de Cristóbal Colón",
                                      "number":"12","city":"Sevilla", "userTimezone":"UTC"}).decode("utf-8")
        response = self.client.post(
            '/events/', data=data1, content_type='application/json')
        event = Event.objects.get(title="Evento1")

        data2 = JSONRenderer().render({"name":"","phone": "666555444", "last_name":"Apellido"}).decode("utf-8")

        response = self.client.post(
            f'/events/{event.id}/booking/', data=data2, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        dataMessage = {'error': 'Name, last_name and phone are required.'}
        self.assertEqual(response.data, dataMessage)

    def test_post_positive_eventBooking_status_EMPTY_PLACES(self):
        data1 = JSONRenderer().render({"title":"Evento1","description": "Descripcion1", "start_date":"2024-04-21 14:00:00",
                                      "end_date":"2024-04-22 14:00:00","places":"0","street":"P.º de Cristóbal Colón",
                                      "number":"12","city":"Sevilla", "userTimezone":"UTC"}).decode("utf-8")
        response = self.client.post(
            '/events/', data=data1, content_type='application/json')
        event = Event.objects.get(title="Evento1")

        data2 = JSONRenderer().render({"name":"Asistente","phone": "666555444", "last_name":"Apellido"}).decode("utf-8")

        response = self.client.post(
            f'/events/{event.id}/booking/', data=data2, content_type='application/json')
        self.assertEqual(response.status_code, 409)
        dataMessage = {'error': 'No more places available.'}
        self.assertEqual(response.data, dataMessage)

    def test_post_positive_eventBooking_status_PAST_EVENT(self):
        event=Event.objects.create(title="evento1", description="descripcion1", start_date="2022-04-21", end_date="2022-04-22",
                             places=15, street="calle1", number="20", city="ciudad1", latitude=55, longitude=55)

        data2 = JSONRenderer().render({"name":"Asistente","phone": "666555444", "last_name":"Apellido"}).decode("utf-8")

        response = self.client.post(
            f'/events/{event.id}/booking/', data=data2, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        dataMessage = {'error': 'You can`t book a past event'}
        self.assertEqual(response.data, dataMessage)

class IntegrationTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="ispp",
            password="ispp"
        )
        self.client.force_authenticate(user=self.user)

    def test_positive_create_event(self):
        #Se crea un evento
        data = JSONRenderer().render({"title":"Evento1","description": "Descripcion1", "start_date":"2024-04-21 14:00:00",
                                      "end_date":"2024-04-22 14:00:00","places":"15","street":"P.º de Cristóbal Colón",
                                      "number":"12","city":"Sevilla", "userTimezone":"UTC"}).decode("utf-8")
        response = self.client.post(
            '/events/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)

        evento_test = Event.objects.get(title="Evento1")

        #Se muestra la lista de eventos
        response = self.client.get(f'/events/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        #Se muestra el evento creado
        response = self.client.get(f'/events/{evento_test.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("title"), "Evento1")