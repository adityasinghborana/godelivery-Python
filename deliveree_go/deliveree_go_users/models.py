from django.contrib.gis.db import models

class users(models.Model):
    userid = models.AutoField(primary_key=True)
    uid = models.CharField(max_length=200,default='',unique=True)
    email = models.CharField(default='',max_length=100,null=True,blank=True)
    contact_number = models.CharField(max_length=100,default='',null=True,blank=True)
    first_name = models.CharField(default='',max_length=100,null=True,blank=True)
    last_name = models.CharField(default='',max_length=100,null=True,blank=True)
    username = models.CharField(default='',max_length=100,null=True,blank=True)
    created_on = models.CharField(max_length=300,default='')
    modified_on = models.CharField(max_length=300,default='')


class user_locations(models.Model):
    address_id = models.AutoField(primary_key=True)
    userid = models.IntegerField(null=True,blank=True)
    uid = models.CharField(max_length=200,null=True,blank=True)
    email = models.CharField(null=True,blank=True,max_length=100)
    address_type = models.CharField(max_length=50)
    house_flat = models.CharField(max_length=200)
    road_area = models.CharField(max_length=200)
    landmark = models.CharField(max_length=200)
    postalcode = models.CharField(max_length=20)
    location = models.TextField()
    the_geom= models.GeometryField()
    created_on = models.CharField(max_length=300,default='')
    modified_on = models.CharField(max_length=300,default='')
    class Meta:
        db_table = 'user_locations'


def categoryImage_directory_path(instance, filename):
    category_name = instance.category_name.replace(" ","")
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'media/category_types/{0}/{1}'.format((category_name), filename)

class category_types(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100,unique=True)
    category_description = models.TextField()
    image = models.FileField(upload_to=categoryImage_directory_path)
    class Meta:
        db_table = "category_types"


def shopImage_directory_path(instance, filename):
    # shop_name = instance.shop_name.replace(" ","")
    # shop_id = str(instance.shop_id)
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    # return 'media/shops/{0}/{1}'.format((shop_name), filename)
    shop_id = str(instance.shop_id)
    return 'media/shops/{0}/{1}'.format((shop_id), filename)

class shops_list(models.Model):
    shop_id = models.AutoField(primary_key=True)
    shop_name = models.CharField(default='',max_length=200)
    open_time = models.CharField(default='',max_length=200)
    closing_time = models.CharField(default='',max_length=200)
    menu_data = models.TextField()
    shop_type = models.CharField(default='',max_length=50)
    category_id = models.IntegerField(null=True)
    category_type = models.CharField(default='',max_length=200)
    # images = models.FileField(upload_to=shopImage_directory_path)
    address = models.TextField(default='')
    location = models.TextField()
    the_geom = models.GeometryField()
    created_on = models.CharField(max_length=300,default='')
    modified_on = models.CharField(max_length=300,default='')

    class Meta():
        db_table = 'shops_list'

class shops_images(models.Model):
    image_id = models.AutoField(primary_key=True)
    shop_id = models.IntegerField()
    image = models.FileField(upload_to=shopImage_directory_path)
    created_on = models.CharField(max_length=300,default='')

    class Meta():
        db_table = 'shops_images'   


class items_list(models.Model):
    item_id = models.AutoField(primary_key=True)
    shop_id = models.IntegerField()
    item_name = models.CharField(max_length=300)
    item_type = models.CharField(max_length=200)
    category_id = models.BigIntegerField()
    category_type = models.CharField(default='',max_length=200)
    item_price = models.FloatField()
    something_extra = models.TextField()
    created_on = models.CharField(max_length=300,default='')
    modified_on = models.CharField(max_length=300,default='')
    class Meta():
        db_table = 'items_list'

class order_details(models.Model):
    order_id = models.AutoField(primary_key=True)
    uid = models.CharField(max_length=300)
    username = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=50)
    delivery_address_id = models.IntegerField()
    billing_address_id = models.CharField(max_length=1000)
    rider_tip_aount = models.CharField(max_length=100)
    driver_id = models.IntegerField(null=True,blank=True)
    total_amount = models.CharField(max_length=200)
    payment_method = models.CharField(max_length=200)
    created_on = models.CharField(max_length=300,default='')
    modified_on = models.CharField(max_length=300,default='')
    
    class Meta():
        db_table = 'order_details'

class addratings(models.Model):
    rating_id = models.AutoField(primary_key=True)
    uid = models.CharField(max_length=200)
    user_id = models.IntegerField()
    item_id = models.IntegerField()
    shop_id = models.IntegerField()
    rating = models.IntegerField()
    reviews = models.TextField(default='')
    created_on = models.CharField(max_length=200)
