from rest_framework.test import APITestCase
from .models import Section, Advertisement, Multimedia
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APIClient
from base.models import User
class SectionTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="ispp",
            password="ispp"
        )
        self.client.force_authenticate(user=self.user)

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

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="ispp",
            password="ispp"
        )
        self.client.force_authenticate(user=self.user)

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
        section = Section.objects.create(name="Seccion 1", active=True)
        data = {"title": "Anuncio 1", "abstract": "Resumen 1", "body": "Descripcion 1",
                                      "url": "https://www.google.com", "section_id": section.id}
        response = self.client.post(
            '/information/advertisements/', data=data)
        self.assertEqual(response.status_code, 201)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)

    def test_create_negative_advertisement_status_CONFLICT(self):
        section = Section.objects.create(name="Seccion 1", active=True)
        Advertisement.objects.create(
            title="Anuncio 1", abstract="Resumen 1", body="Descripcion 1", url="https://www.google.com", section=section)
        data = {"title": "Anuncio 1", "abstract": "Resumen 1", "body": "Descripcion 1",
                "url": "https://www.google.com", "section_id": section.id}
        response = self.client.post(
            '/information/advertisements/', data=data)
        self.assertEqual(response.status_code, 409)
        dataMessage = {
            "error": "This title's advertisement was added into the page, please create another different"}
        self.assertEqual(response.data, dataMessage)

    def test_create_negative_advertisement_section_NOT_FOUND(self):
        data = {"title": "Anuncio 1", "abstract": "Resumen 1", "body": "Descripcion 1",
                "url": "https://www.google.com", "section_id": 1}
        response = self.client.post(
            '/information/advertisements/', data=data)
        self.assertEqual(response.status_code, 404)
        dataMessage = {'message': 'Section not found'}
        self.assertEqual(response.data, dataMessage)

    ################################################## PUTS ##################################################

    def test_update_positive_advertisement_status_OK(self):
        section = Section.objects.create(name="Seccion 1", active=True)
        advertisement = Advertisement.objects.create(
            title="Anuncio 1", abstract="Resumen 1", body="Descripcion 1", url="https://www.google.com", section=section)

        data = {"title": "Anuncio 2", "abstract": "Resumen 2", "body": "Descripcion 2",
                "url": "https://www.google.com", "section_id": section.id}
        response = self.client.put(
            f'/information/advertisements/{advertisement.id}', data=data)
        self.assertEqual(response.status_code, 200)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)

    def test_update_negative_advertisement_status_CONFLICT(self):
        section = Section.objects.create(name="Seccion 1", active=True)
        Advertisement.objects.create(
            title="Anuncio 1", abstract="Resumen 1", body="Descripcion 1", url="https://www.google.com", section=section)

        advertisement = Advertisement.objects.create(
            title="Anuncio 2", abstract="Resumen 1", body="Descripcion 1", url="https://www.google.com", section=section)
        data = {"title": "Anuncio 1", "abstract": "Resumen 2", "body": "Descripcion 2",
                "url": "https://www.google.com", "section_id": section.id}
        response = self.client.put(
            f'/information/advertisements/{advertisement.id}', data=data)
        self.assertEqual(response.status_code, 409)
        dataMessage = {
            "error": "This title's advertisement was added into the page, please select another different"}
        self.assertEqual(response.data, dataMessage)

    def test_update_negative_advertisement_NOT_FOUND(self):
        section = Section.objects.create(name="Seccion 1", active=True)
        data = {"title": "Anuncio 2", "abstract": "Resumen 2", "body": "Descripcion 2",
                "url": "https://www.google.com", "section_id": section.id}
        response = self.client.put(
            f'/information/advertisements/1', data=data)
        self.assertEqual(response.status_code, 404)
        dataMessage = {'message': 'Advertisement not found'}
        self.assertEqual(response.data, dataMessage)

    ################################################## DELETES ##################################################

    def test_delete_positive_advertisement_status_OK(self):
        section = Section.objects.create(name="Seccion 1", active=True)
        advertisement = Advertisement.objects.create(
            title="Anuncio 1", abstract="Resumen 1", body="Descripcion 1", url="https://www.google.com", section=section)
        response = self.client.delete(
            f'/information/advertisements/{advertisement.id}')
        self.assertEqual(response.status_code, 200)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)

    def test_delete_negative_advertisement_status_NOT_FOUND(self):
        response = self.client.delete('/information/advertisements/1')
        self.assertEqual(response.status_code, 404)
        dataMessage = {'message': 'Advertisement not found'}
        self.assertEqual(response.data, dataMessage)


class MultimediaTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="ispp", 
            password="ispp"
        )
        self.client.force_authenticate(user=self.user)

    ################################################## GETS ##################################################

    def test_list_multimedia_status_OK(self):
        section = Section.objects.create(name="Seccion 1", active=True)
        advertisement = Advertisement.objects.create(
            title="Anuncio 1", abstract="Resumen 1", body="Descripcion 1", url="https://www.google.com", section=section)
        Multimedia.objects.create(
            advertisement=advertisement)
        response = self.client.get('/information/multimedias/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_list_multimedia_status_NOT_FOUND(self):
        response = self.client.get('/information/multimedias/')
        self.assertEqual(response.status_code, 404)
        dataMessage = {"message": "multimedias not found..."}
        self.assertEqual(response.data, dataMessage)

    def test_show_multimedia_status_OK(self):
        section = Section.objects.create(name="Seccion 1", active=True)
        advertisement = Advertisement.objects.create(
            title="Anuncio 1", abstract="Resumen 1", body="Descripcion 1", url="https://www.google.com", section=section)
        multimedia = Multimedia.objects.create(
            advertisement=advertisement)
        response = self.client.get(
            f'/information/multimedias/{multimedia.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], multimedia.id)

    def test_show_multimedia_status_NOT_FOUND(self):
        response = self.client.get('/information/multimedias/1')
        self.assertEqual(response.status_code, 404)
        dataMessage = {"message": "multimedia not found..."}
        self.assertEqual(response.data, dataMessage)

    ################################################## POSTS ##################################################

    def test_create_positive_multimedia_status_OK(self):
        section = Section.objects.create(name="Seccion 1", active=True)
        advertisement = Advertisement.objects.create(
            title="Anuncio 1", abstract="Resumen 1", body="Descripcion 1", url="https://www.google.com", section=section)
        data = JSONRenderer().render(
            {"advertisement_id": advertisement.id, "multimedia": "", "description": ""}).decode('utf-8')
        response = self.client.post(
            '/information/multimedias/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)

    def test_create_negative_multimedia_advertisement_NOT_FOUND(self):
        data = JSONRenderer().render(
            {"advertisement_id": 1, "multimedia": "", "description": ""}).decode('utf-8')
        response = self.client.post(
            '/information/multimedias/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        dataMessage = {'message': 'Advertisements not found'}
        self.assertEqual(response.data, dataMessage)

    ################################################## PUTS ##################################################

    def test_update_positive_multimedia_status_OK(self):
        section = Section.objects.create(name="Seccion 1", active=True)
        advertisement = Advertisement.objects.create(
            title="Anuncio 1", abstract="Resumen 1", body="Descripcion 1", url="https://www.google.com", section=section)
        multimedia = Multimedia.objects.create(
            advertisement=advertisement)
        data = JSONRenderer().render(
            {"advertisement_id": advertisement.id, "multimedia": "", "description": "como funcione me corto las venas"}).decode('utf-8')
        response = self.client.put(
            f'/information/multimedias/{multimedia.id}', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)

    def test_update_negative_multimedia_advertisement_NOT_FOUND(self):
        section = Section.objects.create(name="Seccion 1", active=True)
        advertisement = Advertisement.objects.create(
            title="Anuncio 1", abstract="Resumen 1", body="Descripcion 1", url="https://www.google.com", section=section)
        multimedia = Multimedia.objects.create(
            advertisement=advertisement)
        data = JSONRenderer().render(
            {"advertisement_id": 1, "multimedia": "", "description": "como funcione me corto las venas"}).decode('utf-8')
        response = self.client.put(
            f'/information/multimedias/{multimedia.id}', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        dataMessage = {'message': 'Advertisement not found...'}
        self.assertEqual(response.data, dataMessage)

    def test_update_negative_multimedia_status_NOT_FOUND(self):
        data = JSONRenderer().render(
            {"advertisement_id": 1, "multimedia": "", "description": "como funcione me corto las venas"}).decode('utf-8')
        response = self.client.put(
            f'/information/multimedias/1', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        dataMessage = {'message': 'Multimedia not found...'}
        self.assertEqual(response.data, dataMessage)

    ################################################## DELETES ##################################################

    def test_delete_positive_multimedia_status_OK(self):
        section = Section.objects.create(name="Seccion 1", active=True)
        advertisement = Advertisement.objects.create(
            title="Anuncio 1", abstract="Resumen 1", body="Descripcion 1", url="https://www.google.com", section=section)
        multimedia = Multimedia.objects.create(
            advertisement=advertisement)
        response = self.client.delete(
            f'/information/multimedias/{multimedia.id}')
        self.assertEqual(response.status_code, 204)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)

    def test_delete_negative_multimedia_status_NOT_FOUND(self):
        response = self.client.delete(
            f'/information/multimedias/1')
        self.assertEqual(response.status_code, 404)
        dataMessage = {'message': 'Multimedia not found...'}
        self.assertEqual(response.data, dataMessage)


class AdvertisementSectionTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="ispp", 
            password="ispp"
        )
        self.client.force_authenticate(user=self.user)

    def test_show_advertisement_section_status_OK(self):
        section = Section.objects.create(name="Seccion 1", active=True)
        Advertisement.objects.create(
            title="Anuncio 1", abstract="Resumen 1", body="Descripcion 1", url="https://www.google.com", section=section)
        response = self.client.get(
            f'/information/sections/{section.id}/advertisements/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['title'], "Anuncio 1")

    def test_show_advertisement_section_status_NOT_FOUND(self):
        response = self.client.get(
            f'/information/sections/1/advertisements/')
        self.assertEqual(response.status_code, 404)
        dataMessage = {"message": "Section not found"}
        self.assertEqual(response.data, dataMessage)
