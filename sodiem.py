from flask import Flask, url_for

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

sodiem = Flask(__name__)

@sodiem.route('/')
def index():
    sinhvien = len(STUDENTS)
    solop = set()
    for i in STUDENTS:
        solop.add(STUDENTS[i]["lop"])

    return f"""
            Tong so sinh vien la: {sinhvien}, So lop la: {len(solop)} <br>
            <a href="{url_for('students')}">Danh sach sinh vien</a>
        """

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

@sodiem.route('/students')
@sodiem.route('/students/<student_id>')
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

@sodiem.route('/student/<student_id>')
def get_student(student_id):
    return STUDENTS[student_id]

@sodiem.route('/search/<student_id>')
def tim_kiem_sinh_vien(student_id):
    return STUDENTS[student_id]

if __name__ == '__main__':
    sodiem.run(debug=True)