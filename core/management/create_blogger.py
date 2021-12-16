from core import models
from rest_framework.response import Response
from rest_framework import status


def create_or_update_blogger(request, blogger_id=None):
    languge_id = request.data.get('languge', None)
    country_city_id = request.data.get('country_city', None)
    specialization_id = request.data.get('specialization', None)

    if blogger_id:
        try:
            blogger = models.BloggerAccount.objects.get(id=blogger_id)
        except:
            return Response({'error': 'No such blogger'}, status=status.HTTP_400_BAD_REQUEST)

        languge = blogger.languge
        country_city = blogger.country_city
        specialization = blogger.specialization

        first_name = request.data.get('first_name', blogger.first_name)
        last_name = request.data.get('last_name', blogger.last_name)
        sex = request.data.get('sex', blogger.sex)
        date_of_birth = request.data.get('date_of_birth', blogger.date_of_birth)

        is_conditions_accepted = request.data.get('is_conditions_accepted', blogger.is_conditions_accepted)

    else:
        languge = None
        country_city = None
        specialization = None

        first_name = request.data.get('first_name', None)
        last_name = request.data.get('last_name', None)
        sex = request.data.get('sex', None)
        date_of_birth = request.data.get('date_of_birth', None)
        languge_id = request.data.get('languge', None)
        country_city_id = request.data.get('country_city', None)
        specialization_id = request.data.get('specialization', None)
        is_conditions_accepted = request.data.get('is_conditions_accepted', False)

    blogger = models.BloggerAccount.objects.update_or_create(
        id=blogger_id,
        default={
            'first_name': first_name,
            'last_name': last_name,
            'sex': sex,
            'date_of_birth': date_of_birth,
            'is_conditions_accepted': is_conditions_accepted
        })[0]

    if languge_id:
        try:
            language = models.Language.objects.get(id=languge_id)
            blogger.languages.add(language)
        except:
            return Response({'error': 'No such language'}, status=status.HTTP_400_BAD_REQUEST)
    if country_city_id:
        try:
            country_city = models.Place.objects.get(id=country_city_id)
            blogger.places.add(country_city)
        except:
            return Response({'error': 'No such Place'}, status=status.HTTP_400_BAD_REQUEST)
    if specialization_id:
        try:
            specialization = models.Specialization.objects.get(id=specialization_id)
            blogger.specializations.add(specialization)
        except:
            return Response({'error': 'No such Specialization'}, status=status.HTTP_400_BAD_REQUEST)
    return True