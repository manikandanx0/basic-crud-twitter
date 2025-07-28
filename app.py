from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash
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

@app.route("/users")
def userList():
    users = db.session.execute(db.select(User).order_by(User.email)).scalars().all()
    for user in users:
        print(user.email, user.password)

    return render_template("userlist.html")



@app.post("/signup")
def postReqHandler():
    email = request.form.get("email")
    password = request.form.get("psw")
    stmt = db.select(User).where(User.email == email)
    existing_user = db.session.execute(stmt).scalars().first()
 # type: ignore
    if existing_user:
        return "Email already registered. Try a different one."
    # print(f"Username: {username}, Password: {password}")

    hashed_password = generate_password_hash(password)  # 🔐 HASHING HERE
    new_user = User(email=email, password=password) #type: ignore
    db.session.add(new_user)
    db.session.commit()
    return "success"



if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
