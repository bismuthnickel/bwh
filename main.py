from flask import Flask, render_template, request, redirect, url_for
from os.path import exists
from os import listdir

app = Flask(__name__)

based = ["index.html","fail.html","success.html"]

@app.route("/",methods=["GET","POST"])
def index():
    def write():
        if request.form['pass'] != "":
            with open(f"templates/{request.form['name']}.txt","w") as f:
                f.write(request.form['pass'])
        with open(f"templates/{request.form['name']}.html","w") as f:
            f.write(request.form['payload'])
    if request.method == "POST":
        if request.form['name'] and request.form['payload']:
            if "%" in request.form['name'] or f"{request.form['name']}.html" in based:
                return render_template("fail.html")
            if exists(f"templates/{request.form['name']}.html"):
                if exists(f"templates/{request.form['name']}.txt"):
                    if request.form['pass'] == open(f"templates/{request.form['name']}.txt",'r').read():
                        write()
                        return render_template("success.html",title=request.form['name'])
                    return render_template("fail.html")
                write()
            write()
            return render_template("success.html",title=request.form['name'])
    else:
        rectory = listdir("templates")
        rectoryb = []
        for item in rectory:
            if item[-5:] != ".html":
                rectory.remove(item)
            if item in based:
                rectory.remove(item)
        for item in rectory:
            rectoryb.append(item[:-5])
        return render_template("index.html",files=rectoryb)
    
@app.route("/page")
def page():
    brake = 0
    if request.args.get('broken'):
        if request.args.get('broken') == "1":
            brake = 1
    if request.args.get('name'):
        if brake == 0:
            return render_template(f"{request.args.get('name')}.html")
        else:
            return "l bozo what else did you expect"
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=80,debug=True)