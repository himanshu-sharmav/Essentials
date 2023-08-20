from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate
# from django.contrib.auth.decorators import login_required
from .models import CustomUser,Sections_a,Products,UserProducts
from django.http import JsonResponse,HttpResponseForbidden
from decimal import Decimal
from django.utils import timezone
import datetime
import json
# Create your views here.
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        
        password = data['password']
        email = data['email']
        contact = data['contact']
        address = data['address']
        first_name = data['first_name']
        last_name = data['last_name']
        # superuser = data['superuser',False]
     
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            contact =contact,
            address =address, 
             
        )

        # user_profile = UserProfile.objects.create(
        #    user=user,
        #    address=address,
        #    contact=contact,
           
        # )
        
        return JsonResponse({'message':'Registration successful'})
    else:
        return JsonResponse({'message':'wrong method'}, status=405)
    
def custom_login(request):
  

    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password = data['password']

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            # request.session['user_id'] = user.id
            # request.session['is_superuser'] = user.is_superuser
            # request.session.save()
            if user.is_superuser:
              custom = CustomUser.objects.get(username=username)
              sections = Sections_a.objects.all()
              sections_data = [{'name': section.name, 'image': section.image.url} for section in sections]
            #   sections_data = [{'name': section.name} for section in sections]
              response= JsonResponse(list(sections_data),safe=False)
            #   response.set_cookie(key="username", value=username, max_age=3600,httponly=False,path='/')
            #   response.set_cookie(key="password", value=password, max_age=3600,httponly=False,path='/')
            #   response.cookies['session.id']['samesite'] = 'None'
            #   response.cookies['session.id']['secure'] = True
              response2=JsonResponse({"message":"Manager"})
              return response2
              
            # if user.is_superuser: 
             
            #   data = [{'name':sections.name}]
              
            #   return JsonResponse(list(sections),safe=False)               
            else:
              return JsonResponse({'message':'Normal User logged in','authentication_id':False})  
        else:
            return JsonResponse({'message':'invalid credentials'})
   
   



def add_section(request) :
    # if not request.user.is_super:
    #     return HttpResponseForbidden("Permission Denied")
    if request.method == 'GET':
       user =request.user
       if user.is_superuser:
          sections = Sections_a.objects.filter(delete_sign=False)
          sections_data = [{'id': section.id,'name': section.name, 'image': section.image.url} for section in sections]
          return JsonResponse(list(sections_data),safe=False)
    if request.method == 'POST':
    #   data = json.loads(request.body)
    #   request.COOKIES.get('username')
    #   request.COOKIES.get('password')
      user = request.user
    #  data=json.loads(request.body)
      if user.is_authenticated and user.is_superuser:
            # if request.user.is_superuser:
            name = request.POST.get('sectionName')
            image_file = request.FILES.get('sectionImage') 
            # Sections_a.objects.create(name=name)
            #           
            if name and image_file is not None:
                Sections_a.objects.create(image=image_file,name=name)
            #  new_section = Sections_a(name=name)
            #  new_section.save()
                return JsonResponse({'message':'Section Added Successfully'})
            else:
             return JsonResponse({'message':'no added'})
      else:
         return JsonResponse({'message':'invalid authentication request'},status=400)
    else:
        return JsonResponse({'message':'Invalid request method'}, status=405)  

def  edit_section(request,section_id):
    section =get_object_or_404(Sections_a,id=section_id)

    if request.method =='POST':
        # data =json.loads(request.body)
        name = request.POST.get('name')
        image_file = request.FILES.get('product_image')
        if name is not None:    
         section.name = name
         
        if image_file is not None:   
         section.image=image_file
        
        if name is not None or image_file is not None:
            section.update_date = timezone.now()
            section.save()
        
        return JsonResponse({'message':'Section updated successfully'})
    else:
        return JsonResponse({'message':'Invalid request method'}, status=405)
    
def remove_section(request):
    section_id= request.POST.get('section_id')
    section =get_object_or_404(Sections_a,id=section_id)
    
    if request.method=='POST':
        section.delete_sign=True
        section.delete_date =timezone.now()
        section.save()
        return JsonResponse({'message':'Section removed successfully'})
    else:
        return JsonResponse({'message':'Invalid request method'})    
    
def add_product(request):
  if request.method =='GET':
    user =request.user
    if user.is_authenticated and user.is_superuser:
        products=Products.objects.filter(delete_sign=False).all()
        products_data = [{'id':product.id,'name': product.name, 'section': product.section.name, 'manufacture_date': product.manufacture_date.strftime('%Y-%m-%d'), 'expiring_date': product.expiring_date.strftime('%Y-%m-%d'), 'rate_per_unit': str(product.rate_per_unit), 'image': product.image.url} for product in products]
            # return JsonResponse(products_data, safe=False)
        return JsonResponse(list(products_data),safe=False)   
  if request.method =='POST':  
    # data =json.loads(request.body)
    # data = json.loads(request.POST.get('data'))
    name = request.POST.get('productName')
    section_id = request.POST.get('section_id')
    manufacture_date = request.POST.get('manufactureDate')
    expiring_date = request.POST.get('expiryDate')
    rate_per_unit = request.POST.get('ratePerUnit')
    image_file = request.FILES.get('productImage')
    if not name or not manufacture_date or not expiring_date  or not rate_per_unit:
       return JsonResponse({'message':'All Fields are required'})
    section = Sections_a.objects.get(id=section_id)

    manufacture_date = datetime.datetime.strptime(manufacture_date,"%Y-%m-%d").date()
    expiring_date = datetime.datetime.strptime(expiring_date,"%Y-%m-%d").date()
    rate_per_unit = Decimal(rate_per_unit)

    product = Products(
       name=name,
       section=section,
       manufacture_date=manufacture_date,
       expiring_date=expiring_date,
       rate_per_unit=rate_per_unit,
       image=image_file
   )
    product.save()
    return JsonResponse({'message':'Products added successfully'})
  else:
      return JsonResponse({'message':'invalid request method'})
  
def edit_product(request,product_id):
    if request.method == 'POST': 
        product_id= request.POST.get('product_id')
        product = get_object_or_404(Products,id=product_id)
    
        name =request.POST.get('name')
        section_id = request.POST.get('section_id')
        manufacture_date = request.POST.get('manufacture_date')
        expiring_date = request.POST.get('expiring_date')
        rate_per_unit = request.POST.get('rate_per_unit')
        image_file = request.FILES.get('product_image')
        if not section_id or not product_id:
         return JsonResponse({'message':'Section id and Product_id is required'})

        # manufacture_date = datetime.datetime.strptime(manufacture_date,"%Y-%m-%d").date()
        # expiring_date = datetime.datetime.strptime(expiring_date,"%Y-%m-%d").date()
        # rate_per_unit = Decimal(rate_per_unit)
        section_id = int(section_id)
        section = Sections_a.objects.get(id=section_id)
        if name is not None:     
            product.name =name    
        if section is not None:    
            product.section=section
        if manufacture_date is not None:   
            product.manufacture_date=manufacture_date
        if expiring_date is not None:
            product.expiring_date=expiring_date
        if rate_per_unit is not None:    
            product.rate_per_unit=rate_per_unit
        if image_file is not None:
            product.image=image_file

        if name is not None or section is not None or manufacture_date is not None or expiring_date is not None or rate_per_unit is not None or image_file is not None:
            section.update_date = timezone.now()
            product.save()

        return JsonResponse({'message':'Product updated successfully'})
    else:
        return JsonResponse({'message':'Invalid request method'})
    
def remove_product(request,product_id):
    product= get_object_or_404(Products,id=product_id)

    if request.method =='POST':
        product.delete_sign=True
        product.delete_date=timezone.now()
        product.save()
        return JsonResponse({'message':'Product deleted successfully'})
    else:
        return JsonResponse({'message':'Invalid request method'})
    
def search_sections(request):
    query = request.GET.get('q')
    if query:
        sections= Sections_a.objects.filter(name__icontains=query).values()
    else:
        sections=Sections_a.objects.all().values()

    return JsonResponse(list(sections),safe=False)

def search_products(request):
    query= request.GET.get('q')
    if query:
        sections=Products.objects.filter(name__icontains=query).values()
    else:
        sections=Products.objects.all().values()
    return JsonResponse(list(sections),safe=False)

def add_to_cart(request,product_id):
    product = get_object_or_404(Products,id=product_id)
    user =request.user
    if request.method=='POST':
        quantity= int(request.POST.get('quantity',1))
        user_product,created= UserProducts.objects.get_or_create(user=user,product=product)

        if created:
            user_product.quantity= quantity
        else:
            user_product.quantity+= quantity

        user_product.save()
        return JsonResponse({'message':'Product added to cart successfully.'})
    elif request.method == 'GET':
        cart_items = UserProducts.objects.filter(user=user)
        cart_data = [{'product_id': item.product.id, 'quantity': item.quantity} for item in cart_items]
        return JsonResponse({'cart_items': cart_data})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)            
    
def view_cart(request):
    user=request.user
    cart_items = UserProducts.objects.filter(user=user).values()

    return JsonResponse(list(cart_items),safe=False)

def buy_products(request):
    if request.method=='POST':
        # cart_items = request.POST.getlist('cart_item')
            total_amount = 0

        # for item in cart_items:
            item_id = request.POST.get('item_id')
            requested_quantity = int(request.POST.get('quantity'))
            product = get_object_or_404(Products,id=item_id)
            
            if product.quantity >= requested_quantity:
                total_amount+=product.rate_per_unit*requested_quantity
                product.quantity-=requested_quantity
                # if product.quantity < 0:
                #    product.quantity = 0 
                product.save()
            else:
                return JsonResponse({'message':'Product not available in requested quantity'})    
                # decrease_stored_quantity(product,quantity)
                # add_to_cart(request.user,product,quantity)
            return JsonResponse({"message":"Product bought successfully.","total amount":total_amount})        
    else:
        return JsonResponse({'message':'Invalid request method'}, status=405)   

# def product_available(user, product, requested_quantity):
    
#     return product.quantity >= requested_quantity  
# def decrease_stored_quantity(produ)
# def remove_cart(request):
#     user = request.user

#     if request.method == 'POST':
#         UserProducts.objects.filter(user=user).delete()

#         return JsonResponse

# def show_section(request):       
