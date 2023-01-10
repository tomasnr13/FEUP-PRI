from flask import Flask, render_template, request, redirect, url_for, session
import search

app = Flask(__name__)
app.secret_key = "#$%#$%^%^BFGBFGBSFGNSGJTNADFHH@#%$%#T#FFWF$^F@$F#$FW"

@app.route("/")
def index():
	return render_template("index.html")

def maptobool(value):
    if value == "on":
        return True
    return False

@app.route("/search", methods=["POST", "GET"])
def searchr():
    results=[]
    query=""
    if request.method == "POST":
        query = request.form["query"]
        print("heree")
        print(query)
        sort_a = request.form.get("sort_a")
        print(sort_a)
        sort_a = maptobool(sort_a)
        print(sort_a)
        sort_d = request.form.get("sort_d")
        sort_d = maptobool(sort_d)
        print(sort_d)
        sort_la = request.form.get("sort_la")
        sort_la = maptobool(sort_la)
        sort_ld = request.form.get("sort_ld")
        sort_ld = maptobool(sort_ld)

        q_op = request.form.get("q_op")
        q_op = maptobool(q_op)
        print(q_op)
        # n_rows = request.form.get("n_rows", type = int)
        # if n_rows is None:
        #     n_rows = 200
    
        tamjokes = request.form.get("tamjokes")
        print("tamjokes")
        print(tamjokes)
        tamjokes = maptobool(tamjokes)
        print(tamjokes)
        antijokes = request.form.get("antijokes")
        antijokes = maptobool(antijokes)
        jokes = request.form.get("jokes")
        jokes = maptobool(jokes)
        otherjokes = request.form.get("otherjokes")
        otherjokes = maptobool(otherjokes)

        punch = request.form.get("punch")
        punch = maptobool(punch)
        dialog = request.form.get("dialog")
        dialog = maptobool(dialog)
        people = request.form.get("people")
        people = maptobool(people)
        positive = request.form.get("positive")
        positive = maptobool(positive)
        negative = request.form.get("negative")
        negative = maptobool(negative)
        
        results = search.querysolr(query,sort_a, sort_d, False, False, q_op, 20, tamjokes, antijokes, jokes, otherjokes,punch, dialog, people, positive, negative)
        session["results"] = results
        session["query"] = query
        return redirect(url_for("searchr"))
    print(session["results"])
    return render_template("search.html", results=session["results"], query=session["query"])


if __name__ == '__main__':
	app.run(debug=True)