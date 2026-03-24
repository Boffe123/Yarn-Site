from flask import Flask, redirect, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename
from datetime import datetime


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
    y_brand = db.Column(db.String(20), nullable = False)
    y_grams = db.Column(db.Integer, nullable = False)
    y_weight = db.Column(db.Integer, nullable = False)
    y_length = db.Column(db.Integer, nullable = False)
    



class Projects(db.Model):
    p_id = db.Column(db.Integer, primary_key=True)
    p_name = db.Column(db.String(50), nullable=False)
    p_due_date = db.Column(db.Date, nullable=False)
    p_description = db.Column(db.Text, nullable=False)
# Routes


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/wishlist.html")
def wishlist():
    return render_template("wishlist.html")

@app.route("/delete_yarn/<int:y_id>", methods=["POST"])
def delete_yarn(y_id):
    yarn = Yarn.query.get_or_404(y_id)

    db.session.delete(yarn)
    db.session.commit()

    return redirect(url_for("yarn_storage"))

@app.route("/yarn_storage.html", methods=["GET", "POST"])
def yarn_storage():
    if request.method == "POST":
        name = request.form.get("name")
        yarn_type = request.form.get("type")
        color = request.form.get("color")
        brand = request.form.get("brand")
        grams = int(request.form.get("grams"))
        weight = int(request.form.get("weight"))
        length = int(request.form.get("length"))

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
                y_image=filename,
                y_brand = brand,
                y_grams = grams,
                y_weight = weight,
                y_length = length
            )
            db.session.add(new_yarn)
            db.session.commit()

        return redirect(url_for("yarn_storage"))
    
    sort = request.args.get("sort", "id")
    direction = request.args.get("direction", "desc")

    filter_field = request.args.get("filter_field")
    filter_value = request.args.get("filter_value")

    sort_map = {
    "id": Yarn.y_id,
    "name": Yarn.y_name,
    "type": Yarn.y_type,
    "color": Yarn.y_color,
    "brand": Yarn.y_brand,
    "grams": Yarn.y_grams,
    "weight": Yarn.y_weight,
    "length": Yarn.y_length
    }
    
    column = sort_map.get(sort, Yarn.y_id)

    if direction == "asc":
        column = column.asc()
    else:
        column = column.desc()    

    query = Yarn.query

    if filter_field and filter_value:
        if filter_field == "color":
            query = query.filter(Yarn.y_color.ilike(f"%{filter_value}%"))
        elif filter_field == "type":
            query = query.filter(Yarn.y_type.ilike(f"%{filter_value}%"))
        elif filter_field == "brand":
            query = query.filter(Yarn.y_brand.ilike(f"%{filter_value}%"))
        elif filter_field == "grams":
            query = query.filter(Yarn.y_grams == int(filter_value))
        elif filter_field == "weight":
            query = query.filter(Yarn.y_weight == int(filter_value))
        elif filter_field == "length":
            query = query.filter(Yarn.y_length == int(filter_value))
            
    query = query.order_by(column)
    yarns = query.all()
    return render_template("yarn_storage.html", yarns=yarns)


@app.route("/projects.html", methods=["GET", "POST"])
def projects():
    if request.method == "POST":
        name = request.form.get("name")
        due_date_str = request.form.get("due_date")
        parsed_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
        description = request.form.get("description")

        if name and parsed_date and description:
            new_project = Projects(
            p_name=name,
            p_due_date=parsed_date,
            p_description=description
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