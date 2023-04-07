from django.http import HttpResponse
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString 
import json
from django.forms import ValidationError
from .validators import validate_date, validate_dni, validate_iban, validate_name, validate_last_name, validate_dni_blank,validate_phone1,validate_birthdate,validate_address,validate_account_holder,validate_iban_blank,validate_language,validate_postal_code,validate_province,validate_township,validate_sex,validate_state
from rest_framework import views
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK as ST_200,
    HTTP_201_CREATED as ST_201,
    HTTP_404_NOT_FOUND as ST_404,
    HTTP_409_CONFLICT as ST_409,
)
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.http.response import JsonResponse
from .models import Partners, Donation, Communication, CSVFile
from datetime import datetime,date
from .validators import *
import csv
from os import remove
from rest_framework.permissions import IsAdminUser
from django.contrib.admin.views.decorators import staff_member_required

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

    permission_classes = [IsAdminUser]

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

    permission_classes = [IsAdminUser]

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, partner_id):
        partner = Partners.objects.get(id=partner_id)
        if partner_id > 0:
            donation = list(Donation.objects.filter(partner=partner).values())
            if len(donation) > 0:
                donation = donation[0]
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

        date_str = jd['start_date']
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        year = jd['year']
        year = datetime.datetime.strptime(year, '%Y').date()
        Donation.objects.create(partner=partner, start_date=date,
                                amount=amount, periodicity=periodicity, year=year)
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


    def put(self, request, partner_id):
        jd = json.loads(request.body)
        amount = jd['amount']
        periodicity = jd['periodicity']
        
        try:
            partner = Partners.objects.get(id=partner_id, state='Activo')
        except Partners.DoesNotExist:
            datos = {'message': "Partner not found or not active"}
            return JsonResponse(datos, status=400)
        
        try:
            donation = Donation.objects.filter(partner=partner).latest('start_date')
        except Donation.DoesNotExist:
            datos = {'message': "Donation not found..."}
            return JsonResponse(datos)

        donation.amount = amount
        donation.periodicity = periodicity
        donation.save()
        datos = {'message': "Success"}
        return JsonResponse(datos)

    
def get_don_part(request, partner_id):
    partner = Partners.objects.get(id=partner_id, state='Activo')
    donation = Donation.objects.filter(partner=partner)
    datos = list(donation.values())[0]
    return JsonResponse(datos, safe=False)

class CommunicationView(View):

    permission_classes = [IsAdminUser]
    
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

    permission_classes = [IsAdminUser]

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    @method_decorator(login_required)
    def post(self, request):
        try:
            file=request.FILES["selectedFile"]
        except Exception as e:
            error = {'error': "Se debe adjuntar un archivo"}
            return Response(data=error, status=ST_409)

        obj=CSVFile.objects.create(file=file)
        path = "media/"+str(obj.file)
        partners_id_list=[]
        donation_id_list=[]
        try:
            with open(path) as csvFile:
                csvReader=csv.DictReader(csvFile,delimiter=";")
                contador_filas=2
                for jd in csvReader:
                    if jd['Idioma']=='Español':
                        jd['Idioma']='spanish'
                    
                    if jd['Idioma']=='Catalán':
                        jd['Idioma']='catalan'

                    if jd['Sexo']=='Hombre':
                        jd['Sexo']='men'

                    if jd['Sexo']=='Mujer':
                        jd['Sexo']='women'

                    if jd['Sexo']=='Ninguno':
                        jd['Sexo']='none'

                    if jd['Situación (Alta/Baja)']=='Alta':
                        jd['Situación (Alta/Baja)']='Activo'

                    if jd['Situación (Alta/Baja)']=='Baja':
                        jd['Situación (Alta/Baja)']='Inactivo'
                    
                    if "/" in jd['Fch Nac.']:
                        fecha=jd['Fch Nac.'].split("/")
                        jd['Fch Nac.']=fecha[2]+'-'+fecha[1]+'-'+fecha[0]

                    try:
                        partner=Partners.objects.filter(id=jd['Nº Soc'])
                        if len(partner)>0:
                            raise ValidationError('El numero de socio esta duplicado')
                        validate_dni(jd['DNI'])
                        validate_iban(jd['CCC IBAN'])
                        validate_date(jd['Fch Nac.'])
                        validate_name(jd['Nombre'])
                        validate_last_name(jd['Apellidos'])
                        validate_dni_blank(jd['DNI'])
                        validate_phone1(jd['Tfn. 1'])
                        validate_birthdate(jd['Fch Nac.'])
                        validate_address(jd['Dirección Postal, nº - CP'])
                        validate_postal_code(jd['CP'])
                        validate_township(jd['Municipio'])
                        validate_province(jd['Provincia'])
                        validate_language(jd['Idioma'])
                        validate_iban_blank(jd['CCC IBAN'])
                        validate_account_holder(jd['Titular de la cuenta'])
                        validate_state(jd['Situación (Alta/Baja)'])
                        validate_sex(jd['Sexo'])
                        validate_periodicity(jd['Periodicidad'])
                        validate_amount(jd[' Importe '])

                    except ValidationError as e:
                        csvFile.close()
                        obj.delete()
                        remove(path)
                        for donation_id in donation_id_list:
                            donation=Donation.objects.get(id=donation_id)
                            donation.delete()

                        for partner_id in partners_id_list:
                            partner=Partners.objects.get(id=partner_id)
                            partner.delete()
                        error = {'error': e.message + ", este error se ha dado en la fila " + str(contador_filas) + " del fichero csv."}
                        return Response(data=error, status=ST_409)
                    
                    except KeyError as e:
                        csvFile.close()
                        obj.delete()
                        remove(path)
                        for donation_id in donation_id_list:
                            donation=Donation.objects.get(id=donation_id)
                            donation.delete()

                        for partner_id in partners_id_list:
                            partner=Partners.objects.get(id=partner_id)
                            partner.delete()
                        error = {'error': "El fichero csv no es correcto"}
                        return Response(data=error, status=ST_409)
                        
                    try:
                        new_partner=Partners.objects.create(id=jd['Nº Soc'],name=jd['Nombre'], last_name=jd['Apellidos'],
                        dni=jd['DNI'], phone1=jd['Tfn. 1'], phone2=jd['Tfn. 2'], birthdate=jd['Fch Nac.'], sex=jd['Sexo'],
                        email=jd['Email'], address=jd['Dirección Postal, nº - CP'], postal_code=jd['CP'], township=jd['Municipio'],
                        province=jd['Provincia'], language=jd['Idioma'], iban=jd['CCC IBAN'],  account_holder=jd['Titular de la cuenta'],
                        state=jd['Situación (Alta/Baja)'])
                        partners_id_list.append(new_partner.id)

                        new_donation=Donation.objects.create(partner=new_partner,date=date.today(),amount=jd[' Importe '],periodicity=jd['Periodicidad'])
                        donation_id_list.append(new_donation.id)


                    except IntegrityError:
                    
                        csvFile.close()
                        obj.delete()
                        remove(path)
                        for donation_id in donation_id_list:
                            donation=Donation.objects.get(id=donation_id)
                            donation.delete()
                        
                        for id in partners_id_list:
                            partner=Partners.objects.get(id=id)
                            partner.delete()
                        error = {'error': "Ya hay un socio con algún campo igual que uno ya existente, este error se ha dado en la fila "+ str(contador_filas) + " del fichero csv."}
                        return Response(data=error, status=ST_409)
                    
                    contador_filas=contador_filas+1
        except UnicodeDecodeError as e:
                obj.delete()
                remove(path)
                error = {'error': "El archivo no es válido, solo se admiten ficheros csv."}
                return Response(data=error, status=ST_409)
        csvFile.close()
        obj.delete()
        remove(path)
        datos = {'message': "Success"}
        return JsonResponse(datos)
