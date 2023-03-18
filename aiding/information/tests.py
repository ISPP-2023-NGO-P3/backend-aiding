from rest_framework.test import APITestCase
from .models import Section, Advertisement, Multimedia, Resource
from rest_framework.renderers import JSONRenderer


class SectionTests(APITestCase):

    ################################################## GETS ##################################################

    def test_list_positive_sections_status_OK(self):
        # Para probar que la respuesta HTTP de un código 200, se debe de crear previamente una seccion
        Section.objects.create(name="Seccion 1", active=True)
        Section.objects.create(name="Seccion 2", active=False)
        response = self.client.get('/information/sections/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_list_negative_sections_status_NOT_FOUND(self):
        response = self.client.get('/information/sections/')
        data = {"message": "sections not found..."}
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, data)

    def test_show_positive_section_status_OK(self):
        section = Section.objects.create(name="Seccion 1", active=True)
        response = self.client.get(f'/information/sections/{section.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Seccion 1")

    def test_show_negative_section_status_NOT_FOUND(self):
        response = self.client.get('/information/sections/1')
        data = {"message": "section not found..."}
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, data)

    ################################################## POSTS ##################################################

    def test_create_positive_section_status_CREATED(self):
        data = JSONRenderer().render({"name": "Seccion 1"}).decode("utf-8")
        response = self.client.post(
            '/information/sections/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)

    def test_create_negative_section_status_CONFLICT(self):
        Section.objects.create(name="Seccion 1")
        data = JSONRenderer().render({"name": "Seccion 1"}).decode("utf-8")
        response = self.client.post(
            '/information/sections/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 409)
        dataMessage = {
            "error": "This section was added into the page, please create another different"}
        self.assertEqual(response.data, dataMessage)

    ################################################## PUTS ##################################################

    def test_update_positive_section_status_OK(self):
        section = Section.objects.create(name="Seccion 1")
        data = JSONRenderer().render(
            {"name": "Seccion 2", "active": True}).decode("utf-8")
        response = self.client.put(
            f'/information/sections/{section.id}', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)

    def test_update_negative_section_status_NOT_FOUND(self):
        data = JSONRenderer().render({"name": "Seccion 2"}).decode("utf-8")
        response = self.client.put(
            '/information/sections/1', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        dataMessage = {'message': 'Section not found...'}
        self.assertEqual(response.data, dataMessage)

    def test_update_negative_section_status_CONFLICT(self):
        Section.objects.create(name="Seccion 1")
        section = Section.objects.create(name="Seccion 2")
        data = JSONRenderer().render(
            {"name": "Seccion 1", "active": True}).decode("utf-8")
        response = self.client.put(
            f'/information/sections/{section.id}', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 409)
        dataMessage = {
            "error": "This section was added into the page, please select another different"}
        self.assertEqual(response.data, dataMessage)

    ################################################## DELETES ##################################################

    def test_delete_positive_section_status_OK(self):
        section = Section.objects.create(name="Seccion 1")
        response = self.client.delete(f'/information/sections/{section.id}')
        self.assertEqual(response.status_code, 204)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)

    def test_delete_negative_section_status_NOT_FOUND(self):
        response = self.client.delete('/information/sections/1')
        self.assertEqual(response.status_code, 404)
        dataMessage = {'message': 'Section not found...'}
        self.assertEqual(response.data, dataMessage)


class AdvertisementTests(APITestCase):

    ################################################## GETS ##################################################

    def test_list_positive_advertisements_status_OK(self):
        # Para probar que la respuesta HTTP de un código 200, se debe de crear previamente una seccion
        section = Section.objects.create(name="Seccion 1", active=True)
        Advertisement.objects.create(
            title="Anuncio 1", abstract="Resumen 1", body="Descripcion 1", url="https://www.google.com", section=section)
        response = self.client.get('/information/advertisements/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_list_negative_advertisements_status_NOT_FOUND(self):
        response = self.client.get('/information/advertisements/')
        data = {"message": "advertisements not found..."}
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, data)

    def test_show_positive_advertisement_status_OK(self):
        section = Section.objects.create(name="Seccion 1", active=True)
        advertisement = Advertisement.objects.create(
            title="Anuncio 1", abstract="Resumen 1", body="Descripcion 1", url="https://www.google.com", section=section)
        response = self.client.get(
            f'/information/advertisements/{advertisement.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "Anuncio 1")

    def test_show_negative_advertisement_status_NOT_FOUND(self):
        response = self.client.get('/information/advertisements/1')
        data = {"message": "advertisement not found..."}
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, data)

    ################################################## POSTS ##################################################

    def test_create_positive_advertisement_status_CREATED(self):
        section = JSONRenderer().render({"name" : "Seccion 1", "active" : True})
        data = JSONRenderer().render({"title": "Anuncio 1", "abstract": "Resumen 1", "body": "Descripcion 1",
                                      "url": "https://www.google.com", "section_id": section}).decode("utf-8")
        response = self.client.post(
            '/information/advertisements/', data=data, content_type='application/json')
        print(response.data)
        print(data)
        #Revisar porque no funciona correctamente el test
