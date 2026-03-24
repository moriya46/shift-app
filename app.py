from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])

def index():

    result = []

    setting = []

    if request.method == "POST":

        all_members = request.form.get("all_members", "").split(",")

        all_members = [m.strip() for m in all_members if m.strip()]

        i = 0

        used = []

        while True:

            band = request.form.get(f"band{i}")

            member = request.form.get(f"member{i}")

            if not band:

                break

            # 出演者を分割

            members = []

            if member:

                members = member.split(",")

                members = [m.strip() for m in members if m.strip()]

            # 2人だけ選ぶ

            selected = []

            for m in members:

                if m not in selected:

                    selected.append(m)

                if len(selected) == 2:

                    break

            # 足りない場合

            while len(selected) < 2:

                selected.append("未定")

            result.append([band, selected[0], selected[1]])

            used.extend(selected)

            i += 1

        # セッティング係（出演してない人）

        setting = [m for m in all_members if m not in used]

    return render_template("index.html", result=result, setting=setting)

if __name__ == "__main__":

    app.run()
 