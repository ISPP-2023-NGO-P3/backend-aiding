from django.http import HttpResponse
from django.shortcuts import render
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString 
from datetime import datetime
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from .models import Partners, Donation
from django.http import HttpResponseNotFound
from datetime import datetime


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
    amount.text = str(partner.total_donation) + "€"
    receipt.append(amount)

    xml_str=ET.tostring(receipt,'utf-8',short_empty_elements=False)
    return parseString(xml_str).toxml(encoding='utf-8')

    

def download_receipt_xml(request,partner_id):
    try:
        partner=Partners.objects.get(id=partner_id)
        response = HttpResponse(generate_receipt_xml(partner),content_type="application/xml")
        todayDate=datetime.today().strftime('%Y-%m-%d')
        response['Content-Disposition'] = 'attachment; filename ='+ partner.name.replace(" ","") + partner.last_name.replace(" ","") + todayDate  +'RECIBO.xml'
        return response 
    except:
        return HttpResponseNotFound("Socio no encontrado")
        
    

    
    





class PartnerManagement(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, id = 0):
        if (id > 0):
            partners = list(Partners.objects.filter(id=id).values())
            if len(partners) > 0:
                partners = partners[0]
                datos = {'partners': partners}
            else:
                datos = {'message': "partner not found..."}
            return JsonResponse(partners, safe = False)
        else:

            partners = list(Partners.objects.values())
            if len(partners) > 0:
                datos = {'partners': partners}
            else:
                datos = {'message': "partners not found..."}
            return JsonResponse(partners, safe = False)

    def post(self, request):
        jd = json.loads(request.body)

        try:
            Partners.objects.create(name=jd['name'], last_name=jd['last_name'], 
            dni=jd['dni'], phone=jd['phone'], email=jd['email'], province=jd['province'],
            iban=jd['iban'], state=jd['state'])
            datos = {'message': "Success"}
            return JsonResponse(datos)
        except IntegrityError:
            error = {'error': "There is already a partner with a field equal to the one you are trying to add, please check the data."}
            return JsonResponse(error)

    def put(self, request, id):
        jd = json.loads(request.body)
        partners = list(Partners.objects.filter(id=id).values())
        if len(partners) > 0:
            partner = Partners.objects.get(id=id)
            partner.name = jd['name']
            partner.last_name=jd['last_name']
            partner.dni=jd['dni']
            partner.phone=jd['phone']
            partner.email=jd['email']
            partner.province=jd['province']
            partner.iban=jd['iban']
            partner.state=jd['state']
            partner.save()
            datos = {'message': "Success"}
        else:
            datos = {'message': "Partner not found..."}
        return JsonResponse(datos)
    


class DonationView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if id > 0:
            donations = list(Donation.objects.filter(id=id).values())
            if len(donations) > 0:
                donation = donations[0]
                datos = {'donation': donation}
            else:
                datos = {'message': "Donation not found..."}
            return JsonResponse(donation, safe=False)
        else:
            donations = list(Donation.objects.values())
            if len(donations) > 0:
                datos = {'donations': donations}
            else:
                datos = {'message': "Donations not found..."}
            return JsonResponse(donations, safe=False)
        
    def post(self, request):
        jd = json.loads(request.body)
        partner_id = jd['partner_id']
        donation_type = jd['donation_type']
        amount = jd['amount']
        periodicity = jd['periodicity']

        try:
            partner = Partners.objects.get(id=partner_id, state='ACTIVE')
        except Partners.DoesNotExist:
            datos = {'message': "Partner not found or not active"}
            return JsonResponse(datos, status=400)

        date_str = jd['date']
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        Donation.objects.create(partner=partner, date=date, donation_type=donation_type,
                                amount=amount, periodicity=periodicity)

        datos = {'message': "Success"}
        return JsonResponse(datos)

    
    def put(self, request, id):
        jd = json.loads(request.body)
        donations = list(Donation.objects.filter(id=id).values())
        if len(donations) > 0:
            partner =Partners.objects.filter(id = jd['partner_id'])
            partner = partner[0]
            donation = Donation.objects.get(id=id)
            donation.partner = partner
            donation.periodicity = jd['periodicity']
            donation.save()
            datos = {'message': "Success"}
        else:
            datos = {'message': "Donation not found..."}
        return JsonResponse(datos)
    
    def delete(self, request, id):
        try:
            donation = Donation.objects.get(id=id)
            donation.delete()
            datos = {'message': "Success"}
        except Donation.DoesNotExist:
            datos = {'message': "Donation not found..."}
        return JsonResponse(datos)


