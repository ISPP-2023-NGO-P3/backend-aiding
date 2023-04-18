import json

from django.db import IntegrityError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required

from rest_framework import views
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK as ST_200
from rest_framework.status import HTTP_201_CREATED as ST_201
from rest_framework.status import HTTP_204_NO_CONTENT as ST_204
from rest_framework.status import HTTP_404_NOT_FOUND as ST_404
from rest_framework.status import HTTP_409_CONFLICT as ST_409

from .models import Item, Type

class CsrfExemptMixin:
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)



class ItemView(CsrfExemptMixin, views.APIView):

    def get(self, request, item_id=0):
        if item_id > 0:
            item = list(Item.objects.filter(id=item_id).values())
            if len(item) > 0:
                item = item[0]
                return Response(data=item, status=ST_200)
            else:
                datos = {"message": "item not found..."}
                return Response(data=datos, status=ST_404)
        else:
            items = list(Item.objects.all().values())
            lenght = len(items)
            if lenght > 0:
                return Response(data=items, status=ST_200)
            else:
                datos = {"message": "items not found..."}
            return Response(data=datos, status=ST_404)

    @method_decorator(staff_member_required)
    def post(self, request):
        jd = json.loads(request.body)
        name = jd["name"]
        description = jd["description"]
        quantity = jd["quantity"]
        try:
            type_id = jd["type_id"]
            try:
                t = Type.objects.get(id=type_id)
                Item.objects.create(name=name,description= description, quantity= quantity, type=t)
                datos = {"message": "Success"}
                return Response(data=datos, status=ST_201)
            except Type.DoesNotExist:
                error = {
                "error": "Type not found"
            }
            return Response(data=error, status=ST_404)
        except IntegrityError:
            error = {
                "error": "This item's name was added into the page, please create another different"
            }
            return Response(data=error, status=ST_409)

    @method_decorator(staff_member_required)
    def put(self, request, item_id):
        jd = json.loads(request.body)        
        type_id = jd["type_id"]
        name = jd["name"]
        description = jd["description"]
        quantity = jd["quantity"]

        items = list(
            Item.objects.filter(id=item_id).values()
        )
        if len(items) > 0:
            t= Type.objects.filter(id=type_id)
            if len(t) > 0:
                t = t[0]
                item = Item.objects.get(id=item_id)
                try:
                    item.name = name
                    item.description = description
                    item.quantity = quantity
                    item.type = t
                    item.save()
                    datos = {"message": "Success"}
                    return Response(data=datos, status=ST_200)
                except IntegrityError:
                    error = {
                        "error": "This name's item was added into the page, please select another different"
                    }
                    return Response(data=error, status=ST_409)
            else:
                datos = {"message": "type not found"}
                return Response(data=datos, status=ST_404)
        else:
            datos = {"message": "Item not found"}
            return Response(data=datos, status=ST_404)

    @method_decorator(staff_member_required)
    def delete(self, request, item_id):
        items = list(
            Item.objects.filter(id=item_id).values()
        )
        if len(items) > 0:
            Item.objects.filter(id=item_id).delete()
            datos = {"message": "Success"}
            return Response(data=datos, status=ST_200)
        else:
            datos = {"message": "Item not found"}
            return Response(data=datos, status=ST_404)

class TypeView(CsrfExemptMixin, views.APIView):

    def get(self, request, type_id=0):
        if type_id > 0:
            t = list(Type.objects.filter(id=type_id).values())
            if len(t) > 0:
                t = t[0]
                return Response(data=t, status=ST_200)
            else:
                datos = {"message": "type not found..."}
                return Response(data=datos, status=ST_404)
        else:
            types = list(Type.objects.all().values())
            lenght = len(types)
            if lenght > 0:
                return Response(data=types, status=ST_200)
            else:
                datos = {"message": "types not found..."}
            return Response(data=datos, status=ST_404)

    @method_decorator(staff_member_required)
    def post(self, request):
        name = request.data["name"]

        try:
            Type.objects.create(name=name)
            datos = {"message": "Success"}
            return Response(data=datos, status=ST_201)
        except IntegrityError:
            error = {
                "error": "This type was added into the page, please create another different"
            }
            return Response(data=error, status=ST_409)

    @method_decorator(staff_member_required)
    def put(self, request, type_id):
        jd = json.loads(request.body)
        types = list(Type.objects.filter(id=type_id).values())
        if len(types) > 0:
            types = Type.objects.get(id=type_id)
            try:
                types.name = jd["name"]
                types.save()
                datos = {"message": "Success"}
                return Response(data=datos, status=ST_200)
            except IntegrityError:
                error = {
                    "error": "This type was added into the page, please select another different"
                }
                return Response(data=error, status=ST_409)
        else:
            datos = {"message": "Type not found..."}
        return Response(data=datos, status=ST_404)

    @method_decorator(staff_member_required)
    def delete(self, request, type_id):
        types = list(Type.objects.filter(id=type_id).values())
        if len(types) > 0:
            Type.objects.filter(id=type_id).delete()
            datos = {"message": "Success"}
            return Response(data=datos, status=ST_204)
        else:
            datos = {"message": "Type not found..."}
            return Response(data=datos, status=ST_404)



