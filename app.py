import pymongo
from pymongo import MongoClient
# from flask import Flask, jsonify
import bson.json_util as json_util
import json
import certifi

from flask import Flask, render_template, request, url_for, redirect, session
import bcrypt

client = MongoClient("mongodb+srv://admin:rootadmin@cluster0.uzp3f5v.mongodb.net/logindb?retryWrites=true&w=majority", tlsCAFile=certifi.where())

db = client["logindb"]
records = db["logindata"]

app = Flask(__name__,template_folder="templates")

app.secret_key = "Desafio"

@app.route("/login", methods=["POST", "GET"])
def login():
    message = 'Entre com seu email e senha'
    if "email" in session:
        return redirect('/')
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        email_found = records.find_one({"email": email})
        password_found = records.find_one({"password": password})
        login = records.find_one({"email": email},{"_id":0,"login":1})

        if email_found and password_found:
            email_val = email_found['email']
            session["email"] = email_val
            session["login"] = login
            return redirect('/')
        else:
            message = 'Email ou senha não encontrado'
            return render_template('login.html', message=message)
    else:
        return render_template('login.html', message=message)

@app.route('/')
def logged_in():
    if "email" in session:
        message = 'Entre com seu email e senha'

        cluster = MongoClient(
        "mongodb+srv://admin:rootadmin@cluster0.uzp3f5v.mongodb.net/materia?retryWrites=true&w=majority",
        tlsCAFile=certifi.where())

        dbmateria = cluster["materia"]
        records = dbmateria["records"]

        x = records.find()
        y=json_util.dumps(x,default=json_util.default)
        return json.loads(y)
    else:
        return redirect(url_for("login"))

@app.route("/logout", methods=["POST", "GET"])
def logout():
    message = 'Entre com seu email e senha'
    if "email" in session:
        session.pop("email", None)
        return render_template("signout.html")
    else:
        return render_template('index.html')

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080, debug=True)