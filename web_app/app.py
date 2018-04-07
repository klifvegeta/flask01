from flask import Flask, render_template
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import login_required
from flask_security import SQLAlchemyUserDatastore, Security

from models import db, Page, Menu, User, Role
from views import PageModelView, MenuModelView, SecuredAdminIndexView


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')

    db.init_app(app)

    admin = Admin(app, name='Flask01', template_mode='bootstrap3', index_view=SecuredAdminIndexView())
    admin.add_view(PageModelView(Page, db.session))
    admin.add_view(MenuModelView(Menu, db.session))

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    @app.route('/')
    @app.route('/<url>')
    def index(url=None):
        print('here', url)
        if url is not None:
            # contoh /about
            page = Page.query.filter_by(url=url).first()
        else:
            # contoh /
            page = Page.query.filter_by(is_homepage=True).first()

        if page is None:
            # TODO cute 404
            return 'Page not found for {} or homepage not set'.format(url)

        contents = 'empty'
        if page is not None:
            contents = page.contents

        menu = Menu.query.order_by('order')


        return render_template('index.html', TITLE='Flask-01', CONTENT=contents, menu=menu)

    @app.route('/rahasia')
    @login_required
    def rahasia():
        return '<h1>Luke dies!<h1>'



    @app.route('/testdb')
    def testdb():
        import psycopg2

        con = psycopg2.connect('dbname=flask01 user=devuser password=devpassword host=postgres')
        cur = con.cursor()

        cur.execute('select * from page;')

        id, title = cur.fetchone()
        con.close()
        return 'Output table page: {} - {}'.format(id, title)

    return app