from flask import Flask, render_template, request

DiemHocPhan = Flask(__name__)

@DiemHocPhan.route('/', methods=['POST', 'GET'])
def tinh_diem():
    values, error = kiem_tra()
    values["dtb"] = round(values["cc"] * 0.1  + values["gk"] * 0.3 + values["ck"] * 0.6, 2)
    if values["ck"] <= 1:
        values["xeploai"] = "F"
    else:
        values["xeploai"] = xep_loai(values["dtb"])

    return render_template("diemhocphan.html", values=values, error=error)

def xep_loai(dtb):
    if dtb >= 8.5:
        return "A"
    elif dtb >= 7:
        return "B"
    elif dtb >= 5.5:
        return "C"
    elif dtb >= 4:
        return "D"
    else:
        return "F"

def kiem_tra():
    values, error = {}, {}

    try:
        values["cc"] = float(request.form.get("cc", "0").strip())
        values["gk"] = float(request.form.get("gk", "0").strip())
        values["ck"] = float(request.form.get("ck", "0").strip())
    except ValueError:
        error["in"] = "Lỗi: Vui lòng nhập số hợp lệ"

    if values["cc"] < 0 or values["cc"] > 10:
        error["cc"] = "Lỗi: Điểm chuyên cần phải từ 0 đến 10"

    if values["gk"] < 0 or values["gk"] > 10:
        error["gk"] = "Lỗi: Điểm giữa kỳ phải từ 0 đến 10"

    if values["ck"] < 0 or values["ck"] > 10:
        error["ck"] = "Lỗi: Điểm cuối kỳ phải từ 0 đến 10"  

    return values, error

if __name__ == "__main__":
    DiemHocPhan.run(debug=True)