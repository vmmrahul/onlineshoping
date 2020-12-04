from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import sqlite3
from django.contrib import messages


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
            'description': item[2]
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
    id = request.GET['id']
    name = request.GET['name']
    description = request.GET['description']
    query = "update category set name = '{}', description = '{}' where id ={}".format(name, description, id)

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
