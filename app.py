from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])

def index():

    result = []

    setting = []

    if request.method == "POST":

        bands = []

        performers = {}

        all_members = set()

        # 入力取得

        for i in range(6):

            band = request.form.get(f"band{i}")

            member = request.form.get(f"member{i}")

            if band:

                names = []

                if member:

                    names = [m.strip() for m in member.split(",") if m.strip()]

                performers[band] = names

                bands.append(band)

                all_members.update(names)

        # 全メンバー入力

        all_input = request.form.get("all_members")

        if all_input:

            all_members.update([m.strip() for m in all_input.split(",")])

        # 後輩

        juniors_input = request.form.get("juniors")

        juniors = []

        if juniors_input:

            juniors = [j.strip() for j in juniors_input.split(",")]

        # 回数カウント

        count = {m: 0 for m in all_members}

        # 候補取得（段階的緩和）

        def get_candidates(i, band):

            # ① 出演＋前後NG

            strict = []

            for m in all_members:

                ok = True

                for b, names in performers.items():

                    if m in names:

                        idx = bands.index(b)

                        if abs(idx - i) <= 1:

                            ok = False

                            break

                if ok:

                    strict.append(m)

            if len(strict) >= 2:

                return strict

            # ② 出演のみNG

            semi = []

            for m in all_members:

                if m not in performers[band]:

                    semi.append(m)

            if len(semi) >= 2:

                return semi

            # ③ 全員OK

            return list(all_members)

        # 割り当て

        for i, band in enumerate(bands):

            candidates = get_candidates(i, band)

            # 均等（少ない順）

            candidates.sort(key=lambda x: count[x])

            selected = []

            for m in candidates:

                if len(selected) < 2:

                    selected.append(m)

            # 後輩補充

            if len(selected) < 2:

                for j in juniors:

                    if j not in selected:

                        selected.append(j)

                    if len(selected) == 2:

                        break

            # 最終補完

            while len(selected) < 2:

                selected.append("未定")

            for m in selected:

                if m in count:

                    count[m] += 1

            result.append([band, selected[0], selected[1]])

        # セッティング係（回数少ない順）

        setting = sorted(count, key=lambda x: count[x])

    return render_template("index.html", result=result, setting=setting)

if __name__ == "__main__":

    app.run(debug=True)
 