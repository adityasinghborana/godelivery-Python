from email.utils import getaddresses
from getpass import getuser
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.serializers import serialize
import requests,pyrebase,sys,os
from django.contrib.gis.geos import GEOSGeometry,Point,MultiPoint
from . import models
# from django.conf import settings
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from datetime import datetime
from django.db.models import Avg
import json
# firebase = pyrebase.initialize_app()

def getExceptionData(e):
    exc_type,exc_obj,exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    message = {}
    message["filename"] = fname
    message["line_number"] = exc_tb.tb_lineno
    message["exc_obj"] = str(exc_obj)
    template = "An exception of type {0} occured. Argument:\n{1!r}"
    msg = template.format(type(e).__name__,e.args)
    message["message"] = msg
    return message

def verifyfirebaseAuth(request):
    uid = request.headers['Authorization']
    # uid = "YAN4JOclzTXASEF7zANEJSpTZnW2"
    user = auth.get_user(uid)
    print('Successfully fetched user data: {0}'.format(user.uid))
    return user

# class category_list(APIView):
class home_pageApi(APIView):
    def get(self,request):
        try:
            user = verifyfirebaseAuth(request)
            uid = user.uid
            response = {}
            getUser = models.users.objects.get(uid=uid)
            response['username'] = getUser.username
            getaddress = models.user_locations.objects.filter(uid=uid,userid=getUser.userid)
            address_data = json.loads(serialize('json',getaddress))
            address_res = []
            for address in address_data:
                address['fields']['address_id'] = address['pk']
                address_res.append(address['fields'])
            response['addresses'] =  address_res
            result = models.category_types.objects.all()
            result = json.loads(serialize('json',result))
            category_res = []
            for data in result:
                data['fields']['category_id'] = data['pk']
                data.pop('pk',None)
                data.pop('models',None)
                category_res.append(data['fields'])
            response['categories'] = category_res
            return Response({"data":response,"status":"PASS","message":"category list fetched successfully"},status=status.HTTP_200_OK)
        except Exception as e:
            msg = getExceptionData(e)
            return Response({"data":msg},status=status.HTTP_400_BAD_REQUEST)

class shopsListData(APIView):
    def get(self,request):
        try:
            user = verifyfirebaseAuth(request)
            uid = user.uid
            user_id = self.request.query_params.get('user_id')
            category_id = self.request.query_params.get('category_id')
            getallshops = models.shops_list.objects.filter(category_id=category_id)
            getallshops = json.loads(serialize('json',getallshops))
            response = {}
            shops_data = []
            for shops in getallshops:
                reviews_list = []
                images_list = []
                shop_id = shops['pk']
                getShopRatingAvg = models.addratings.objects.filter(shop_id=shop_id).aggregate(Avg('rating'))
                shops['fields']['shop_id'] = shop_id
                getImages = models.shops_images.objects.filter(shop_id=shop_id)
                getImages = json.loads(serialize('json',getImages))
                images_list = []
                if getImages:
                    for image in getImages:
                        image['fields']['image_id'] = image['pk']
                        getImage = models.shops_images.objects.get(image_id=image['pk'])
                        image['fields']['image_url'] = getImage.image.path
                        images_list.append(image['fields'])
                shops['fields']['images'] = images_list
                shops['fields']['ratings'] = getShopRatingAvg
                getreviews = models.addratings.objects.filter(shop_id=shop_id)
                getreviews = json.loads(serialize('json',getreviews))
                if getreviews:
                    for review in getreviews:
                        data = {
                            "rating_id":review['pk'],
                            "rating":review['fields']['rating'],
                            "reviews":review['fields']['reviews'],
                            "created_on":review['fields']['created_on']
                            }
                        reviews_list.append(data)
                shops['fields']['reviews'] = reviews_list
                shops_data.append(shops['fields'])
            return Response({"data":shops_data,"status":"PASS","message":"shops data fetched"})        
        except Exception as e:
            msg = getExceptionData(e)
            return Response({"data":msg},status=status.HTTP_400_BAD_REQUEST)

class itemsListData(APIView):
    def get(self,request):
        try:
            user = verifyfirebaseAuth(request)
            uid = user.uid
            user_id = request.data.get('user_id')
            category_id = request.data.get('category_id')
            shop_id = request.data.get('shop_id')
            getItemsData = models.items_list.objects.filter(shop_id)
            getItemsData = json.loads(serialize('json',getItemsData))
            item_lists = []
            if getItemsData:
                for items in getItemsData:
                    items['fields']['item_id'] = items['pk']
                    item_lists.append(items['fields'])
            return Response({"data":item_lists,"status":"PASS","message":"Successfully fetched items data"})
        except Exception as e:
            msg = getExceptionData(e)
            return Response({"data":msg},status=status.HTTP_400_BAD_REQUEST)



class ratingitems(APIView):
     def post(self,request):
        try:
            user = verifyfirebaseAuth(request)
            uid = user.uid
            user_id = request.data.get('user_id')
            item_name = request.data.get('item_name')
            item_id = request.data.get('item_id')
            shop_id = request.data.get('shop_id')
            rating = request.data.get('rating')


        except Exception as e:
            msg = getExceptionData(e)
            return Response({"data":msg},status=status.HTTP_400_BAD_REQUEST) 

class addressAfterLogin(APIView):
    def post(self,request):
        try:
            user = verifyfirebaseAuth(request)
            uid = user.uid
            first_name = request.data.get('first_name')
            last_name = request.data.get('last_name')
            if user.email !=None:
                email = user.email
            else:
                email = request.data.get('email')
            if user.phone_number != None:
                contact_number = user.phone_number
            else:
                contact_number = request.data.get('contact_number')
            if email:
                username = email.rpartition('@')[0]
            else:
                username = first_name.replace(" ","")
            address_type =request.data.get('address_type')
            house_flat =request.data.get('house_flat')
            road_area =request.data.get('road_area')
            landmark =request.data.get('landmark')
            postalcode =request.data.get('postalcode')
            location = str(request.data.get('location'))
            geom = GEOSGeometry(location,srid=4326)
            checkUser = models.users.objects.filter(uid=uid).exists()
            if not checkUser:
                # data = {}
                # data['uid'] = uid
                # data['email'] = email
                addUser = models.users.objects.create(uid=uid,email=email,username=username,first_name=first_name,last_name=last_name,contact_number=contact_number,)
                userid = addUser.userid
            else:
                user = models.users.objects.get(uid=uid)
                userid = user.userid
            saveData = models.user_locations.objects.create(address_type=address_type,house_flat=house_flat,road_area=road_area,landmark=landmark,postalcode=postalcode,location=location,the_geom=geom,email=email,uid=uid,userid=userid)
            if saveData:
                data = models.user_locations.objects.filter(address_id=saveData.saveData)
                data = serialize('json',data)
                return Response({'data':data,"message":"Successfully address Saved"},status=status.HTTP_201_CREATED)
            else:
                return Response({'data':'',"message":"Failed address Saved"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            msg = getExceptionData(e)
            return Response({"data":msg},status=status.HTTP_400_BAD_REQUEST)




##VENDORS : 

class shopData(APIView):
    def post(self,request):
        try:
            current_date = int(datetime.timestamp(datetime.now())) * 1000
            shop_name = request.data.get('shop_name')
            open_time = request.data.get('open_time')
            closing_time = request.data.get('closing_time')
            menu_data = request.data.get('menu_data')
            shop_type = request.data.get('shop_type')
            # category_id = request.data.get('category_id')
            category_type =request.data.get('category_type')
            category_description = request.data.get('category_description')
            images = dict((request.data).lists())['images']
            location = request.data.get('location')
            the_geom = GEOSGeometry(location,srid=4326)
            save_shopdata = models.shops_list.objects.create(shop_name=shop_name,open_time=open_time,closing_time=closing_time,menu_data=menu_data,shop_type=shop_type,category_type =category_type,location=location,the_geom=the_geom,created_on =current_date,modified_on=current_date,category_id=None)
            shop_id = save_shopdata.shop_id
            check_category = models.category_types.objects.filter(category_name=category_type).exists()
            if not check_category:
                category = models.category_types.objects.create(category_name=category_type,category_description=category_description)
                category_id = category.category_id
                save_shopdata.category_id = category_id
                save_shopdata.save()
            else:
                category = models.category_types.objects.get(category_name=category_type)
                category_id = category.category_id
                save_shopdata.category_id = category_id
                save_shopdata.save()
            a = save_shopdata
            
            ## insert images
            for image in images:
                addImage = models.shops_images.objects.create(shop_id=shop_id,image=image,created_on=current_date)
            
            return Response({"data":save_shopdata.shop_id})
        except Exception as e:
            msg = getExceptionData(e)
            return Response({"data":msg},status=status.HTTP_400_BAD_REQUEST)