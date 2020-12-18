from django.http import HttpResponse,JsonResponse
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import sqlite3
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from datetime import *

def addCateogryPage(request):
    return render(request, 'myadmin/addCategory.html')


def addCategoryAction(request):
    name = request.GET['name']
    Description = request.GET['description']

    conn = sqlite3.connect('db.sqlite3')
    cr1 = conn.cursor()
    selectQuery = "select name from category"
    cr1.execute(selectQuery)
    result = cr1.fetchall()
    for item in result:
        if name in item:
            return HttpResponse("AllReady ")
    query = f"insert into category ('name', 'description') values ('{name}','{Description}')"
    cr = conn.cursor()
    cr.execute(query)
    conn.commit()
    messages.add_message(request, messages.SUCCESS, 'Data Add Success')
    return redirect(viewCateogrypage)


def viewCateogrypage(request):
    conn = sqlite3.connect('db.sqlite3')
    query = "select * from category"
    cr = conn.cursor()
    cr.execute(query)
    result = cr.fetchall()
    result_data = []
    sno = 0
    for item in result:
        dist = {
            'sno': sno,
            'id': item[0],
            'name': item[1],
            'description': item[2],
            'photo': item[3]
        }
        sno += 1
        result_data.append(dist)
    return render(request, 'myadmin/categoryview.html', {'data': result_data})


def deleteCategory(request):
    id = request.GET['id']
    conn = sqlite3.connect('db.sqlite3')
    query = "Delete from category where id = {}".format(id)
    cr = conn.cursor()
    cr.execute(query)
    conn.commit()
    messages.add_message(request, messages.ERROR, 'Data Deleted Success item id: {}'.format(id))
    return redirect(viewCateogrypage)


def editCateogry(request):
    id = request.GET['id']
    conn = sqlite3.connect('db.sqlite3')
    query = "select * from category where id = {}".format(id)
    cr = conn.cursor()
    cr.execute(query)
    result = cr.fetchone()
    return render(request, 'myadmin/editCateogry.html', {'data': result})


def editCategoryAction(request):
    id = request.POST['id']
    name = request.POST['name']
    description = request.POST['description']
    photo=request.FILES['photo']
    Ar = FileSystemStorage()
    filename = Ar.save("productImages/" + photo.name, photo)
    query = "update category set name = '{}', description = '{}', photo='{}' where id ={}".format(name, description, Ar.url(filename),id)
    conn = sqlite3.connect('db.sqlite3')
    cr = conn.cursor()
    cr.execute(query)
    conn.commit()
    messages.add_message(request, messages.WARNING, 'Data Edit Success')
    return redirect(viewCateogrypage)


def addproduct(request):
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        priceAfterDiscount = request.POST['priceAfterDiscount']
        description = request.POST['description']
        brand = request.POST['brand']
        cid = request.POST['cid']
        photo = request.FILES['photo']
        Ar = FileSystemStorage()
        filename = Ar.save("productImages/" + photo.name, photo)
        query = f"insert into products (name,price,priceAfterDiscount, description, brand,category_id,photo) values('{name}','{price}','{priceAfterDiscount}','{description}','{brand}','{cid}','{Ar.url(filename)}')"
        conn = sqlite3.connect('db.sqlite3')
        cr = conn.cursor()
        cr.execute(query)
        conn.commit()
        messages.add_message(request, messages.SUCCESS, 'Product {} Add Success.'.format(name))
        return redirect(addproduct)

    conn = sqlite3.connect('db.sqlite3')
    query = "select * from category"
    cr = conn.cursor()
    cr.execute(query)
    result = cr.fetchall()
    result_all = []
    for item in result:
        dist = {}
        dist['id'] = item[0]
        dist['name'] = item[1]
        result_all.append(dist)
    content = {
        'data': result_all
    }
    return render(request, 'myadmin/addproduct.html', content)


def view_product(request):
    return render(request, 'myadmin/viewProduct.html')



# client side

def index(request):
    return render(request,'client/index.html')


def cartCheckout(request):
    try:
        all_items = request.session['cart']

        new_all_items =[]
        count =1
        grand_total = 0
        for item in all_items:
            dist = item
            grand_total+=item['totalPrice']
            dist['sno']= count
            count += 1
            new_all_items.append(dist)
        content ={'data':new_all_items,'grand_total':grand_total}
    except:
        content = {'data':'no'}
    return render(request, 'client/checkout.html', content)

def cart_inc_dec(request):
    id=request.GET['id']
    operation=request.GET['opt']
    print(id,operation)
    all_items = request.session['cart']
    for item in all_items:
        if item['id'] == id and operation=='plus':
            item['qty']=item['qty']+1
            item['totalPrice']=float(item['price'])* item['qty']
            break
        elif item['id'] == id and operation=='minus':
            print(item['qty'])
            if item['qty'] == 1:
                del all_items[all_items.index(item)]
            else:
                item['qty']=item['qty']-1
                item['totalPrice']=float(item['price'])* item['qty']
            break
    request.session['cart'] = all_items
    print(request.session['cart'])
    return HttpResponse('success')

def process_to_pay(request):
    total = 0
    for item in request.session['cart']:
        total += item['totalPrice']
    return render(request, 'client/processToPay.html', {'total':total})


@csrf_exempt
def payment_action(request):
    name = request.POST['name']
    email = request.POST['email']
    address = request.POST['address']
    total = request.POST['total']
    paymentmode = request.POST['paymentmode']
    mobile = request.POST['mobile']
    dateOfOrder = date.today()

    if paymentmode == 'Cash':
        payStatus = 'pending'
    else:
        payStatus = 'Done'

    conn = sqlite3.connect('db.sqlite3')
    cr = conn.cursor()
    Query_for_bill = f"insert into billing (`email`, `address`, `totalAmount`, `mobile`, `typeofbill`, `dateofpayment`, `paystatus`,`name`) values ('{email}', '{address}','{total}', '{mobile}','{paymentmode}','{dateOfOrder}', '{payStatus}','{name}')"
    cr.execute(Query_for_bill)
    conn.commit()

    select_query = "select bill_id from billing order by bill_id DESC"
    cr = conn.cursor()
    cr.execute(select_query)
    result = cr.fetchone()

    for item in request.session['cart']:
        query_detail = "insert into billDetail (`title`, `price`, `qty`, `total_price`, `billing_id`) values ('{}','{}','{}','{}','{}')".format(item['name'], item['price'], item['qty'] ,item['totalPrice'], result[0])
        cr = conn.cursor()
        cr.execute(query_detail)
        conn.commit()
    return JsonResponse({'billid':result[0]})

def thankspage(request):
    try:
        del request.session['cart']
    except:
        pass
    billid = request.GET['billid']
    return render(request, 'client/thankyou.html',{'billid': billid})

@csrf_exempt
def add_to_cart(request):
    try:
        all_items=request.session['cart']
    except:
        all_items=[]

    for item in all_items:
        if item['id'] == request.POST['id']:
            return HttpResponse("Fail")

    dist={
        'id':request.POST['id'],
        'name':request.POST['name'],
        'price':request.POST['price'],
        'image':request.POST['image'],
        'qty':1,
    }
    dist['totalPrice']=dist['qty']*float(dist['price'])
    all_items.append(dist)
    request.session['cart']=all_items
    print(request.session['cart'])

    grand_total =0
    for i in all_items:
        grand_total += i['totalPrice']
    return JsonResponse({'grand_total':grand_total, 'length':len(all_items)})


def viewCateogry(request):
    conn = sqlite3.connect('db.sqlite3')
    query = "select * from category"
    cr = conn.cursor()
    cr.execute(query)
    result = cr.fetchall()
    result_data = []
    for item in result:
        dist = {
            'id': item[0],
            'name': item[1],
            'description': item[2],
            'photo': item[3]
        }
        result_data.append(dist)
    return render(request,'client/showCateogry.html', {'data': result_data})


def viewProduct(request):
    conn = sqlite3.connect('db.sqlite3')
    query = "select * from category"
    cr = conn.cursor()
    cr.execute(query)
    result1 = cr.fetchall()
    result_data = []
    for item in result1:
        dist = {
            'id': item[0],
            'name': item[1],
            'description': item[2],
            'photo': item[3]
        }
        result_data.append(dist)

    id=request.GET['id']
    query = "Select * from products where category_id='{}'".format(id)
    conn = sqlite3.connect('db.sqlite3')
    cr = conn.cursor()
    cr.execute(query)
    result = cr.fetchall()
    product_list = []
    for item in result:
        dist={
            'id':item[0],
            'name':item[1],
            'price':item[2],
            'priceAfterDiscount':item[3],
            'brand':item[4],
            'photo':item[6],
        }
        product_list.append(dist)
    return render(request, 'client/products.html', {'data':product_list,'cateogry':result_data})



def contactUs(request):
    return render(request, 'client/mail.html')

# end of client side
