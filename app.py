from flask import Flask, render_template, url_for, request
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.get("/signup")
def handleGet():
    return render_template("create_account.html")

@app.post("/signup")
def postReqHandler():
    username = request.form.get("email")
    password = request.form.get("psw")
    print(f"Username: {username}, Password: {password}")
    return "success"

if __name__ == "__main__":
    app.run(debug=True)
