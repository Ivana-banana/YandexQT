import flask
from flask import Flask, render_template, request
from data import db_session, jobs_api, one_job
from data.jobs import Jobs
from data.users import User
from flask_login import LoginManager
from flask import redirect
from data.login_form import LoginForm
from flask_restful import Api
from data import user_resource

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)


login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first
        if user and user.check_password(form.email.data):
            login_user(user, form.remember_me.data)
            return redirect("/succes")
        else:
            return render_template("login.html", message="Неверно", form=form)
    return render_template("login.html", title="Авторизация", form=form)


def login_user(user, remember=False):
    pass


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/index')
@app.route('/')
def index():
    nazvanie = "Главная"
    return render_template("base.html", title=nazvanie)


@app.route('/training/<prof>')
def train(prof):
    return render_template("training.html", prof=prof)


@app.route("/list_prof/<list>")
def prof(list):
    lst = ["слесарь"] * 10 + ["сантехник"] * 3 + ["плотник"] * 2
    return render_template("prof.html", list=lst, znak=list)


@app.route('/form1', methods=['POST', 'GET'])
def form1():
    if request.method == "GET":
        return render_template("form1.html")
    else:
        profil = {}
        profil["email"] = request.form.get('email')
        profil["class"] = request.form.get('class')
        return render_template("answer.html", **profil)


@app.route("/answer")
def answer():
    pass


def add_user():
    sess = db_session.create_session()
    user = User()
    user.surname = "Ridley"
    user.name = "Schott"
    user.age = 21
    user.position = "capitan"
    user.email = "sr@mars.com"
    user.speciality = "resercher"
    user.address = "module 1"
    user.set_password("123")
    sess.add(user)
    sess.commit()
    sess.close()


def add_jobs():
    sess = db_session.create_session()
    job = Jobs()
    job.team_leader = 1
    job.job = 'deployment of residential modules 1 and 2'
    job.work_size = 15
    job.collaborators = '2, 3'
    job.is_finished = False
    sess.add(job)
    sess.commit()
    sess.close()


def zapros():
    sess = db_session.create_session()
    user = sess.query(User).filter(User.age == 21).all()
    for el in user:
        print(el.name)
    sess.close()


def main1():
    # db_name = input()
    #   global_init(db_name)

    sess = db_session.create_session()

    res = sess.query(User.id).filter((User.address == "module 1"), (User.speciality.notlike("%engineer%")),
                                     (User.position.notlike("%engineer%"))).all()

    for el in res:
        print(el.id)


def main():
    db_session.global_init("db/blogs.db")
    # zapros()
    # main1()
    # add_user()
    # add_jobs()
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(one_job.blueprint)
    api.add_resource(user_resource.UserResource, "/api/v2/users/<int:user_id>")
    api.add_resource(user_resource.UserResourceList, "/api/v2/users/")

    app.run("127.0.0.1", port=80)


if __name__ == "__main__":
    main()

