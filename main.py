from flask import Flask, render_template, redirect, url_for, request, jsonify, make_response
from gevent.pywsgi import WSGIServer
from gevent import monkey

import db_driver

app = Flask(__name__)
app.json.ensure_ascii = False

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', e=e)

@app.route('/')
def index_page():
    return render_template('index.html')

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/service/menu/add', methods=['GET','POST'])
def service_add():
    if request.method == 'POST':
        id_service = request.form.get('id_service')
        name_service = request.form.get('name_service')
        cost_service = request.form.get('cost_service')
        ser = db_driver.add_service(id_service, name_service, cost_service)
        services = db_driver.get_service()
        return render_template('add_service.html', ser=ser, services=services)
    elif request.method == 'GET':
        services = db_driver.get_service()
        return render_template('add_service.html', services=services)
    return render_template('add_service.html', services=list())

@app.route('/service/menu/update', methods=['GET','POST'])
def service_update():
    if request.method == 'POST':
        id = request.form.get('id')
        name = request.form.get('name')
        cost = request.form.get('cost')
        ser = db_driver.update_service(id, name, cost)
        services = db_driver.get_service()
        return render_template('update_service.html', ser=ser, services=services)
    elif request.method == 'GET':
        services = db_driver.get_service()
        return render_template('update_service.html', services=services)
    return render_template('update_service.html', services=list())

@app.route('/service/menu/delete', methods=['GET','POST'])
def service_delete():
    if request.method == 'POST':
        id_service = request.form.get('id_service')
        ser = db_driver.delete_service(id_service)
        services = db_driver.get_service()
        return render_template('delete_service.html', ser=ser, services=services)
    elif request.method == 'GET':
        services = db_driver.get_service()
        return render_template('delete_service.html', services=services)
    return render_template('delete_service.html', services=list())

@app.route('/service/menu')
def servise_menu_page():
    return render_template('service_menu.html')

@app.route('/discount/menu')
def discount_menu_page():
    return render_template('discount_menu.html')

@app.route('/discount/menu/add', methods=['GET','POST'])
def discount_add():
    if request.method == 'POST':
        id = request.form.get('id')
        name = request.form.get('name')
        discount = request.form.get('discount')
        dis = db_driver.add_discount(id, name, discount)
        discount = db_driver.get_discount()
        return render_template('add_discount.html', dis=dis, discount=discount)
    elif request.method == 'GET':
        discount = db_driver.get_discount()
        return render_template('add_discount.html', discount=discount)
    return render_template('add_discount.html', discount=list())

@app.route('/discount/menu/delete', methods=['GET','POST'])
def discount_delete():
    if request.method == 'POST':
        id = request.form.get('id')
        dis = db_driver.delete_discount(id)
        discount = db_driver.get_discount()
        return render_template('delete_discount.html', dis=dis, discount=discount)
    elif request.method == 'GET':
        discount = db_driver.get_discount()
        return render_template('delete_discount.html', discount=discount)
    return render_template('delete_service.html', discount=list())

@app.route('/discount/menu/update', methods=['GET','POST'])
def discount_update():
    if request.method == 'POST':
        id = request.form.get('id')
        name = request.form.get('name')
        discount = request.form.get('discount')
        dis = db_driver.update_discount(id, name, discount)
        discount = db_driver.get_discount()
        return render_template('update_discount.html', dis=dis, discount=discount)
    elif request.method == 'GET':
        discount = db_driver.get_discount()
        return render_template('update_discount.html', discount=discount)
    return render_template('update_discount.html', discount=list())

@app.route('/department/menu')
def department_menu_page():
    return render_template('department_menu.html')

@app.route('/department/menu/add', methods=['GET','POST'])
def department_add():
    if request.method == 'POST':
        id = request.form.get('id')
        name = request.form.get('name')
        dep = db_driver.add_department(id,name)
        department = db_driver.get_department()
        return render_template('add_department.html', dep=dep, department=department)
    elif request.method == 'GET':
        department = db_driver.get_department()
        return render_template('add_department.html', department=department)
    return render_template('add_department.html', department=list())

@app.route('/department/menu/delete', methods=['GET','POST'])
def department_delete():
    if request.method == 'POST':
        id = request.form.get('id')
        dep = db_driver.delete_department(id)
        department = db_driver.get_department()
        return render_template('delete_department.html', dep=dep, department=department)
    elif request.method == 'GET':
        department = db_driver.get_department()
        return render_template('delete_department.html', department=department)
    return render_template('delete_department.html', department=list())

@app.route('/department/menu/update', methods=['GET','POST'])
def department_update():
    if request.method == 'POST':
        id = request.form.get('id')
        name = request.form.get('name')
        dep = db_driver.update_departent(id, name)
        department = db_driver.get_department()
        return render_template('update_department.html', dep=dep, department=department)
    elif request.method == 'GET':
        department = db_driver.get_department()
        return render_template('update_department.html', department=department)
    return render_template('update_department.html', department=list())

@app.route('/doc', methods=['GET'])
def doctors_page():
    doctors = db_driver.get_doctors()
    print(db_driver.get_doctors())
    return render_template('doctor.html', doctors=doctors)

@app.route('/menuPat')
def menuPat_page():
    return render_template('menuPat.html')

@app.route('/menuDoc')
def menuDoc_page():
    return render_template('menuDoc.html')


@app.route('/zapros', methods=['GET'])
def zapros_page():
    diagnosises = db_driver.get_diagnosises()
    return render_template('zapros.html', diagnosises=diagnosises)

@app.route('/zapros/updateDate', methods=['GET'])
def zapros_updateDate_page():
    return render_template('updateDate.html')

@app.route('/zapros/three', methods=['GET', 'POST'])
def zapros_three_page():
    if request.method == 'POST':
        date1 = request.form.get('date1')
        date2 = request.form.get('date2')
        incomes = db_driver.get_three_zapros(date1, date2)
        return render_template('zapros_three.html', incomes=incomes)
    return render_template('zapros_three.html', incomes=list())

@app.route('/zapros/two', methods=['GET', 'POST'])
def zapros_two_page():
    if request.method == 'POST':
        name = request.form.get('name')
        date1 = request.form.get('date1')
        date2 = request.form.get('date2')
        doc_lists = db_driver.get_two_zapros(name, date1, date2)
        return render_template('zapros_two.html', doc_lists=doc_lists)
    return render_template('zapros_two.html', doc_lists=list())

@app.route('/zapros/four', methods=['GET'])
def zapros_four_page():
    statics = db_driver.get_four_zapros()
    return render_template('zapros_four.html', statics=statics)

@app.route('/zapros/five', methods=['GET', 'POST'])
def zapros_five_page():
    if request.method == 'POST':
        id = request.form.get('id_patient')
        date = request.form.get('date')
        scores = db_driver.get_five_zapros(id, date)
        return render_template('zapros_five.html', scores=scores)
    return render_template('zapros_five.html', scores=list())


@app.route('/zapros/six', methods=['GET', 'POST'])
def zapros_six_page():
    if request.method == 'POST':
        id = request.form.get('id_patient')
        cards = db_driver.get_six_zapros(id)
        return render_template('zapros_six.html', cards=cards)
    return render_template('zapros_six.html', incomes=list())

@app.route('/zapros/seven',methods=['GET', 'POST'])
def zapros_seven_page():
    if request.method == 'POST':
        id = request.form.get('id_patient')
        lists = db_driver.get_seven_zapros(id)
        return render_template('zapros_seven.html', lists=lists)
    return render_template('zapros_seven.html', incomes=list())


@app.route('/zapros/eight', methods=['GET', 'POST'])
def zapros_eight_page():
    if request.method == 'POST':
        id = request.form.get('id_patient')
        ratings = db_driver.get_eight_zapros(id)
        return render_template('zapros_eight.html', ratings=ratings)
    return render_template('zapros_eight.html', incomes=list())



monkey.patch_all(ssl=False)
if __name__ == '__main__':
    gevent_server = WSGIServer(('localhost', 80), app)
    gevent_server.serve_forever()
