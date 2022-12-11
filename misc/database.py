import pymysql
from datetime import datetime

class Database:
    def __init__(self):
        self.connection = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='Dmitry9260304',
            database='car_rental'
        )
        
    def __get_datetime(self, date, time):
        if 'PM' in time:
            time = time.replace(' PM', '')
            time = time.split(':')
            time = f'{int(time[0]) + 12}*{time[1]}*00'
        else:
            time = time.replace(' AM', '').replace(':', '*')
            time += '*00'
        
        date = date.split('/')
        date = f'{date[2]}*{date[0]}*{date[1]}'
        date_time = f'{date}*{time}'
        return date_time
        
    def get_free_cars(self):
        cars = []
        with self.connection.cursor() as cursor:
            cursor.execute(f'SELECT * FROM cars WHERE status = 0')
            rows = cursor.fetchall()
            for row in rows:
                cars.append([row[0], f'{row[1]} {row[2]} - {row[3]}', row[3]])
        return cars
    
    def get_all_cars(self):
        cars = []
        with self.connection.cursor() as cursor:
            cursor.execute(f'SELECT * FROM cars')
            rows = cursor.fetchall()
            for row in rows:
                status = 'Бронь'
                if row[4] == 0:
                    status = 'Свободно'
                cars.append([row[0], f'{row[1]} {row[2]}', row[3], status])
        return cars
    
    def get_all_tariff(self):
        tariff = []
        with self.connection.cursor() as cursor:
            cursor.execute(f'SELECT * FROM tariffs')
            rows = cursor.fetchall()
            for row in rows:
                tariff.append([row[0], f'{row[1]} (${row[3]})'])
        return tariff
    
    def add_new_application(self, name, age, email, number, address, date, time, auto, tariff, date_end, time_end):
        user_id = 0
        with self.connection.cursor() as cursor:
            cursor.execute(f'SELECT * FROM clients WHERE name = "{str(name)}" AND age = {int(age)} AND phone_num = {int(number)}')
            users = cursor.fetchall()
            if users:
                user_id = users[0][0]
            else: 
                cursor.execute(f'INSERT INTO clients (client_status_id, name, age, phone_num, email, address) '
                               f'VALUES (1, "{str(name)}", {int(age)}, {int(number)}, "{str(email)}", "{str(address)}")')
                self.connection.commit()
                cursor.execute(f'SELECT * FROM clients WHERE name = "{str(name)}" AND age = {int(age)} AND phone_num = {int(number)}')
                users = cursor.fetchall()
                user_id = users[0][0]
            
            datetime_start = self.__get_datetime(date, time)
            datetime_end = self.__get_datetime(date_end, time_end)
                
            cursor.execute(f'INSERT INTO application (rental_status_id, date_start, date_end, cars_id, clients_id, tariffs_id)'
                           f'VALUES (1, "{datetime_start}", "{datetime_end}", {auto}, {user_id}, {tariff})')
            self.connection.commit()
            
    def get_active_rental(self):
        # now = datetime.now()
        # now = f'{now.year}*{now.month}*{now.day}*{now.hour}*{now.minute}*{now.second}'
        active = []
        with self.connection.cursor() as cursor:
            cursor.execute(f'SELECT cars.label, cars.model, application.date_start, application.date_end, clients.name FROM cars '
                            f'INNER JOIN application ON application.cars_id = cars.id '
                            f'INNER JOIN clients ON clients.id = application.clients_id '
                            f'WHERE cars.status = 1')
            rows = cursor.fetchall()
            for row in rows:
                active.append([f'{row[0]} {row[1]}', str(row[2]), str(row[3]), row[4]])
        return active
    
    def add_tariff(self, title, info, price):
        with self.connection.cursor() as cursor:
            cursor.execute(f'INSERT INTO tariffs (title, information, price) VALUES ("{title}", "{info}", {float(price)})')
            self.connection.commit()
    
    def add_car(self, title, model, docs):
        with self.connection.cursor() as cursor:
            cursor.execute(f'INSERT INTO cars (label, model, documentation, status) VALUES ("{title}", "{model}", "{docs}", 0)')
            self.connection.commit()
            
    def get_active_orders(self):
        orders = []
        with self.connection.cursor() as cursor:
            cursor.execute(f'SELECT application.id, clients.name, cars.label, cars.model, rental_status.title, application.date_start FROM application '
                            f'INNER JOIN clients ON application.clients_id = clients.id '
                            f'INNER JOIN rental_status ON rental_status.id = application.rental_status_id '
                            f'INNER JOIN cars ON cars.id = application.cars_id '
                            f'WHERE cars.status = 1')
            rows = cursor.fetchall()
            for row in rows:
                orders.append([row[0], f'{row[1]} | {row[2]} {row[3]} | {row[4]} | {row[5]}'])
        return orders
        
    def get_fines(self):
        fines = []
        with self.connection.cursor() as cursor:
            cursor.execute('SELECT * FROM fines')
            for row in cursor.fetchall():
                fines.append([row[0], f'{row[1]} | {row[2]} | ${row[3]}'])
        return fines
    
    def add_fines_has_application(self, app, fines):
        with self.connection.cursor() as cursor:
            cursor.execute(f'INSERT INTO application_has_fines (application_id, fines_id) VALUES ({app}, {fines})')
            self.connection.commit()