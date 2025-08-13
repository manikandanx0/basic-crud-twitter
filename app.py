from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config['SECRET_KEY'] = 'SteelBallRun07'  # Added secret key for sessions

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

db.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.get("/signup")
def handleGet():
    return render_template("create_account.html")

@app.route("/users")
@login_required  # Protect this route
def userList():
    users = db.session.execute(db.select(User).order_by(User.email)).scalars().all()
    for user in users:
        print(user.email, user.password, user.name, user.dob)

    return render_template("userlist.html", users=users)

@app.post("/signup")
def postReqHandler():
    name = request.form.get("fname")
    email = request.form.get("email")
    password = request.form.get("psw")
    dob_str = request.form.get("dob")

    try:
        dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
    except ValueError:
        flash("Invalid date format. Please use YYYY-MM-DD.", "error")
        return redirect(url_for('handleGet'))

    stmt = db.select(User).where(User.email == email)
    existing_user = db.session.execute(stmt).scalars().first()
    
    if existing_user:
        flash("Email already registered. Try a different one.", "error")
        return redirect(url_for('handleGet'))

    hashed_password = generate_password_hash(password)
    new_user = User(email=email, password=hashed_password, name=name, dob=dob)
    db.session.add(new_user)
    db.session.commit()
    
    flash("Account created successfully! Please log in.", "success")
    return redirect(url_for('login'))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        if not email or not password:
            flash("Please fill in all fields.", "error")
            return render_template("login.html")
        
        # Find user by email
        stmt = db.select(User).where(User.email == email)
        user = db.session.execute(stmt).scalars().first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash(f"Welcome back, {user.name}!", "success")
            
            # Redirect to next page if it exists, otherwise go to index
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash("Invalid email or password.", "error")
    
    return render_template("loginpage.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out successfully.", "info")
    return redirect(url_for('index'))

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)