from urllib import response
from wsgiref.util import setup_testing_defaults
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework import status
from . import models,viewsets
from firebase_admin import auth 
import firebase_admin
from firebase_admin import credentials
# from django.conf import settings
import deliveree_go.settings as settings


class CustomMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        try:
            # cred = credentials.Certificate(str(settings.MEDIA_ROOT)+"/media/firebase_auth/userlogin-aa2c1-firebase-adminsdk-1dooj-aed92a82dc.json")
            # firebase_admin.initialize_app(cred)
            # print(cred)
            api_req = str(request)
            header = request.headers
            uid = header['Authorization']
            user = auth.get_user(uid)
            data = user.provider_data[0]
            print('Successfully fetched user data: {0}'.format(user.email))
            if user:
                pass
            else:
                return JsonResponse({"data":[],"message":"Invalid uid","status":"FAIL"},status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            msg = viewsets.getExceptionData(e)
            return JsonResponse(msg)
        response = self.get_response(request)
        response['Content-Type'] = "application/json"
        return response
    
    # def respond(self,request,message):
    #     response = self.get_response(request)
    #     response['Content-Type'] = "application/json"
    #     response.Content = message
    #     return response

    # def process_request(self,request):
    #     try:
    #         api_req = str(request)
    #         header = request.headers
    #         uid = header['Authorization']
    #         user = auth.get_user(uid)
    #         print('Successfully fetched user data: {0}'.format(user.email))
    #         if user:
    #             return None
    #         else:
    #             return JsonResponse({"data":[],"message":"Invalid uid","status":"FAIL"},status=status.HTTP_401_UNAUTHORIZED)
    #     except Exception as e:
    #         msg = viewsets.getExceptionData(e)
    #         return JsonResponse(msg)
