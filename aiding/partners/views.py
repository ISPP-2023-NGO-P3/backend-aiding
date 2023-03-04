from django.http import HttpResponse
from django.shortcuts import render
import xml.etree.ElementTree as ET

from xml.dom.minidom import parseString 




def generate_receipt_xml(donation_id):
    receipt = ET.Element("Recibo")
    donator = ET.Element("donante")
    receipt.append(donator)

    name = ET.SubElement(donator,"nombre")
    name.text="Jose Luis"
    surname = ET.SubElement(donator,"apellido")
    surname.text = "Perez Garciaa"
    dni = ET.SubElement(donator,"dni")
    dni.text = "666669694S"

    iban = ET.Element("IBAN")
    iban.text = "243432223442342PA"
    receipt.append(iban)

    concept = ET.Element("concepto")
    concept.text = "Cuota Bosco Global"
    receipt.append(concept)

    amount = ET.Element("importe")
    amount.text = "456 €"
    receipt.append(amount)

    xml_str=ET.tostring(receipt,'utf-8',short_empty_elements=False)
    return parseString(xml_str).toxml(encoding='utf-8')

    

def download_receipt_xml(request,donation_id):
    response = HttpResponse(generate_receipt_xml(1),content_type="application/xml")
    response['Content-Disposition'] = 'attachment; filename = exampleFile.xml'
    return response




