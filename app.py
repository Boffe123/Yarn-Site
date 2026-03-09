from flask import Flask, redirect, request, render_template, url_for

app = Flask(__name__)

# Set up database 


yarns = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/yarn_storage.html", methods=["GET", "POST"])
def yarn_storage():
    if request.method == "POST":
        name = request.form.get("name")
        type = request.form.get("type")
        color = request.form.get("color")
        image = request.form.get("image")
        
        if name and color and type:
            yarn = {
                "name": name,
                "type": type,
                "color": color,
                "image": image
            }
            yarns.append(yarn)
        return redirect(url_for("yarn_storage"))
    
    reversed_yarns = list(reversed(yarns))
    return render_template("yarn_storage.html", yarns=reversed_yarns)
if __name__ == "__main__":  
    app.run(debug=True)

