# server/app.py
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

class MessageListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('body', type=str, required=True, help="Body is required")
    parser.add_argument('username', type=str, required=True, help="Username is required")

    def get(self):
        messages = Message.query.all()
        return [message.to_dict() for message in messages], 200

    def post(self):
        args = self.parser.parse_args()
        message = Message(body=args['body'], username=args['username'])
        db.session.add(message)
        db.session.commit()
        return message.to_dict(), 201

class MessageResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('body', type=str, help="Body is required")
    parser.add_argument('username', type=str, help="Username is required")

    def get(self, id):
        message = Message.query.filter_by(id=id).first()
        if not message:
            abort(404, message="Message not found")
        return message.to_dict(), 200

    def patch(self, id):
        message = Message.query.filter_by(id=id).first()
        if not message:
            abort(404, message="Message not found")
        args = self.parser.parse_args()
        if args['body'] is not None:
            message.body = args['body']
        if args['username'] is not None:
            message.username = args['username']
        db.session.commit()
        return message.to_dict(), 200

    def delete(self, id):
        message = Message.query.filter_by(id=id).first()
        if not message:
            abort(404, message="Message not found")
        db.session.delete(message)
        db.session.commit()
        return '', 204

api.add_resource(MessageListResource, '/messages')
api.add_resource(MessageResource, '/messages/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)