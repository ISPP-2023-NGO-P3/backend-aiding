import json

from django.db import IntegrityError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import views
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK as ST_200
from rest_framework.status import HTTP_201_CREATED as ST_201
from rest_framework.status import HTTP_204_NO_CONTENT as ST_204
from rest_framework.status import HTTP_404_NOT_FOUND as ST_404
from rest_framework.status import HTTP_409_CONFLICT as ST_409

from .models import Advertisement, Multimedia, Resource, Section


class CsrfExemptMixin:
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class SectionView(CsrfExemptMixin, views.APIView):
    def get(self, request, section_id=0):
        if section_id > 0:
            section = list(Section.objects.filter(id=section_id).values())
            if len(section) > 0:
                section = section[0]
                return Response(data=section, status=ST_200)
            else:
                datos = {"message": "section not found..."}
                return Response(data=datos, status=ST_404)
        else:
            sections = list(Section.objects.filter(active=True).values())
            lenght = len(sections)
            if lenght > 0:
                return Response(data=sections, status=ST_200)
            else:
                datos = {"message": "sections not found..."}
            return Response(data=datos, status=ST_404)

    def post(self, request):
        jd = json.loads(request.body)
        name = jd["name"]

        try:
            active = jd["active"]
        except KeyError:
            active = True

        try:
            Section.objects.create(name=name, active=active)
            datos = {"message": "Success"}
            return Response(data=datos, status=ST_201)
        except IntegrityError:
            error = {
                "error": "This section was added into the page, please create another different"
            }
            return Response(data=error, status=ST_409)

    def put(self, request, section_id):
        jd = json.loads(request.body)
        sections = list(Section.objects.filter(id=section_id).values())
        if len(sections) > 0:
            section = Section.objects.get(id=section_id)
            try:
                section.name = jd["name"]
                section.active = jd["active"]
                section.save()
                datos = {"message": "Success"}
                return Response(data=datos, status=ST_200)
            except IntegrityError:
                error = {
                    "error": "This section was added into the page, please select another different"
                }
                return Response(data=error, status=ST_409)
        else:
            datos = {"message": "Section not found..."}
        return Response(data=datos, status=ST_404)

    def delete(self, request, section_id):
        sections = list(Section.objects.filter(id=section_id).values())
        if len(sections) > 0:
            Section.objects.filter(id=section_id).delete()
            datos = {"message": "Success"}
            return Response(data=datos, status=ST_204)
        else:
            datos = {"message": "Section not found..."}
            return Response(data=datos, status=ST_404)


class MultimediaView(CsrfExemptMixin, views.APIView):
    def get(self, request, multimedia_id=0):
        if multimedia_id > 0:
            multimedia = list(Multimedia.objects.filter(
                id=multimedia_id).values())
            if len(multimedia) > 0:
                multimedia = multimedia[0]
                return Response(data=multimedia, status=ST_200)
            else:
                datos = {"message": "multimedia not found..."}
                return Response(data=datos, status=ST_404)
        else:
            multimedias = list(Multimedia.objects.values())
            if len(multimedias) > 0:
                return Response(data=multimedias, status=ST_200)
            else:
                datos = {"message": "multimedias not found..."}
            return Response(data=datos, status=ST_404)

    def post(self, request):
        jd = json.loads(request.body)
        adv = Advertisement.objects.filter(id=jd["advertisement_id"])
        if len(adv) > 0:
            adv = adv[0]
            Multimedia.objects.create(
                advertisement=adv,
                multimedia=jd["multimedia"],
                description=jd["description"],
            )
            datos = {"message": "Success"}
            return Response(data=datos, status=ST_201)
        else:
            datos = {"message": "Advertisements not found"}
            return Response(data=datos, status=ST_404)

    def put(self, request, multimedia_id):
        jd = json.loads(request.body)
        multimedias = list(Multimedia.objects.filter(
            id=multimedia_id).values())
        if len(multimedias) > 0:
            adv = Advertisement.objects.filter(id=jd["advertisement_id"])
            if len(adv) > 0:
                adv = adv[0]
                multimedia = Multimedia.objects.get(id=multimedia_id)
                multimedia.advertisement = adv
                multimedia.multimedia = jd["multimedia"]
                multimedia.description = jd["description"]
                multimedia.save()
                datos = {"message": "Success"}
                return Response(data=datos, status=ST_200)
            else:
                datos = {"message": "Advertisement not found..."}
                return Response(data=datos, status=ST_404)
        else:
            datos = {"message": "Multimedia not found..."}
        return Response(data=datos, status=ST_404)

    def delete(self, request, multimedia_id):
        multimedias = list(Multimedia.objects.filter(
            id=multimedia_id).values())
        if len(multimedias) > 0:
            Multimedia.objects.filter(id=multimedia_id).delete()
            datos = {"message": "Success"}
            return Response(data=datos, status=ST_204)
        else:
            datos = {"message": "Multimedia not found..."}
        return Response(data=datos, status=ST_404)


class AdvertisementView(CsrfExemptMixin, views.APIView):
    def get(self, request, advertisement_id=0):
        if advertisement_id > 0:
            advertisement = list(
                Advertisement.objects.filter(id=advertisement_id).values("id",
                            "title",
                            "abstract",
                            "body",
                            "url",
                            "section_id__name",
                            "section_id",
                            "front_page",
                            "creation_date")
            )
            if len(advertisement) > 0:
                advertisement = advertisement[0]
                return Response(data=advertisement, status=ST_200)
            else:
                datos = {"message": "advertisement not found..."}
                return Response(data=datos, status=ST_404)
        else:
            try:
                sections = Section.objects.all()
                if len(sections) > 0:
                    advertisements = []
                    for sec in sections:
                        section_id = sec.__getattribute__("id")
                        advertisements_with_section_id = Advertisement.objects.filter(
                            section_id=section_id
                        ).values(
                            "id",
                            "title",
                            "abstract",
                            "body",
                            "url",
                            "section_id__name",
                            "front_page",
                            "creation_date"
                        )
                        for adv in advertisements_with_section_id:
                            advertisements.append(adv)
                    return Response(data=advertisements, status=ST_200)
                else:
                    datos = {"message": "advertisements not found..."}
                    return Response(data=datos, status=ST_404)
            except Exception:
                datos = {"message": "Sections not found..."}
                return Response(data=datos, status=ST_404)

    def post(self, request):
        try:
            section_id = request.POST.get("section_id")
            title = request.POST.get("title")
            abstract = request.POST.get("abstract")
            body = request.POST.get("body")
            url = request.POST.get("url")
            section = Section.objects.get(id=section_id)
            front_page = request.FILES.get("front_page")
            
            Advertisement.objects.create(
                title=title,
                abstract=abstract,
                body=body,
                url=url,
                section=section,
                front_page=front_page,
            )
            datos = {"message": "Success"}
            return Response(data=datos, status=ST_201)
        except Section.DoesNotExist:
            datos = {"message": "Section not found"}
            return Response(data=datos, status=ST_404)
        except IntegrityError:
            error = {
                "error": "This title's advertisement was added into the page, please create another different"
            }
            return Response(data=error, status=ST_409)

    def put(self, request, advertisement_id):

        section_id = request.POST.get("section_id")
        title = request.POST.get("title")
        abstract = request.POST.get("abstract")
        body = request.POST.get("body")
        url = request.POST.get("url")
        front_page = request.FILES.get("front_page")

        advertisements = list(
            Advertisement.objects.filter(id=advertisement_id).values()
        )
        if len(advertisements) > 0:
            sec = Section.objects.filter(id=section_id)
            if len(sec) > 0:
                sec = sec[0]
                advertisement = Advertisement.objects.get(id=advertisement_id)
                try:
                    advertisement.title = title
                    advertisement.abstract = abstract
                    advertisement.body = body
                    advertisement.url = url
                    advertisement.section = sec
                    if front_page is not None:
                        advertisement.front_page = front_page
                    advertisement.save()
                    datos = {"message": "Success"}
                    return Response(data=datos, status=ST_200)
                except IntegrityError:
                    error = {
                        "error": "This title's advertisement was added into the page, please select another different"
                    }
                    return Response(data=error, status=ST_409)
            else:
                datos = {"message": "Section not found"}
                return Response(data=datos, status=ST_404)
        else:
            datos = {"message": "Advertisement not found"}
            return Response(data=datos, status=ST_404)

    def delete(self, request, advertisement_id):
        advertisements = list(
            Advertisement.objects.filter(id=advertisement_id).values()
        )
        if len(advertisements) > 0:
            Advertisement.objects.filter(id=advertisement_id).delete()
            datos = {"message": "Success"}
            return Response(data=datos, status=ST_200)
        else:
            datos = {"message": "Advertisement not found"}
            return Response(data=datos, status=ST_404)


class AdvertisementSectionView(CsrfExemptMixin, views.APIView):
    def get(self, request, section_id=0):
        if section_id > 0:
            try:
                section = Section.objects.filter(
                    id=section_id).filter(active=True)
                section_id = section.get().__getattribute__("id")

                advertisements_with_section_id = list(
                    Advertisement.objects.filter(section_id=section_id).values(
                            "id",
                            "title",
                            "abstract",
                            "url",
                            "section_id__name",
                            "front_page",
                            "creation_date")
                )
                return Response(data=advertisements_with_section_id, status=ST_200)
            except Exception:
                datos = {"message": "Section not found"}
                return Response(data=datos, status=ST_404)
        else:
            datos = {"message": "Section not found"}
            return Response(data=datos, status=ST_404)


class ResourceView(CsrfExemptMixin, views.APIView):
    def get(self, request, resource_id=0):
        if resource_id > 0:
            resources = list(Resource.objects.filter(id=resource_id).values())
            if len(resources) > 0:
                resource = resources[0]
                return Response(data=resource, status=ST_200)
            else:
                data = {"message": "Resource not found..."}
                return Response(data=data, status=ST_404)
        else:
            resources = list(Resource.objects.values())
            if len(resources) > 0:
                return Response(data=resources, status=ST_200)
            else:
                data = {"message": "Resources not found..."}
            return Response(data=data, status=ST_404)

    def post(self, request):
        jd = json.loads(request.body)
        try:
            street = jd["street"]
            number = jd["number"]
            city = jd["city"]

            coord = Resource.get_coordinates(self, street, number, city)
            if isinstance(coord, Response):
                return coord
            Resource.objects.create(
                title=jd["title"],
                description=jd["description"],
                contact_phone=jd["contact_phone"],
                street=street,
                number=number,
                city=city,
                resource_type=jd['resource_type'],
                additional_comments=jd["additional_comments"],
                latitude=coord[0],
                longitude=coord[1],
            )
            data = {"message": "Success"}
            return Response(data=data, status=ST_201)
        except IntegrityError:
            error = {
                "error": "This resource was added into the page, please create another different"
            }
            return Response(data=error, status=ST_409)

    def put(self, request, resource_id):
        jd = json.loads(request.body)
        resources = list(Resource.objects.filter(id=resource_id).values())
        if len(resources) > 0:
            resource = Resource.objects.get(id=resource_id)
            try:

                resource.title = jd["title"]
                resource.description = jd["description"]
                resource.contact_phone = jd["contact_phone"]
                resource.additional_comments = jd["additional_comments"]
                resource.resource_type=jd['resource_type']
                street = jd["street"]
                number = jd["number"]
                city = jd["city"]

                coord = Resource.get_coordinates(self, street, number, city)
                if isinstance(coord, Response):
                    return coord

                resource.number = number
                resource.street = street
                resource.city = city

                resource.latitude = coord[0]
                resource.longitude = coord[1]

                resource.save()
                data = {"message": "Success"}

                return Response(data=data, status=ST_200)
            except IntegrityError:
                error = {
                    "error": "This resource was added into the page, please select another different"
                }
                return Response(data=error, status=ST_409)
        else:
            data = {"message": "Resource not found..."}
            return Response(data=data, status=ST_404)

    def delete(self, request, resource_id):
        resources = list(Resource.objects.filter(id=resource_id).values())
        if len(resources) > 0:
            Resource.objects.filter(id=resource_id).delete()
            data = {"message": "Success"}
            return Response(data=data, status=ST_204)
        else:
            data = {"message": "Resource not found..."}
            return Response(data=data, status=ST_404)


