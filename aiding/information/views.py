from django.db import IntegrityError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Section, Advertisement, Multimedia
import json

from rest_framework import views
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED as ST_201,
    HTTP_404_NOT_FOUND as ST_404,
    HTTP_409_CONFLICT as ST_409,
    HTTP_204_NO_CONTENT as ST_204,
    HTTP_200_OK as ST_200
)

# Create your views here.


class SectionView(views.APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if (id > 0):
            section = list(Section.objects.filter(id=id).values())
            if len(section) > 0:
                section = section[0]
                return Response(data=section, status=ST_200)
            else:
                datos = {'message': "section not found..."}
                return Response(data=datos, status=ST_404)
        else:
            sections = list(Section.objects.filter(active=True).values())
            lenght = len(sections)
            if lenght > 0:
                sections = sections[lenght-2:lenght]
                return Response(data=sections, status=ST_200)
            else:
                datos = {'message': "sections not found..."}
                return Response(data=datos, status=ST_404)

    def post(self, request):
        jd = json.loads(request.body)
        try:
            Section.objects.create(name=jd['name'], active=jd['active'])
            datos = {'message': "Success"}
            return Response(data=datos, status=ST_201)
        except IntegrityError:
            error = {
                'error': "This section was added into the page, please create another different"}
            return Response(data=error, status=ST_409)

    def put(self, request, id):
        jd = json.loads(request.body)
        sections = list(Section.objects.filter(id=id).values())
        if len(sections) > 0:
            section = Section.objects.get(id=id)
            try:
                section.name = jd['name']
                section.active = jd['active']
                section.save()
                datos = {'message': "Success"}
                return Response(data=datos, status=ST_200)
            except IntegrityError:
                error = {
                    'error': "This section was added into the page, please select another different"}
                return Response(data=error, status=ST_409)
        else:
            datos = {'message': "Section not found..."}
            return Response(data=datos, status=ST_404)

    def delete(self, request, id):
        sections = list(Section.objects.filter(id=id).values())
        if len(sections) > 0:
            Section.objects.filter(id=id).delete()
            datos = {'message': "Success"}
            return Response(data=datos, status=ST_204)
        else:
            datos = {'message': "Section not found..."}
            return Response(data=datos, status=ST_404)

############################################################################################################


class MultimediaView(views.APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if (id > 0):
            multimedia = list(Multimedia.objects.filter(id=id).values())
            if len(multimedia) > 0:
                multimedia = multimedia[0]
                return Response(data=multimedia, status=ST_200)
            else:
                datos = {'message': "multimedia not found..."}
                return Response(data=datos, status=ST_404)
        else:
            multimedias = list(Multimedia.objects.values())
            if len(multimedias) > 0:
                return Response(data=multimedias, status=ST_200)
            else:
                datos = {'message': "multimedias not found..."}
                return Response(data=datos, status=ST_404)

    def post(self, request):
        jd = json.loads(request.body)
        adv = Advertisement.objects.filter(id=jd['advertisement_id'])
        if len(adv) > 0:
            adv = adv[0]
            Multimedia.objects.create(
                advertisement=adv, multimedia=jd['multimedia'], description=jd['description'])
            datos = {'message': "Success"}
            return Response(data=datos, status=ST_201)
        else:
            datos = {'message': "Advertisements not found"}
            return Response(data=datos, status=ST_404)

    def put(self, request, id):
        jd = json.loads(request.body)
        multimedias = list(Multimedia.objects.filter(id=id).values())
        if len(multimedias) > 0:
            adv = Advertisement.objects.filter(id=jd['advertisement_id'])
            if len(adv) > 0:
                adv = adv[0]
                multimedia = Multimedia.objects.get(id=id)
                multimedia.advertisement = adv
                multimedia.multimedia = jd['multimedia']
                multimedia.description = jd['description']
                multimedia.save()
                datos = {'message': "Success"}
                return Response(data=datos, status=ST_200)
            else:
                datos = {'message': "Advertisement not found..."}
                return Response(data=datos, status=ST_404)
        else:
            datos = {'message': "Multimedia not found..."}
            return Response(data=datos, status=ST_404)

    def delete(self, request, id):
        multimedias = list(Multimedia.objects.filter(id=id).values())
        if len(multimedias) > 0:
            Multimedia.objects.filter(id=id).delete()
            datos = {'message': "Success"}
            return Response(data=datos, status=ST_204)
        else:
            datos = {'message': "Multimedia not found..."}
            return Response(data=datos, status=ST_404)

##################################################################################################################


class AdvertisementView(views.APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if (id > 0):
            advertisement = list(Advertisement.objects.filter(id=id).values())
            if len(advertisement) > 0:
                advertisement = advertisement[0]
                return Response(data=advertisement, status=ST_200)
            else:
                datos = {'message': "advertisement not found..."}
                return Response(data=datos, status=ST_404)
        else:
            try:
                sections = Section.objects.filter(active=True)
                if len(sections) > 0:
                    advertisements = []
                    for sec in sections:
                        section_id = sec.__getattribute__('id')
                        advertisements_with_section_id = Advertisement.objects.filter(
                            section_id=section_id).values()
                        for adv in advertisements_with_section_id:
                            advertisements.append(adv)
                    return Response(data=advertisements, status=ST_200)
                else:
                    datos = {'message': "advertisements not found..."}
                    return Response(data=datos, status=ST_404)
            except Exception:
                datos = {'message': "Sections not found..."}
                return Response(data=datos, status=ST_404)

    def post(self, request):
        jd = json.loads(request.body)
        try:
            sec = Section.objects.filter(id=jd['section_id'])
            if len(sec) > 0:
                sec = sec[0]
                Advertisement.objects.create(
                    title=jd['title'], description=jd['description'], url=jd['url'], section=sec, front_page=jd['front_page'])
                datos = {'message': "Success"}
                return Response(data=datos, status=ST_201)
            else:
                datos = {'message': "Section not found"}
                return Response(data=datos, status=ST_404)
        except IntegrityError:
            error = {
                'error': "This title's advertisement was added into the page, please create another different"}
            return Response(data=error, status=ST_409)

    def put(self, request, id):
        jd = json.loads(request.body)
        advertisements = list(Advertisement.objects.filter(id=id).values())
        if len(advertisements) > 0:
            sec = Section.objects.filter(id=jd['section_id'])
            if len(sec) > 0:
                sec = sec[0]
                advertisement = Advertisement.objects.get(id=id)
                try:
                    advertisement.title = jd['title']
                    advertisement.description = jd['description']
                    advertisement.url = jd['url']
                    advertisement.section = sec
                    advertisement.front_page = jd['front_page']
                    advertisement.save()
                    datos = {'message': "Success"}
                    return Response(data=datos, status=ST_200)
                except IntegrityError:
                    error = {
                        'error': "This title's advertisement was added into the page, please select another different"}
                    return Response(data=error, status=ST_409)
            else:
                datos = {'message': "Section not found"}
                return Response(data=datos, status=ST_404)
        else:
            datos = {'message': "Advertisement not found"}
            return Response(data=datos, status=ST_404)

    def delete(self, request, id):
        advertisements = list(Advertisement.objects.filter(id=id).values())
        if len(advertisements) > 0:
            Advertisement.objects.filter(id=id).delete()
            datos = {'message': "Success"}
            return Response(data=datos, status=ST_200)
        else:
            datos = {'message': "Advertisement not found"}
            return Response(data=datos, status=ST_404)

        # CUSTOM ENDPOINTS


class AdvertisementSectionView(views.APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, section_id=0):
        if (section_id > 0):
            try:
                section = Section.objects.filter(
                    id=section_id).filter(active=True)
                section_id = section.get().__getattribute__('id')

                advertisements_with_section_id = list(
                    Advertisement.objects.filter(section_id=section_id).values())
                return Response(data = advertisements_with_section_id, status=ST_200)
            except Exception:
                datos = {'message': "Section not found"}
                return Response(data=datos, status=ST_404)
        else:
            datos = {'message': "Section not found"}
            return Response(data=datos, status=ST_404)
