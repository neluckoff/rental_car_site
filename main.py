from flask import Flask, render_template, url_for, request, redirect
from misc.database import Database


app = Flask(__name__)
db = Database()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', 
                           free_cars=db.get_free_cars(), 
                           tariffs=db.get_all_tariff(),
                           all_cars=db.get_all_cars())
    
    
@app.route('/detail', methods=['GET'])
def detail():
    return render_template('detail.html')

@app.route('/booking', methods=['GET'])
def booking():
    return render_template('booking.html', 
                           free_cars=db.get_free_cars(), 
                           tariffs=db.get_all_tariff())
    
@app.route('/admin', methods=['GET'])
def admin():
    return render_template('admin.html', active_rent=db.get_active_rental(), 
                           orders=db.get_active_orders(), 
                           fines=db.get_fines())


@app.route('/admin/add_tariff', methods=['POST'])
def admin_tariff():
    name = request.form['name']
    info = request.form['info']
    price = request.form['price']
    db.add_tariff(name, info, price)
    return redirect('/admin')


@app.route('/admin/add_car', methods=['POST'])
def admin_car():
    label = request.form['label']
    model = request.form['model']
    docs = request.form['docs']
    db.add_car(label, model, docs)
    return redirect('/admin')

@app.route('/admin/add_fines', methods=['POST'])
def admin_fines():
    order = request.form['order']
    fines = request.form['fines']
    db.add_fines_has_application(order, fines)
    return redirect('/admin')
    
    
@app.route('/booking/add', methods=['POST'])
def booking_add():
    name = request.form['name']
    age = request.form['age']
    email = request.form['mail']
    number = request.form['number']
    address = request.form['address']
    date = request.form['date']
    time = request.form['time']
    auto = request.form['auto']
    tariff = request.form['tariff']
    date_end = request.form['date2']
    time_end = request.form['time2']
    db.add_new_application(name, age, email, number, address, date, time, auto, tariff, date_end, time_end)
    return redirect('/booking')


if __name__ == '__main__':
    app.run()