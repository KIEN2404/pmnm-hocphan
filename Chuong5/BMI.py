from flask import Flask, render_template, request

BMI = Flask(__name__)

@BMI.route('/', methods=['POST', 'GET'])
def tinh_bmi():
    values, error = {}, {}

    try:
        values["cao"] = float(request.form.get("cao", "1").strip())
        values["nang"] = float(request.form.get("nang", "1").strip())
    except ValueError:
        error["in"] = "Lỗi: Vui lòng nhập số hợp lệ"

    if values["cao"] < 50 or values["cao"] > 250: 
        error["cao"] = "Lỗi: Chiều cao phải từ 50 đến 250"
        
    if values["nang"] < 10 or values["nang"] > 300:
        error["nang"] = "Lỗi: Cân nặng phải từ 10 đến 300"

    values["bmi"] = round(values["nang"] / (values["cao"]/100)**2, 1)

    if values["bmi"] < 18.5:
        values["xeploai"] = "thieu can"
        values["mau"] = "vang"
    elif values["bmi"] < 23:
        values["xeploai"] = "binh thuong"
        values["mau"] = "xanh"
    elif values["bmi"] < 25:
        values["xeploai"] = "thua can"
        values["mau"] = "vang"
    else:
        values["xeploai"] = "beo phi"
        values["mau"] = "do"

    return render_template("bmi.html", values=values, error=error)


if __name__ == "__main__":
    BMI.run(debug=True)