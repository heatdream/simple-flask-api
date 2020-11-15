from flask import Flask
from flask_restful import Api, Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from passgen import passgen


def send_reset_mail(email):
    senderEmail = "" #Email from youre EMail Account
    empfangsEmail = email
    msg = MIMEMultipart()
    msg['From'] = senderEmail
    msg['To'] = empfangsEmail
    msg['Subject'] = "Reset youre Password"
    code = passgen(length=6, punctuation=False, digits=True, letters=False, case='both')
    emailText = f"Use this code to reset youre Password: {code}"
    msg.attach(MIMEText(emailText, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)  # The Server Datas
    server.starttls()
    server.login(senderEmail, "")  # The Password
    text = msg.as_string()
    server.sendmail(senderEmail, empfangsEmail, text)
    server.quit()
    collection.update_one({'email': f'{email}'}, {'$set': {'code': int(code)}})


app = Flask(__name__)
api = Api(app)

reset_parser = reqparse.RequestParser()
reset_parser.add_argument('code', type=str, help='req. code', required=True)
reset_parser.add_argument('password', type=str, help='req. password', required=True)


do_reset_parser = reqparse.RequestParser()
do_reset_parser.add_argument('code', type=str, help='code', required=True)
do_reset_parser.add_argument('email', type=str, help='req email', required=True)


reset_pwd_parser = reqparse.RequestParser()
reset_pwd_parser.add_argument('email', type=str, help='email is required', required=True)

register_parser = reqparse.RequestParser()
register_parser.add_argument('username', type=str, help='req. username', required=True)
register_parser.add_argument('password', type=str, help='req. username', required=True)
register_parser.add_argument('email', type=str, help='req. email', required=True)

login_parser = reqparse.RequestParser()
login_parser.add_argument('username', type=str, help='req. username', required=True)
login_parser.add_argument('password', type=str, help='req. username', required=True)


cluster = MongoClient(YOURE-MONGODB-DATAS) # connection to youre DB

db = cluster['ClientDatabase']
collection = db['users']


@app.route('/')
def hallo():
    return 'Webservice running...'

class Do_Pwd_Reset(Resource):
    def post(self):
        args = do_reset_parser.parse_args()
        code = collection.find_one({'code': args['code']})
        if code == args['code']:
            email = args['email']
            collection.update_one({'email': email}, {'$unset': {'password': ''}})
            return {'status': 'reseted password'}, 200

    def put(self):
        args = reset_parser.parse_args()
        user_code = args['code']
        password = args['password']
        collection.update_one({'code': int(user_code)}, {'$set': {'password': generate_password_hash(password,
                                                   method='pbkdf2:sha256',
                                                   salt_length=8)}})
        collection.update_one({'code': int(user_code)}, {'$unset': {'code': ''}})
        return {'status': 'updated password'}, 200




class ResetPwd(Resource):
    def post(self):
        args = reset_pwd_parser.parse_args()
        email = args['email']
        account = collection.find_one({'email': email})
        if not account:
            return {'status': 'no account with this email'}, 404
        send_reset_mail(email)


class Login(Resource):
    def post(self):
        args = login_parser.parse_args()
        username = args['username']
        password = args['password']
        user = collection.find_one({'_id': username})

        if not user:
            return {'message': 'wrong username'}, 401

        if user['_id'] != username and not check_password_hash(user['password'],
                                                               password):
            return {'message': 'wrong data'}, 401
        return {'message': 'logged_in'}, 200


class Register(Resource):
    def get(self):
        return {'message': 'Method Not Allowed'}, 405

    def post(self):
        args = register_parser.parse_args()
        username = args['username']
        password = args['password']
        email_ = args['email']
        user = collection.find_one({'_id': username})
        email = collection.find_one({'email': email_})

        if user or email:
            return {'message': 'Username or Email already exist'}, 400

        collection.insert_one({
            '_id': username,
            'email': email_,
            'password': generate_password_hash(password,
                                               method='pbkdf2:sha256',
                                               salt_length=8)
        })
        return {'message': 'created'}, 201


api.add_resource(Login, '/login')
api.add_resource(Register, '/register')
api.add_resource(ResetPwd, '/resetpwd')
api.add_resource(Do_Pwd_Reset, '/doreset')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
