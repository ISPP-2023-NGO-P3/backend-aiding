from django.http import HttpResponse
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString 
import json
from django.forms import ValidationError
from .validators import validate_date, validate_dni, validate_iban
from rest_framework import views
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK as ST_200,
    HTTP_201_CREATED as ST_201,
    HTTP_404_NOT_FOUND as ST_404,
    HTTP_409_CONFLICT as ST_409,
)
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.http.response import JsonResponse
from .models import Partners, Donation, Communication, CSVFile
from datetime import datetime
from .validators import *
import csv

def generate_receipt_xml(partner):
    receipt = ET.Element("Recibo")
    donator = ET.Element("donante")
    receipt.append(donator)

    name = ET.SubElement(donator,"nombre")
    name.text=partner.name
    surname = ET.SubElement(donator,"apellido")
    surname.text = partner.last_name
    dni = ET.SubElement(donator,"dni")
    dni.text = partner.dni

    iban = ET.Element("IBAN")
    iban.text = partner.iban
    receipt.append(iban)

    concept = ET.Element("concepto")
    concept.text = "Cuota Bosco Global"
    receipt.append(concept)

    amount = ET.Element("importe")
    amount.text = "placeholder" #str(donation.total_donation()) +"€"
    receipt.append(amount)

    xml_str=ET.tostring(receipt,'utf-8',short_empty_elements=False)
    return parseString(xml_str).toxml(encoding='utf-8')

def download_receipt_xml(request,partner_id):
    try:
        partner=Partners.objects.get(id=partner_id)
        response = HttpResponse(generate_receipt_xml(partner),content_type="application/xml")
        todayDate=datetime.datetime.today().strftime('%Y-%m-%d')
        response['Content-Disposition'] = 'attachment; filename ='+ partner.name.replace(" ","") + partner.last_name.replace(" ","") + '_'+todayDate  +'_RECIBO.xml'
        return response
    except Exception:
        return HttpResponse(status=404)

class PartnerManagement(views.APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, partner_id = 0):
        if (partner_id > 0):
            partners = list(Partners.objects.filter(id=partner_id).values())
            if len(partners) > 0:
                partners = partners[0]
                return Response(data=partners, status=ST_200)
            else:
                datos = {'message': "partner not found..."}
            return Response(data=datos, status=ST_404)
        else:
            partners = list(Partners.objects.values())
            if len(partners) > 0:
                datos = {'partners': partners}
                return Response(data=partners, status=ST_200)
            else:
                datos = {'message': "partners not found..."}
            return Response(data=datos, status=ST_404)
  
    def post(self, request):
        jd = json.loads(request.body)

        try:
            validate_dni(jd['dni'])
            validate_iban(jd['iban'])
            validate_date(jd['birthdate'])
        except ValidationError as e:
            error = {'error': e.message}
            return Response(data=error, status=ST_409)

        try:
            Partners.objects.create(name=jd['name'], last_name=jd['last_name'],
            dni=jd['dni'], phone1=jd['phone1'], phone2=jd['phone2'], birthdate=jd['birthdate'], sex=jd['sex'],
            email=jd['email'], address=jd['address'], postal_code=jd['postal_code'], township=jd['township'],
            province=jd['province'], language=jd['language'], iban=jd['iban'],  account_holder=jd['account_holder'],
            state=jd['state'])
            datos = {'message': "Success"}
            return Response(data=datos, status=ST_201)
        except IntegrityError:
            error = {'error': "There is already a partner with a field equal to the one you are trying to add, please check the data."}
            return Response(data=error, status=ST_409)

    def put(self, request, partner_id):
        jd = json.loads(request.body)
        partners = list(Partners.objects.filter(id=partner_id).values())
        if len(partners) > 0:
            partner = Partners.objects.get(id=partner_id)
            try:
                validate_dni(jd['dni'])
                validate_iban(jd['iban'])
                validate_date(jd['birthdate'])
            except ValidationError as e:
                error = {'error': e.message}
                return Response(data=error, status=ST_409)
            try:
                partner.name = jd['name']
                partner.last_name=jd['last_name']
                partner.dni=jd['dni']
                partner.phone1=jd['phone1']
                partner.phone2=jd['phone2']
                partner.birthdate=jd['birthdate']
                partner.sex=jd['sex']
                partner.address=jd['address']
                partner.postal_code=jd['postal_code']
                partner.township=jd['township']
                partner.email=jd['email']
                partner.province=jd['province']
                partner.language=jd['language']
                partner.iban=jd['iban']
                partner.account_holder=jd['account_holder']
                partner.state=jd['state']
                partner.save()
                datos = {'message': "Success"}
                return Response(data=datos, status=ST_200)
            except IntegrityError:
                error = {'error': "There is already a partner with a field equal to the one you are trying to add, please check the data."}
                return Response(data=error, status=ST_409)

        else:
            datos = {'message': "Partner not found..."}
        return Response(data=error, status=ST_409)
    
class DonationView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, partner_id):
        partner = Partners.objects.get(id=partner_id)
        if partner_id > 0:
            donations = list(Donation.objects.filter(partner=partner).values())
            if len(donations) > 0:
                donation = donations[0]
            return JsonResponse(donation, safe=False)
        else:
            donations = list(Donation.objects.values())
            return JsonResponse(donations, safe=False)
        
    def post(self, request, partner_id):
        jd = json.loads(request.body)
        amount = jd['amount']
        periodicity = jd['periodicity']

        try:
            partner = Partners.objects.get(id=partner_id, state='Activo')
        except Partners.DoesNotExist:
            datos = {'message': "Partner not found or not active"}
            return JsonResponse(datos, status=400)

        date_str = jd['date']
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        Donation.objects.create(partner=partner, date=date,
                                amount=amount, periodicity=periodicity)
        datos = {'message': "Success"}
        return JsonResponse(datos)
    
    def delete(self, request, partner_id):
        try:
            donation = Donation.objects.get(id=partner_id)
            donation.delete()
            datos = {'message': "Success"}
        except Donation.DoesNotExist:
            datos = {'message': "Donation not found..."}
        return JsonResponse(datos)
    
def get_don_part(request, partner_id):
    partner = Partners.objects.get(id=partner_id, state='Activo')
    donation = Donation.objects.filter(partner=partner)
    datos = list(donation.values())[0]
    return JsonResponse(datos, safe=False)
    
class CommunicationView(View):
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, communication_id=0, partner_id = 0):
        communications = Communication.objects
        if partner_id > 0:
            communications = communications.filter(partner=partner_id)
            if communication_id>0:
                communications = communications.filter(id=communication_id)
            else:
                return JsonResponse(list(communications.values()), safe = False)
        return JsonResponse(list(communications.values()), safe = False)
        
    def post(self, request, partner_id):
        jd = json.loads(request.body)
        part = Partners.objects.filter(id = partner_id)
        if len(part) >0:
            part = part[0]
            date = jd['date']
            communication_type=jd['communication_type']
            description = jd['description']

            Communication.objects.create(partner=part, date=date,
                                            communication_type=communication_type, description =description)

            data = {'message': 'Success'}
        else:
            data = {'message': 'Partner not found'}
        return JsonResponse(data)
        
    def put(self, request, communication_id, partner_id):
        jd = json.loads(request.body)
        communications = Communication.objects.filter(id=communication_id)
        if len(list(communications.values())) > 0:
            part = Partners.objects.filter(id = partner_id)
            if len(part) > 0:
                part = part[0]
                communication = Communication.objects.get(id=communication_id)
                communication.partner = part
                communication.date = jd['date']
                communication.communication_type = jd['communication_type']
                communication.description = jd['description']
                communication.save()
                datos = {'message': "Success"}
            else:
                datos = {'message': "Partner not found..."}
        else:
            datos = {'message': "Communication not found..."}
        return JsonResponse(datos)
        
    def delete(self, request, communication_id, partner_id):
        communications = Communication.objects.filter(partner=partner_id)
        if len(list(communications.values())) > 0:
            communications = communications.filter(id=communication_id)
            if len(list(communications.values())) > 0:
                communications.delete()
                data = {'message': 'Success'}
            else:
                data = {'message': 'Communication not found...'}
        else:
            data = {'message': 'Partner not found...'}
        return JsonResponse(data)

class ImportCSVView(views.APIView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request):
        file=request.FILES["selectedFile"]
        obj=CSVFile.objects.create(file=file)
        path = str(obj.file)
        with open(path) as csvFile:
            csvReader=csv.DictReader(csvFile,delimiter=";")
            for jd in csvReader:
                
                try:
                    validate_dni(jd['dni'])
                    validate_iban(jd['iban'])
                    validate_date(jd['birthdate'])
                except ValidationError as e:
                    obj.delete()
                    error = {'error': e.message}
                    return Response(data=error, status=ST_409)
                try:
                    Partners.objects.create(name=jd['ï»¿name'], last_name=jd['last_name'],
                    dni=jd['dni'], phone1=jd['phone1'], phone2=jd['phone2'], birthdate=jd['birthdate'], sex=jd['sex'],
                    email=jd['email'], address=jd['address'], postal_code=jd['postal_code'], township=jd['township'],
                    province=jd['province'], language=jd['language'], iban=jd['iban'],  account_holder=jd['account_holder'],
                    state=jd['state']) 

                except IntegrityError:
                    obj.delete()
                    error = {'error': "There is already a partner with a field equal to the one you are trying to add, please check the data."}
                    return Response(data=error, status=ST_409)
        obj.delete()
        datos = {'message': "Success"}
        return JsonResponse(datos)
