
from flask_restful import Resource
from flask_restful import fields, marshal_with, reqparse
from application.database import db
from application.models import User, Article
from application.validation import NotFoundError, BusinessValidationError

# suing marshal_with, so that we don't create JSON on the Fly.
output_fields = {
    "user_id" : fields.Integer,
    "username" : fields.String,
    "email" : fields.String,
}

# creating request parser so that we don't have to write the same code again and again.
# instead of doing "request.parse.json"
create_user_parser = reqparse.RequestParser()
create_user_parser.add_argument("username")
create_user_parser.add_argument("email")

update_user_parser = reqparse.RequestParser()
update_user_parser.add_argument("email")


class UserAPI(Resource):
    # Format the return JSON
    @marshal_with(output_fields)
    def get(self,username):
        # Get the username
        # print("In UserAPI GET method",username)
        # Get the User from database based on username
        user = db.session.query(User).filter(User.username == username).first()
        if user: 
            # return a valid user JSON
            return user
        else:
            raise NotFoundError(status_code = 404)
    @marshal_with(output_fields)
    def put(self,username):
        args = update_user_parser.parse_args()
        email = args.get("email",None)

        if email is None:
            raise BusinessValidationError(status_code = 400, error_code = "BE1002", error_message = "email is required")
        if "@" not in email:
            raise BusinessValidationError(status_code = 400, error_code = "BE1003", error_message = "Invalid email")
        # check if there already exists a user with the same email
        user = db.session.query(User).filter(User.email == email).first()
        if user:
            raise BusinessValidationError(status_code = 400, error_code = "BE1006", error_message = "Duplicate email")
        # Check if the user exists
        user = db.session.query(User).filter(User.username == username).first()
        if user is None: 
            # raise a NotFoundError
            raise NotFoundError(status_code = 404)

        user.email = email
        db.session.add(user)
        db.session.commit()

        return user

    def delete(self,username):
        # Check if the user exists
        user = db.session.query(User).filter(User.username == username).first()
        if user is None: 
            # raise a NotFoundError
            raise NotFoundError(status_code = 404)
        # Check if there are articles for this user, if yes
        articles = Article.query.filter(Article.authors.any(username = username)).first()
        # throw error
        if articles:
            raise BusinessValidationError(status_code = 400, error_code = "BE1005", error_message = "Can't delete users, since there are articles written by the user.")
        # If no dependancy then delete the user
        db.session.delete(user)
        db.session.commit()
        return "",204

    def post(self):
        args = create_user_parser.parse_args()
        username = args.get("username",None)
        email = args.get("email",None)
        if username is None:
            raise BusinessValidationError(status_code = 400, error_code = "BE1001", error_message = "username is required")
        
        if email is None:
            raise BusinessValidationError(status_code = 400, error_code = "BE1002", error_message = "email is required")
        
        if "@" not in email:
            raise BusinessValidationError(status_code = 400, error_code = "BE1003", error_message = "Invalid email")

        user = db.session.query(User).filter((User.username == username) | (User.email == email)).first()
        if user:
            raise BusinessValidationError(status_code = 400, error_code = "BE1004", error_message = "Duplicate user")
        
        new_user = User(username = username,email = email)
        db.session.add(new_user)
        db.session.commit()
        return "",201
