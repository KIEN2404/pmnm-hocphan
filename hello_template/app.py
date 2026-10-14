from datetime import date

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/hello/<name>")
def hello(name):
    return render_template(
                "hello.html",
                name=name,
                skills=["Python", "Flask"]
            )

@app.route("/base")
def base():
    return render_template("base.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.context_processor
def inject_globals():
    return {
        "site_name": "MiniBlog",
        "current_year": date.today().year,
    }       

if __name__ == "__main__":
    app.run(debug=True)