from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])

def index():

    schedule = None

    if request.method == "POST":

        members = request.form["members"].split(",")

        bands = request.form["bands"].split(",")

        schedule = {}

        i = 0

        for band in bands:

            schedule[band] = [

                members[i % len(members)],

                members[(i+1) % len(members)]

            ]

            i += 2

    return render_template("index.html", schedule=schedule)

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
 