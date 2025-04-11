from flask_login import LoginManager
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_whooshee import Whooshee
from flask_oauthlib.client import OAuth
from flask_migrate import Migrate


db = SQLAlchemy()
moment = Moment()
csrf = CSRFProtect()
whooshee = Whooshee()
migrate = Migrate()

login_manager = LoginManager()
oauth = OAuth()


@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    user = User.query.get(int(user_id))
    return user

login_manager.login_view = 'auth.login'
# login_manager.login_message = 'Your custom message'
login_manager.login_message_category = 'warning'

login_manager.refresh_view = 'auth.re_authenticate'
# login_manager.needs_refresh_message = 'Your custom message'
login_manager.needs_refresh_message_category = 'warning'
