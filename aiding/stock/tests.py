from .models import Type, Item
from base.models import User
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.renderers import JSONRenderer


class ItemTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="ispp",
            password="ispp"
        )
        self.client.force_authenticate(user=self.user)

######GETS######

    def test_list_item_status_OK(self):
        t=Type.objects.create(name="type1")
        Item.objects.create(name="item1", description="description1", quantity=1, type=t)
        response = self.client.get('/stock/items/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_list_item_status_NO_CONTENT(self):
        response = self.client.get('/stock/items/')
        data = {"message": "items not found..."}
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, data)

    def test_show_positive_item_status_OK(self):
        t=Type.objects.create(name="type1")
        item = Item.objects.create(name="item1", description="description1", quantity=1, type=t)
        response = self.client.get('/stock/items/'+str(item.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "item1")

    def test_show_negative_item_status_NOT_FOUND(self):
        response = self.client.get('/stock/items/1')
        data = {"message": "item not found..."}
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, data)

######POSTS######

    def test_create_item_status_CREATED(self):
        t=Type.objects.create(name="type1")
        data = JSONRenderer().render({"name": "item1", "description": "description1", "quantity": 1, "type_id": t.id})
        response = self.client.post('/stock/items/', data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)
    
    def test_create_item_status_BAD_REQUEST(self):
        data = JSONRenderer().render({"name": "item1", "description": "description1", "quantity": 1, "type_id": 44})
        response = self.client.post('/stock/items/', data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        dataMessage = {'error': 'Type not found'}
        self.assertEqual(response.data, dataMessage)

    def test_create_item_negative_name_status_BAD_REQUEST(self):
        t=Type.objects.create(name="type1")
        Item.objects.create(name="name", description="description1", quantity=1, type=t)
        data = JSONRenderer().render({"name": "name", "description": "description2", "quantity": 1, "type_id": t.id})
        response = self.client.post('/stock/items/', data, content_type='application/json')
        self.assertEqual(response.status_code, 409)
        dataMessage = {'error': "This item's name was added into the page, please create another different"}
        self.assertEqual(response.data, dataMessage)

######PUTS######

    def test_update_item_status_OK(self):
        t=Type.objects.create(name="type1")
        item = Item.objects.create(name="item1", description="description1", quantity=1, type=t)
        data = JSONRenderer().render({"name": "item1", "description": "description1", "quantity": 2, "type_id": t.id})
        response = self.client.put('/stock/items/'+str(item.id), data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)

    def test_update_negative_item_status_NOT_FOUND(self):
        t=Type.objects.create(name="type1")
        data = JSONRenderer().render({"name": "item1", "description": "description1", "quantity": 2, "type_id": t.id})
        response = self.client.put('/stock/items/1', data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        dataMessage = {'message': 'Item not found'}
        self.assertEqual(response.data, dataMessage)

    def test_update_item_negative_name_status_BAD_REQUEST(self):
        t=Type.objects.create(name="type1")
        item = Item.objects.create(name="item1", description="description1", quantity=1, type=t)
        Item.objects.create(name="name", description="description2", quantity=1, type=t)
        data = JSONRenderer().render({"name": "name", "description": "description1", "quantity": 2, "type_id": t.id})
        response = self.client.put('/stock/items/'+str(item.id), data, content_type='application/json')
        self.assertEqual(response.status_code, 409)
        dataMessage = {'error': "This name's item was added into the page, please select another different"}
        self.assertEqual(response.data, dataMessage)
    
    def test_update_item_status_BAD_REQUEST(self):
        t=Type.objects.create(name="type1")
        item = Item.objects.create(name="item1", description="description1", quantity=1, type=t)
        data = JSONRenderer().render({"name": "item1", "description": "description1", "quantity": 2, "type_id": 55})
        response = self.client.put('/stock/items/'+str(item.id), data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        dataMessage = {'message': 'type not found'}
        self.assertEqual(response.data, dataMessage)

######DELETES######

    def test_delete_item_status_OK(self):
        t=Type.objects.create(name="type1")
        item = Item.objects.create(name="item1", description="description1", quantity=1, type=t)
        response = self.client.delete('/stock/items/'+str(item.id))
        self.assertEqual(response.status_code, 200)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)

    def test_delete_negative_item_status_NOT_FOUND(self):
        response = self.client.delete('/stock/items/1')
        self.assertEqual(response.status_code, 404)
        dataMessage = {'message': 'Item not found'}
        self.assertEqual(response.data, dataMessage)

class TypeTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="ispp",
            password="ispp"
        )
        self.client.force_authenticate(user=self.user)

######GETS######

    def test_show_type_status_OK(self):
        t=Type.objects.create(name="type1")
        response = self.client.get('/stock/types/'+str(t.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "type1")

    def test_show_negative_type_status_NOT_FOUND(self):
        response = self.client.get('/stock/types/1')
        self.assertEqual(response.status_code, 404)
        dataMessage = {'message': 'type not found...'}
        self.assertEqual(response.data, dataMessage)

    def test_show_all_types_status_OK(self):
        Type.objects.create(name="type1")
        Type.objects.create(name="type2")
        response = self.client.get('/stock/types/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_show_all_types_status_NO_CONTENT(self):
        response = self.client.get('/stock/types/')
        self.assertEqual(response.status_code, 404)
        dataMessage = {'message': 'types not found...'}
        self.assertEqual(response.data, dataMessage)

######POSTS######

    def test_create_type_status_OK(self):
        data = JSONRenderer().render({"name": "type1"})
        response = self.client.post('/stock/types/', data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)

    def test_create_negative_type_status_BAD_REQUEST(self):
        Type.objects.create(name="type1")
        data = JSONRenderer().render({"name": "type1"})
        response = self.client.post('/stock/types/', data, content_type='application/json')
        self.assertEqual(response.status_code, 409)
        dataMessage = {'error': 'This type was added into the page, please create another different'}
        self.assertEqual(response.data, dataMessage)

######PUTS######

    def test_update_type_status_OK(self):
        t=Type.objects.create(name="type1")
        data = JSONRenderer().render({"name": "type2"})
        response = self.client.put('/stock/types/'+str(t.id), data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)

    def test_update_negative_type_status_NOT_FOUND(self):
        data = JSONRenderer().render({"name": "type2"})
        response = self.client.put('/stock/types/1', data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        dataMessage = {'message': 'Type not found...'}
        self.assertEqual(response.data, dataMessage)

    def test_update_type_negative_name_status_BAD_REQUEST(self):
        t=Type.objects.create(name="type1")
        Type.objects.create(name="type2")
        data = JSONRenderer().render({"name": "type2"})
        response = self.client.put('/stock/types/'+str(t.id), data, content_type='application/json')
        self.assertEqual(response.status_code, 409)
        dataMessage = {'error': 'This type was added into the page, please select another different'}
        self.assertEqual(response.data, dataMessage)

######DELETES######

    def test_delete_type_status_OK(self):
        t=Type.objects.create(name="type1")
        response = self.client.delete('/stock/types/'+str(t.id))
        self.assertEqual(response.status_code, 204)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)

    def test_delete_negative_type_status_NOT_FOUND(self):
        response = self.client.delete('/stock/types/1')
        self.assertEqual(response.status_code, 404)
        dataMessage = {'message': 'Type not found...'}
        self.assertEqual(response.data, dataMessage)

class IntegrationTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="ispp",
            password="ispp"
        )
        self.client.force_authenticate(user=self.user)

    def test_positive_create_type_and_item(self):
        #Se crea un tipo
        type_data = JSONRenderer().render({"name":"tipoPrueba"})
        response = self.client.post(
            '/stock/types/', data=type_data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        dataMessage = {"message": "Success"}
        self.assertEqual(response.data, dataMessage)

        type_test=Type.objects.get(name="tipoPrueba")

        #Se crea un item
        item_data = JSONRenderer().render({"name": "itemPrueba", "description": "descripcionPrueba", "quantity": 1, 
                                      "type_id": type_test.id})
        response = self.client.post('/stock/items/', item_data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        dataMessage = {'message': 'Success'}
        self.assertEqual(response.data, dataMessage)

        item_test = Item.objects.get(name="itemPrueba")

        #Se muestra la lista de tipos
        response = self.client.get(f'/stock/types/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        #Se muestra el item creado
        response = self.client.get(f'/stock/items/{item_test.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("name"), "itemPrueba")