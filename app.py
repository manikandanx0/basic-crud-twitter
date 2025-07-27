from flask import Flask, render_template, request

from models import db, User


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

db.init_app(app)


with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.get("/signup")
def handleGet():
    return render_template("create_account.html")

# @app.route("/users")
# def listUsers():


@app.post("/signup")
def postReqHandler():
    email = request.form.get("email")
    password = request.form.get("psw")
    existing_user = User.query.filter_by(email=email).first() # type: ignore
    if existing_user:
        return "Email already registered. Try a different one."
    # print(f"Username: {username}, Password: {password}")
    
    new_user = User(email=email, password=password) #type: ignore
    db.session.add(new_user)
    db.session.commit()
    return "success"

if __name__ == "__main__":
    app.run(debug=True)
