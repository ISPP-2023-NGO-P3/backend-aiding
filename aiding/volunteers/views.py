from rest_framework import views
import json
from django.db import IntegrityError
from django.forms import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from .models import Volunteer, Turn
from datetime import datetime
from rest_framework.status import HTTP_200_OK as ST_200
from rest_framework.status import HTTP_201_CREATED as ST_201
from rest_framework.status import HTTP_204_NO_CONTENT as ST_204
from rest_framework.status import HTTP_404_NOT_FOUND as ST_404
from rest_framework.status import HTTP_409_CONFLICT as ST_409

from .validators import validate_nif

class VolunteerManagement(views.APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, volunteer_id = 0):
        if (volunteer_id > 0):
            volunteers = list(Volunteer.objects.filter(id=volunteer_id).values())
            if len(volunteers) > 0:
                volunteers = volunteers[0]
                return Response(data=volunteers, status=ST_200)
            else:
                datos = {'message': "Volunteer not found..."}
            return Response(data=datos, status=ST_404)
        else:
            volunteers = list(Volunteer.objects.values())
            if len(volunteers) > 0:
                datos = {'volunteers': volunteers}
                return Response(data=volunteers, status=ST_200)
            else:
                datos = {'message': "Volunteers not found..."}
            return Response(data=datos, status=ST_404)
  
    def post(self, request):
        jd = json.loads(request.body)
        try:
            validate_nif(jd['nif'])
        except ValidationError as e:
            error = {'error': e.message}
            return Response(data=error, status=ST_409)
        try:
            Volunteer.objects.create(name=jd['name'],last_name=jd['last_name'],num_volunteer=jd['num_volunteer'],
                                     nif=jd['nif'],place=jd['place'],phone=jd['phone'],email=jd['email'],
                                     state=jd['state'],situation=jd['situation'],rol=jd['rol'],
                                     observations=jd['observations'],computerKnowledge=jd['computerKnowledge'],
                                     truckKnowledge=jd['truckKnowledge'],warehouseKnowledge=jd['warehouseKnowledge'],
                                     otherKnowledge=jd['otherKnowledge'])
            datos = {'message': "Success"}
            return Response(data=datos, status=ST_201)
        except IntegrityError:
            error = {'error': "There is already a volunteer with a field equal to the one you are trying to add, please check the data."}
            return Response(data=error, status=ST_409)

    def put(self, request, volunteer_id):
        jd = json.loads(request.body)
        volunteers = list(Volunteer.objects.filter(id=volunteer_id).values())
        if len(volunteers) > 0:
            volunteer = Volunteer.objects.get(id=volunteer_id)
            try:
                validate_nif(jd['nif'])
            except ValidationError as e:
                error = {'error': e.message}
                return Response(data=error, status=ST_409)
            try:
                volunteer.name = jd['name']
                volunteer.last_name=jd['last_name']
                volunteer.num_volunteer=jd['num_volunteer']
                volunteer.nif=jd['nif']
                volunteer.place=jd['place']
                volunteer.phone=jd['phone']
                volunteer.email=jd['email']
                volunteer.state=jd['state']
                volunteer.situation=jd['situation']
                volunteer.rol=jd['rol']
                volunteer.observations=jd['observations']
                volunteer.computerKnowledge=jd['computerKnowledge']
                volunteer.truckKnowledge=jd['truckKnowledge']
                volunteer.warehouseKnowledge=jd['warehouseKnowledge']
                volunteer.otherKnowledge=jd['otherKnowledge']
                volunteer.save()
                datos = {'message': "Success"}
                return Response(data=datos, status=ST_200)
            except IntegrityError:
                error = {'error': "There is already a volunteer with a field equal to the one you are trying to add, please check the data."}
                return Response(data=error, status=ST_409)
        else:
            datos = {'error': "Volunteer not found..."}
        return Response(data=datos, status=ST_409)
    
    def delete(self, request, volunteer_id):
        sections = list(Volunteer.objects.filter(id=volunteer_id).values())
        if len(sections) > 0:
            Volunteer.objects.filter(id=volunteer_id).delete()
            datos = {"message": "Successfully deleted"}
            return Response(data=datos, status=ST_204)
        else:
            datos = {"error": "Volunteer not found..."}
            return Response(data=datos, status=ST_404)

class TurnView(views.APIView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        turns = Turn.objects.all()
        datos = []
        for turn in turns:
            volunteers = []
            for volunteer in turn.volunteers.all():
                volunteers.append(volunteer.name)
            datos.append({
                'date': turn.date,
                'startTime': turn.startTime,
                'endTime': turn.endTime,
                'volunteers': volunteers
            })
        return Response(data=datos,status=ST_200)
        

    def post(self,request):
         
        jd = json.loads(request.body)
         
        date_str= jd['date']
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        startTime_str= jd['startTime']
        startTime = datetime.datetime.strptime(startTime_str, '%H:%M').time()
        endTime_str= jd['endTime']
        endTime = datetime.datetime.strptime(endTime_str, '%H:%M').time()
        volunteer_ids = jd['volunteer_ids']

        volunteers = []
        for volunteer_id in volunteer_ids:
            try:
                volunteer = Volunteer.objects.get(id=volunteer_id, state='Activo')
                volunteers.append(volunteer)
            except Volunteer.DoesNotExist:
                datos = {'message': f"Volunteer with id {volunteer_id} not found or not active"}
                return Response(data=datos, status=ST_409)
        
        turn = Turn.objects.create(date=date, startTime=startTime, endTime=endTime)
        turn.volunteer.set(volunteers)

        datos = {'message': "Success"}
        return Response(data=datos, status=ST_201)
    
    def put(self, request, turn_id):

        try:
            turn = Turn.objects.get(id=turn_id)
        except Turn.DoesNotExist:
            datos = {'message': "Turn not found..."}
            return Response(data=datos, status=ST_409)
        
        jd = json.loads(request.body)
        date_str = jd.get('date', None)
        if date_str:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            turn.date = date
        
        start_time_str = jd.get('startTime', None)
        if start_time_str:
            startTime = datetime.strptime(start_time_str, '%H:%M').time()
            turn.startTime = startTime
        
        end_time_str = jd.get('endTime', None)
        if end_time_str:
            endTime = datetime.strptime(end_time_str, '%H:%M').time()
            turn.endTime = endTime
        
        volunteer_id = jd.get('volunteer', None)
        if volunteer_id:
            try:
                volunteer = Volunteer.objects.get(id=volunteer_id, state='Activo')
                turn.volunteer.set([volunteer])
            except Volunteer.DoesNotExist:
                datos = {'message': "Volunteer not found or not active"}
                return Response(data=datos, status=ST_409)
        
        turn.save()
        datos = {'message': "Success"}
        return Response(data=datos, status=ST_200)

    def delete(self, request, turn_id):
        try:
            turn = Turn.objects.get(id=turn_id)
            turn.delete()
            datos = {'message': "Success"}
            return Response(data=datos, status=ST_409)

        except Turn.DoesNotExist:
            datos = {'message': "Turn not found..."}
            return Response(data=datos, status=ST_409)




    

