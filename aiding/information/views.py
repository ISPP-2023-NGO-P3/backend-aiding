from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json

# Create your views here.

class SectionView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, id = 0):
        if (id > 0):
            sections = list(Section.objects.filter(id=id).values())
            if len(sections) > 0:
                section = sections[0]
                datos = {'section': section}
            else:
                datos = {'message': "section not found..."}
            return JsonResponse(section, safe = False)
        else:
            sections = list(Section.objects.values())
            if len(sections) > 0:
                datos = {'sections': sections}
            else:
                datos = {'message': "sections not found..."}
            return JsonResponse(sections, safe = False)
        
    def post(self, request):
        # print(request.body)
        jd = json.loads(request.body)
        # print(jd)
        Section.objects.create(name=jd['name'])
        datos = {'message': "Success"}
        return JsonResponse(datos)

    def put(self, request, id):
        jd = json.loads(request.body)
        sections = list(Section.objects.filter(id=id).values())
        if len(sections) > 0:
            section = Section.objects.get(id=id)
            section.name = jd['name']
            section.save()
            datos = {'message': "Success"}
        else:
            datos = {'message': "Section not found..."}
        return JsonResponse(datos)

    def delete(self, request, id):
        sections = list(Section.objects.filter(id=id).values())
        if len(sections) > 0:
            Section.objects.filter(id=id).delete()
            datos = {'message': "Success"}
        else:
            datos = {'message': "Section not found..."}
        return JsonResponse(datos)
class MultimediaView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, id = 0):
        if (id > 0):
            multimedias = list(Multimedia.objects.filter(id=id).values())
            if len(multimedias) > 0:
                multimedia = multimedias[0]
                datos = {'multimedia': multimedia}
            else:
                datos = {'message': "multimedia not found..."}
            return JsonResponse(multimedia, safe = False)
        else:
            multimedias = list(Multimedia.objects.values())
            if len(multimedias) > 0:
                datos = {'multimedias': multimedias}
            else:
                datos = {'message': "multimedias not found..."}
            return JsonResponse(multimedias, safe = False)
        
    def post(self, request):
        # print(request.body)
        jd = json.loads(request.body)
        adv = Advertisement.objects.filter(id = jd['advertisement_id'])
        if len(adv) > 0:
        # print(jd)
            adv = adv[0]
            Multimedia.objects.create(advertisement=adv, multimedia=jd['multimedia'], description=jd['description'])
            datos = {'message': "Success"}
        else :
            datos = {'message': "Advertisements not found"}
        return JsonResponse(datos)

    def put(self, request, id):
        jd = json.loads(request.body)
        multimedias = list(Multimedia.objects.filter(id=id).values())
        if len(multimedias) > 0:
            adv = Advertisement.objects.filter(id = jd['advertisement_id'])
            if len(adv) > 0:
                adv = adv[0]
                multimedia = Multimedia.objects.get(id=id)
                multimedia.advertisement = adv
                multimedia.multimedia = jd['multimedia']
                multimedia.description = jd['description']
                multimedia.save()
                datos = {'message': "Success"}
            else:
                datos = {'message': "Advertisement not found..."}
        else:
            datos = {'message': "Multimedia not found..."}
        return JsonResponse(datos)

    def delete(self, request, id):
        multimedias = list(Multimedia.objects.filter(id=id).values())
        if len(multimedias) > 0:
            Multimedia.objects.filter(id=id).delete()
            datos = {'message': "Success"}
        else:
            datos = {'message': "Multimedia not found..."}
        return JsonResponse(datos)
class AdvertisementView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, id = 0):
        if (id > 0):
            advertisements = list(Advertisement.objects.filter(id=id).values())
            if len(advertisements) > 0:
                advertisement = advertisements[0]
                datos = {'advertisement': advertisement}
            else:
                datos = {'message': "advertisement not found..."}
            return JsonResponse(advertisement, safe = False)
        else:
            advertisements = list(Advertisement.objects.values())
            if len(advertisements) > 0:
                datos = {'persons': advertisements}
            else:
                datos = {'message': "advertisements not found..."}
            return JsonResponse(advertisements, safe = False)
        
    def post(self, request):
        # print(request.body)
        jd = json.loads(request.body)
        sec = Section.objects.filter(id = jd['section_id'])
        if len(sec) > 0:
        # print(jd)
            sec = sec[0]
            Advertisement.objects.create(title=jd['title'], description=jd['description'], url=jd['url'], section=sec)
            datos = {'message': "Success"}
        else:
            datos = {'message': "Sections not found"}
        return JsonResponse(datos)

    def put(self, request, id):
        jd = json.loads(request.body)
        advertisements = list(Advertisement.objects.filter(id=id).values())
        if len(advertisements) > 0:
            sec = Section.objects.filter(id = jd['section_id'])
            if len(sec) > 0:
                sec = sec[0]
                advertisement = Advertisement.objects.get(id=id)
                advertisement.title = jd['title']
                advertisement.description = jd['description']
                advertisement.url = jd['url']
                advertisement.section = sec
                advertisement.save()
                datos = {'message': "Success"}
            else:
                datos = {'message': "Section not found..."}
        else:
            datos = {'message': "Advertisement not found..."}
        
        return JsonResponse(datos)

    def delete(self, request, id):
        advertisements = list(Advertisement.objects.filter(id=id).values())
        if len(advertisements) > 0:
            Advertisement.objects.filter(id=id).delete()
            datos = {'message': "Success"}
        else:
            datos = {'message': "Advertisement not found..."}
        return JsonResponse(datos)