from flask import Flask, redirect, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:bibi0086@localhost:5432/yarn_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = "static/uploads"

db = SQLAlchemy(app)


os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


# Models


class Yarn(db.Model):
    y_id = db.Column(db.Integer, primary_key=True)
    y_name = db.Column(db.String(50), nullable=False)
    y_type = db.Column(db.String(20), nullable=False)
    y_color = db.Column(db.String(20), nullable=False)
    y_image = db.Column(db.String(500), nullable=True)


class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False)


# Routes


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/wishlist.html")
def wishlist():
    return render_template("wishlist.html")


@app.route("/yarn_storage.html", methods=["GET", "POST"])
def yarn_storage():
    if request.method == "POST":
        name = request.form.get("name")
        yarn_type = request.form.get("type")
        color = request.form.get("color")

        file = request.files.get("image")
        filename = None

        if file and file.filename != "":
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

        if name and yarn_type and color:
            new_yarn = Yarn(
                y_name=name,
                y_type=yarn_type,
                y_color=color,
                y_image=filename
            )
            db.session.add(new_yarn)
            db.session.commit()

        return redirect(url_for("yarn_storage"))

    yarns = Yarn.query.order_by(Yarn.y_id.desc()).all()
    return render_template("yarn_storage.html", yarns=yarns)


@app.route("/projects.html", methods=["GET", "POST"])
def projects():
    if request.method == "POST":
        name = request.form.get("name")
        due_date = request.form.get("due_date")
        description = request.form.get("description")

        if name and due_date and description:
            new_project = Projects(
                name=name,
                due_date=due_date,
                description=description
            )
            db.session.add(new_project)
            db.session.commit()

        return redirect(url_for("projects"))

    all_projects = Projects.query.all()
    return render_template("projects.html", projects=all_projects)



# Run app


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)