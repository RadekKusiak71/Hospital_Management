from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse

@api_view(['GET'])
def apiOverview(request):
    # api_urls = {
    #     'Patient':'/patient/',
    #     'Doctor':'/doctor/',
    #     'Appointment':'/patient/',
    #     'Medicine':'/patient/',
    #     'Perscription':'/patient/',
    #     'PerscriptionItems':'/patient/',
    #     'Room':'/patient/',
    #     'Message':'/patient/',
    # }

    # return Response(api_urls)
    return JsonResponse("API BASE POINT",safe=False)