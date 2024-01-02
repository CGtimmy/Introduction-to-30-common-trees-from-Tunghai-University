#!/Users/hoyi/opt/anaconda3/bin/python
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pymssql://sa:########@localhost/register'
db = SQLAlchemy(app)

#資料庫registers
class registers(db.Model):
    account_number = db.Column(db.String(20), primary_key=True, nullable=False)
    password_number = db.Column(db.String(20), nullable=False)

#資料庫like_animail
class like_animail(db.Model):
    __tablename__ = 'like_animail'
    account_number = db.Column(db.String(20), primary_key=True, nullable=False)
    animal = db.Column(db.String(20), nullable=False)

#資料庫thirty_tree
class thirty_tree(db.Model):
    Botanicname = db.Column(db.String(20), primary_key=True, nullable=False)
    Place = db.Column(db.String(20))

    @classmethod
    def execute_leaf_query(cls, search):
        connection = db.engine.connect()
        try:
            query = text(f"EXECUTE leafsearch @search = :search")
            query = query.bindparams(search=search)
            result = connection.execute(query)
            return result.fetchall()
        finally:
            connection.close()

#登入頁面
@app.route("/login1", methods=['GET', 'POST'])
def login1():
    return render_template('login.html')

#樹葉
@app.route("/tree",methods=['GET'])
def tree():
    return render_template('樹葉.html')

#判斷登入
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        Compare = registers.query.filter_by(account_number=username, password_number=password).first()
        if Compare:
            return render_template('樹葉.html')
        else:
            return render_template('login_false.html', message="登入失敗，帳號或密碼錯誤")
    else:
        return render_template('login_false.html')

#註冊帳號
@app.route("/register", methods=['GET'])
def register():
    return render_template('register.html')

#判斷註冊
@app.route("/register_success", methods=['POST'])
def register_success():
    username = request.form['username']
    password = request.form['password']
    Like_animal = request.form['Like_animal']

    existing_user = registers.query.filter_by(account_number=username).first()
    if existing_user:
        return render_template('register_fail.html', message="帳號已經存在，換一個")

    if not username or not password or not Like_animal:
        return render_template('register_fail.html', message="請填寫所有的欄位")

    new_register = registers(account_number=username, password_number=password)
    new_animal = like_animail(account_number=username, animal=Like_animal)
    db.session.add(new_register)
    db.session.add(new_animal)
    db.session.commit()
    return render_template('register_success.html', message="註冊成功")

#找回密碼
@app.route("/Findpassword",methods=['GET'])
def Findpassword():
    return render_template('Findpassword.html')

#判斷找回密碼
@app.route("/Findpassword_success", methods=['POST'])
def find_password_success():
    username = request.form['username']
    password = request.form['password']
    Like_animal = request.form['Like_animal']

    Compare = like_animail.query.filter_by(account_number=username, animal=Like_animal).first()

    if Compare:
        Newuser = registers.query.filter_by(account_number=username).first()
        Newuser.password_number = password
        db.session.commit()
        return render_template('findpassword_success.html', message="密碼更新成功")

    else:
        return render_template('findpassword_fail.html', message="帳號或動物驗證錯誤")

#刪除帳號
@app.route("/Deleteaccount",methods=['GET'])
def Deleteaccount():
    return render_template('Deleteaccount.html')

#判斷刪除帳號
@app.route("/Deleteaccount_successful", methods=['GET', 'POST'])
def Deleteaccount_successful():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        Like_animal = request.form['Like_animal']

        Compare = registers.query.filter_by(account_number=username, password_number=password).first()
        Compare1 = like_animail.query.filter_by(account_number=username,animal=Like_animal).first()

        if Compare:
            if Compare1:
                db.session.delete(Compare)
                db.session.delete(Compare1)
                db.session.commit()
                return render_template('deleteaccount_success.html', message="成功刪除帳號")
            else:
                return render_template('deleteaccount_false.html',message="帳號或密碼或動物驗證錯誤")
        else:
            return render_template('deleteaccount_false.html', message="帳號或密碼或動物驗證錯誤")
    else:
        return render_template('deleteaccount_false.html')

def get_place_from_database(tree_name):
    place = thirty_tree.query.filter_by(Botanicname=tree_name).first()
    return place.Place if place else None

@app.route("/seven_flower", methods=['GET'])
def seven_flower():
    place = get_place_from_database("七里香")
    return render_template('七里香.html', place=place)

@app.route("/big_flower_purple",methods=['GET'])
def big_flower_purple():
    place = get_place_from_database("大花紫薇")
    return render_template('大花紫薇.html', place=place)

@app.route("/big_leaf",methods=['GET'])
def big_leaf():
    place = get_place_from_database("大葉油加利")
    return render_template('大葉油加利.html', place=place)

@app.route("/small_leaf",methods=['GET'])
def small_leaf():
    place = get_place_from_database("小葉桃花心木")
    return render_template('小葉桃花心木.html', place=place)

@app.route("/moutain_flower",methods=['GET'])
def moutain_flower():
    place = get_place_from_database("山櫻花")
    return render_template('山櫻花.html', place=place)

@app.route("/think_tree",methods=['GET'])
def think_tree():
    place = get_place_from_database("相思樹")
    return render_template('相思樹.html', place=place)

@app.route("/son_tree",methods=['GET'])
def son_tree():
    place = get_place_from_database("桑樹")
    return render_template('桑樹.html', place=place)

@app.route("/block_tree",methods=['GET'])
def block_tree():
    place = get_place_from_database("黑板樹")
    return render_template('黑板樹.html', place=place)

@app.route("/bird_tree",methods=['GET'])
def bird_tree():
    place = get_place_from_database("小葉南洋杉")
    return render_template('小葉南洋杉.html', place=place)

@app.route("/loooo",methods=['GET'])
def loooo():
    place = get_place_from_database("垂柳")
    return render_template('垂柳.html', place=place)

@app.route("/dragon_tree",methods=['GET'])
def dragon_tree():
    place = get_place_from_database("龍柏")
    return render_template('龍柏.html', place=place)

@app.route("/yellow",methods=['GET'])
def yellow():
    place = get_place_from_database("木麻黃")
    return render_template('木麻黃.html', place=place)

@app.route("/bloom",methods=['GET'])
def bloom():
    place = get_place_from_database("血桐")
    return render_template('血桐.html', place=place)

@app.route("/wide",methods=['GET'])
def wide():
    place = get_place_from_database("濕地松")
    return render_template('濕地松.html', place=place)

@app.route("/sheap",methods=['GET'])
def sheap():
    place = get_place_from_database("羊蹄甲")
    return render_template('羊蹄甲.html', place=place)

@app.route("/south",methods=['GET'])
def south():
    return render_template('南天竹.html')
    place = get_place_from_database("南天竹")
    return render_template('南天竹.html', place=place)

@app.route("/big_bird",methods=['GET'])
def big_bird():
    place = get_place_from_database("鳳凰木")
    return render_template('鳳凰木.html', place=place)

@app.route("/huu",methods=['GET'])
def huu():
    place = get_place_from_database("銀樺")
    return render_template('銀樺.html', place=place)

@app.route("/money",methods=['GET'])
def money():
    place = get_place_from_database("串錢柳")
    return render_template('串錢柳.html', place=place)

@app.route("/duck",methods=['GET'])
def duck():
    place = get_place_from_database("鵝掌蘗")
    return render_template('鵝掌蘗.html', place=place)

@app.route("/white",methods=['GET'])
def white():
    place = get_place_from_database("白千層")
    return render_template('白千層.html', place=place)

@app.route("/go",methods=['GET'])
def go():
    place = get_place_from_database("構樹")
    return render_template('構樹.html', place=place)

@app.route("/smell",methods=['GET'])
def smell():
    place = get_place_from_database("楓香")
    return render_template('楓香.html', place=place)

@app.route("/winter",methods=['GET'])
def winter():
    place = get_place_from_database("茄苳")
    return render_template('茄苳.html', place=place)

@app.route("/strangle",methods=['GET'])
def strangle():
    place = get_place_from_database("正榕")
    return render_template('正榕.html', place=place)

@app.route("/dirty",methods=['GET'])
def dirty():
    place = get_place_from_database("樟樹")
    return render_template('樟樹.html', place=place)

@app.route("/taiwan",methods=['GET'])
def taiwan():
    place = get_place_from_database("臺灣欒樹")
    return render_template('臺灣欒樹.html', place=place)

@app.route("/blue",methods=['GET'])
def blue():
    place = get_place_from_database("洋玉蘭")
    return render_template('洋玉蘭.html', place=place)

@app.route("/woo",methods=['GET'])
def woo():
    place = get_place_from_database("烏臼")
    return render_template('烏臼.html', place=place)

@app.route("/gold_flower",methods=['GET'])
def gold_flower():
    place = get_place_from_database("蕾絲金露花")
    return render_template('蕾絲金露花.html', place=place)

#樹葉查詢判斷
@app.route("/Find", methods=['GET', 'POST'])
def Find():
    if request.method == 'POST':
        search = request.form['search']
        find = thirty_tree.execute_leaf_query(search)
        if find:
            place = get_place_from_database(find[0][0])
            return render_template(f"{find[0][0]}.html",place=place)
        else:
            return render_template('樹葉.html')
    else:
        return render_template('樹葉.html')
