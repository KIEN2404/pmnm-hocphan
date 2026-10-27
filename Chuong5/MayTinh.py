from flask import Flask, render_template, request

MayTinh = Flask(__name__)

@MayTinh.route('/', methods=['POST', 'GET'])
def tinh_toan():
    values, error = {"a" : 0, "b": 0, "op" : "", "kq" : 0}, {}

    if request.method == "POST":
        values["a"] = float(request.form.get("a", 0).strip())
        values["b"] = float(request.form.get("b", 0).strip())
        values["op"] = request.form.get("pheptinh", "").strip()

        if values["op"] == "+":
            values["kq"] = values["a"] + values["b"]
        elif values["op"] == "-":
            values["kq"] = values["a"] - values["b"]
        elif values["op"] == "*":
            values["kq"] = values["a"] * values["b"]
        elif values["op"] == "/":
            try:
                values["kq"] = values["a"] / values["b"]
            except ZeroDivisionError:
                error["kq"] = "Lỗi: Không thể chia cho 0"

    return render_template("cal.html", values=values, error=error)

if __name__ == "__main__":
    MayTinh.run(debug=True)