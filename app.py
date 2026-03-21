from flask import Flask, redirect, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:bibi0086@localhost:5432/yarn_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = "static/uploads"

db =SQLAlchemy(app)


# Set up database 


class Yarn(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    type = db.Column(db.String(20), nullable = False)
    color = db.Column(db.String(20),nullable = False)
    image = db.Column(db.String(500), nullable = False)



@app.route("/wishlist.html")
def wishlist():
    return render_template("wishlist.html")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/yarn_storage.html", methods=["GET", "POST"])
def yarn_storage():
    if request.method == "POST":
        name = request.form.get("name")
        type = request.form.get("type")
        color = request.form.get("color")


        file = request.files.get("image")

        filename = None

        if file and filename != "":
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath) 
        
        if name and color and type:
            new_yarn = Yarn(
                name = name,
                type = type,
                color = color,
                image = filename
            )
            db.session.add(new_yarn)
            db.session.commit()
        return redirect(url_for("yarn_storage"))
    yarns= Yarn.query.order_by(Yarn.id.desc()).all()
   
    return render_template("yarn_storage.html", yarns=yarns)
if __name__ == "__main__": 
    with app.app_context():
        db.create_all() 
    app.run(debug=True)

