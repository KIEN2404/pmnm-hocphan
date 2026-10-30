from werkzeug.routing import BaseConverter, ValidationError
from flask import Flask, flash, redirect, request, session, url_for, render_template
from datetime import date

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, Email, EqualTo, ValidationError


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hihihaha'

@app.route('/')
def hello():
    return "Hello, World!"

@app.route('/chia_nhom')
def chia_nhom():
    so_bai = 12
    so_nhom = 2
    return f"Mỗi nhóm làm {so_bai / so_nhom} bài"

@app.route('/user/<username>')
def user_profile(username):
    return f"Trang ca nhan cua {username}"

@app.route('/square/<int:x>')
def square(x):
    return f"{x} squared is {x * x}"

class IntListConverter(BaseConverter):
    regex = r'\d+(?:,\d+)*'

    def to_python(self, value):
        return [int(x) for x in value.split(',')]

    def to_url(self, values):
        return ','.join(str(x) for x in values)

app.url_map.converters['list'] = IntListConverter

@app.route('/sum/<list:ls>')
def Sum(ls):
    total = 0
    for i in ls:
        total += i
    return f"sum = {total}"



#
#
# SO DIEM
STUDENTS = {
    "23T1020001": {"name": "Nguyen Van An", "lop": "K47A", 
                   "scores": {"PMMNM": 8.5, "CSDL": 7.0, "MMT": 9.0}},
    "23T1020002": {"name": "Trần Thị Bình", "lop": "K47A",
                   "scores": {"PMMNM": 6.0, "CSDL": 5.0, "MMT": 7.0}},
    "23T1020003": {"name": "Lê Hoàng Cường", "lop": "K47B",
                     "scores": {"PMMNM": 9.5, "CSDL": 9.0}},
    "23T1020004": {"name": "Phạm Minh Dũng", "lop": "K47B",
                     "scores": {"PMMNM": 4.0, "CSDL": 3.5, "MMT": 5.0}},
    "23T1020005": {"name": "Hoang Thu Hà", "lop": "K47A",
                     "scores": {}},
    "23T1020006": {"name": "Võ Quốc Khánh", "lop": "K47C",
                     "scores": {"PMMNM": 7.5, "MMT": 8.0}}
}

@app.route('/sodiem')
def sodiem():
    sinhvien = len(STUDENTS)
    solop = set()
    for i in STUDENTS:
        solop.add(STUDENTS[i]["lop"])

    return render_template("/sodiem/sodiem.html", sinhvien=sinhvien, solop=len(solop))

def xeploai(diem):
    if diem == -1:
        return "..."
    elif diem >= 8.0:
        return "Gioi"
    elif diem >= 6.5:
        return "Kha"
    elif diem >= 5.0:
        return "Trung binh"
    else:
        return "Yeu"

@app.route('/students')
@app.route('/students/<student_id>')
def students(student_id=None):
    lop = set()

    table = f"""
        <table border="1">
            <tr>
                <th>Ma SV</th>
                <th>Ho ten</th>
                <th>Lop</th>
                <th>DTB</th>
                <th>Xep loai</th>
            </tr>
    """
    for i in STUDENTS:
        lop.add(STUDENTS[i]["lop"])
        dtb = -1
        if STUDENTS[i]["scores"]:
            dtb = sum(STUDENTS[i]["scores"].values()) / len(STUDENTS[i]["scores"])

        if i == student_id or STUDENTS[i]["lop"] == student_id or student_id is None:
            table += f"""
                <tr>
                    <td><a href="{url_for('get_student', student_id=i)}">{i}</a></td>
                    <td>{STUDENTS[i]["name"]}</td>
                    <td>{STUDENTS[i]["lop"]}</td>
                    <td>{dtb == -1 and "..." or f"{dtb:.2f}"}</td>
                    <td>{xeploai(dtb)}</td>
                </tr>"""

    table += "</table>"

    loc = "lop: <br>"
    for i in lop:
        loc += f'<a href={url_for("students", student_id=i)}>{i}</a> <br>'

    loc += "<br>"

    return loc + table

@app.route('/student/<student_id>')
def get_student(student_id):
    return STUDENTS[student_id]

@app.route('/search/<student_id>')
def tim_kiem_sinh_vien(student_id):
    return STUDENTS[student_id]



#
#
# HELLO TEMPLATE
@app.route("/hello_user/<name>")
def hello_user(name):
    return render_template(
                "/hello_template/hello_user.html",
                name=name,
                skills=["Python", "Flask"]
            )

@app.route("/base")
def base():
    return render_template("/hello_template/base.html")

@app.route("/about")
def about():
    return render_template("/hello_template/about.html")

@app.route("/contact")
def contact():
    return render_template("/hello_template/contact.html")

@app.context_processor
def inject_globals():
    return {
        "site_name": "MiniBlog",
        "current_year": date.today().year,
    }       



#
#
# CHUONG 5_2
USERS = {
    "admin": "admin123",
    "an": "an123456"
}


class RegisterForm(FlaskForm):
    username = StringField(
        "Tên đăng nhập",
        filters=[lambda x: x.strip() if x else x],
        validators=[
            DataRequired(message="Vui lòng nhập tên đăng nhập"),
            Length(min=4, max=20, message="Tên đăng nhập phải từ 4 đến 20 ký tự"),
            Regexp(r'^[a-z0-9_]+$',
                   message="Chỉ dùng chữ thường không dấu, số và dấu gạch dưới (_)"),
        ],
    )
    email = StringField(
        "Email",
        filters=[lambda x: x.strip() if x else x],
        validators=[
            DataRequired(message="Vui lòng nhập email"),
            Email(message="Email không đúng định dạng"),
        ],
    )
    password = PasswordField(
        "Mật khẩu",
        validators=[
            DataRequired(message="Vui lòng nhập mật khẩu"),
            Length(min=8, message="Mật khẩu tối thiểu 8 ký tự"),
        ],
    )
    confirm = PasswordField(
        "Nhập lại mật khẩu",
        validators=[
            DataRequired(message="Vui lòng nhập lại mật khẩu"),
            EqualTo("password", message="Mật khẩu nhập lại không khớp"),
        ],
    )
    agree = BooleanField(
        "Tôi đồng ý với điều khoản sử dụng",
        validators=[DataRequired(message="Bạn phải đồng ý với điều khoản để tiếp tục")],
    )
    submit = SubmitField("Đăng ký")

    def validate_username(self, field):
        if field.data in USERS:
            raise ValidationError("Tên đăng nhập này đã tồn tại")


@app.route("/login", methods=['POST', 'GET'])
def login():
    error = None
    if request.method == "POST":
        user = request.form.get("user")
        pw = request.form.get("pass")
        if user in USERS and USERS[user] == pw:
            session["user"] = user
            return redirect(url_for("index"))
        error = "Sai tên đăng nhập hoặc mật khẩu"
    return render_template("/chuong5_2/login.html", error=error)


@app.route("/register", methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        USERS[form.username.data] = form.password.data
        flash("Đăng ký thành công! Vui lòng đăng nhập.", "success")
        return redirect(url_for("login"))
    if request.method == "POST" and form.csrf_token.errors:
        flash("Phiên làm việc đã hết hạn, vui lòng thử lại.", "danger")
    return render_template("/chuong5_2/register.html", form=form)


@app.route("/index")
def index():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("/chuong5_2/index.html", user=session["user"])


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))



#
#
# BMI
@app.route('/bmi', methods=['POST', 'GET'])
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

    return render_template("/chuong5/bmi.html", values=values, error=error)



#
#
# MAY TINH
@app.route('/maytinh', methods=['POST', 'GET'])
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

    return render_template("/chuong5/cal.html", values=values, error=error)



#
#
# DIEM HOC PHAN
@app.route('/diemhocphan', methods=['POST', 'GET'])
def tinh_diem():
    values, error = kiem_tra()
    values["dtb"] = round(values["cc"] * 0.1  + values["gk"] * 0.3 + values["ck"] * 0.6, 2)
    if values["ck"] <= 1:
        values["xeploai"] = "F"
    else:
        values["xeploai"] = xep_loai(values["dtb"])

    return render_template("/chuong5/diemhocphan.html", values=values, error=error)

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

if __name__ == '__main__':
    app.run(debug=True)