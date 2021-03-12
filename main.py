from flask import Flask,render_template,flash,redirect,url_for,request, Response
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
from wtforms import Form,StringField,PasswordField, validators
from flask_ngrok import run_with_ngrok
import cv2
import time
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}/db.db'.format(os.getcwd())
app.secret_key= "demirai"

run_with_ngrok(app)

db = SQLAlchemy(app)


def gen(cap):

    while cap.isOpened():
        ret, img = cap.read()
        if ret == True:
            img = cv2.resize(img, (0,0), fx=0.5, fy=0.5) 
            frame = cv2.imencode('.jpg', img)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else: 
            break


@app.route("/video_feed/<string:idd>")
def video_feed(idd):

    cap_temp=cap[int(idd)]

    return Response(gen(cap_temp),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/",methods =["GET","POST"])
def login():


    form = LoginForm(request.form)
    global cap

    if request.method == "POST":

        button = request.form['submit']
        if button=="User":

            return redirect(url_for("register"))

        username_entered = form.username.data
        password_entered = form.password.data
        
        database = Db.query.filter_by(username = username_entered).first()


        if database==None:

            flash("Wrong username","danger")
            return redirect(url_for("login"))

        elif sha256_crypt.verify(password_entered,database.password):
            
            cap=[]

            for i in range(0,10):

                if cv2.VideoCapture(i).isOpened():

                    cap.append(cv2.VideoCapture(i))

                cv2.VideoCapture(i).release()

            flash("Login successful.","success")
            return render_template("capture.html", count=len(cap))

        else:

            flash("Wrong password","danger")
            return redirect(url_for("login"))

    return render_template("login.html",form = form)


@app.route("/register",methods = ["GET","POST"])
def register():

    form = RegisterForm(request.form)

    if request.method == "POST" and form.validate():

        button = request.form['submit']
        if button=="Login":

            return redirect(url_for("login"))

        username = form.username.data
        password = sha256_crypt.encrypt(form.password.data)
        sudo_password_input= form.sudo_password_input.data

        sudo_password = open("Sudo.txt","r+")
        temp=sudo_password.read().split("=")
        sudo_password=temp[1]
        sudo_password = sudo_password.replace(sudo_password[len(sudo_password)-1],"")

        if str(sudo_password_input)==str(sudo_password):

            if button=="Register":

                newUser = Db(username=username, password=password)

                db.session.add(newUser)
                db.session.commit()

                flash("Registration Successful","success")
                return redirect(url_for("login"))

            else:

                deleteUser = Db.query.filter_by(username = username).first()

                if deleteUser==None:

                    flash("Wrong username","danger")
                    return redirect(url_for("register"))

                elif sha256_crypt.verify(form.password.data,deleteUser.password):

                    db.session.delete(deleteUser)
                    db.session.commit()

                    flash("User successfully deleted","success")
                    return redirect(url_for("login"))

                else:

                    flash("Wrong password","danger")
                    return redirect(url_for("register"))

        else:

            flash("Wrong sudo password","danger")
            return redirect(url_for("register"))

    else:
        return render_template("register.html",form = form)


class RegisterForm(Form):

    username = StringField("Username")
    password = PasswordField("Password",)
    sudo_password_input = PasswordField("Sudo password")

class LoginForm(Form):

    username = StringField("Username")
    password = PasswordField("Password")


class Db(db.Model):

    username = db.Column(db.String(80), primary_key=True)
    password = db.Column(db.String(80))


if __name__ == "__main__":

    db.create_all()
    app.run()


