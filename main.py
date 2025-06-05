import os
from flask import Flask, flash, render_template, request, redirect, url_for
from dotenv import load_dotenv
from flask_hashing import Hashing
from models.user import User
from views.forms import LoginForm, AddUserForm
from flask_sqlalchemy import SQLAlchemy

load_dotenv()
app = Flask(__name__)
db = SQLAlchemy()
hashing = Hashing()

def create_app():
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    db.init_app(app)
    hashing.init_app(app)

    with app.app_context():
        db.create_all()
    
    return app


@app.route("/")
def index():
    return redirect(url_for("admin"))

@app.route("/admin", methods=["POST", "GET"])
def admin():
    form = AddUserForm()
    if request.method == "POST" and form.validate_on_submit():
        try:
            hashed_password = hashing.hash_value(form.password.data, salt="welcome")
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,

            user = User( username, email, password)
        
            db.session.add(user)
            db.session.commit()
            
            flash(f"User {user.username} added successfully", "success")
            return redirect(url_for("list_users"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error occurred while adding user: {e}")

    return render_template("admin.html", form=form)
    
    
@app.route("/users")
def list_users():
    users = db.session.execute(db.select(User)).scalars().all()
    if not users:
         flash("No users found.", "info")
   
    return render_template("user.html", users=users)

    


if __name__ == "__main__":
    create_app().run()
