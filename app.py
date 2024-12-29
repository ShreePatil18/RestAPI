from flask import Flask, request,jsonify
from flask_restful import Api,Resource
import mysql.connector
from flask_jwt_extended import JWTManager, create_access_token,jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt

import uuid


app=Flask(__name__)


app.config['JWT_SECRET_KEY']='codingtest'

api=Api(app)
bcrypt=Bcrypt(app)

jwt=JWTManager(app)

db_config = {
    'host': '127.0.0.1',
    'port':'3306',
    'user': 'root',
    'password': 'Shreyash@18',
    'database': 'caller'
}


def get_db_connection():
    return mysql.connector.connect(**db_config)

#logic for registering a user
class register_user(Resource):
    def post(self):
        data = request.get_json()
        name = data.get('name')
        password = data.get('password')
        email = data.get('email')
        phone_no = data.get('phone')
        if not phone_no or not password:
            return {'error': 'Phone number and password are required'}, 400

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (name, password,email,phone_no) VALUES (%s, %s,%s,%s)', (name, hashed_password,email,phone_no))
            conn.commit()
            return {'message': 'User registered successfully'}, 201
        except mysql.connector.IntegrityError:
            return {'error': 'Phone number already exists'}, 409
        finally:
            cursor.close()
            conn.close()


#logic for login
class login(Resource):
    def post(self):
        data = request.get_json()
        phone_no = data.get('phone')
        password = data.get('password')

        if not phone_no or not password:
            return {'error': 'Phone number and password are required'}, 400
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM users WHERE phone_no = %s', (phone_no,))
            user = cursor.fetchone()

            if user and bcrypt.check_password_hash(user['password'], password):
                access_token = create_access_token(identity=str(user['id']))
                return {'access_token': access_token}, 200
            else:
                return {'error': 'Invalid username or password'}, 401
        finally:
            cursor.close()
            conn.close()

#logic for searcching a user and then also looking for spam table for the same.
class search_user(Resource):
    @jwt_required()  
    def get(self):
        data = request.get_json()
        phone_no = data.get('phone')

        if not phone_no:
            return {'error': 'Phone number is required'}, 400

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            # Search for the user by phone number
            cursor.execute('SELECT id, name, phone_no FROM users WHERE phone_no = %s', (phone_no,))
            user = cursor.fetchone()

            if user:
               
                cursor.execute('''
                    SELECT COUNT(*) AS spam_count
                    FROM SpamRecord
                    WHERE phone_number = %s
                ''', (phone_no,))
                spam_count = cursor.fetchone()['spam_count']

                
                return {
                    'id': user['id'],
                    'name': user['name'],
                    'phone_no': user['phone_no'],
                    'marked_as_spam_by': spam_count
                }, 200
            else:
                return {'message': 'User not found'}, 404

        except mysql.connector.Error as err:
            return {'error': f"Database error: {err}"}, 500

        finally:
            cursor.close()
            conn.close()

#adding number to spam folder , the looged in userr is considered as marking user.
class addspam(Resource):
    @jwt_required()
    def post(self):
        data=request.get_json()
        phone_no=data.get('phone')
        marked_by = get_jwt_identity()

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Generate a UUID for the spam record
            spam_id = str(uuid.uuid4())

            # Insert the spam record into the database
            cursor.execute('''
                INSERT INTO SpamRecord (id, phone_number, marked_by)
                VALUES (%s, %s, %s)
            ''', (spam_id, phone_no, marked_by))

            conn.commit()

            return {'message': 'Phone number marked as spam successfully'}, 201

        except mysql.connector.Error as err:
            return {'error': f"Error: {err}"}, 500

        finally:
            cursor.close()
            conn.close()



api.add_resource(register_user, '/users/register')
api.add_resource(login, '/users/login')
api.add_resource(search_user, '/users/search')
api.add_resource(addspam, '/users/addspam')

if __name__ == '__main__':
    app.run(debug=True)