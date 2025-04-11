import os
import click

from flask import Flask, render_template
from flask_login import current_user
from flask_wtf.csrf import CSRFError

from app.blueprints import main_bp, auth_bp, user_bp, oauth_bp
from app.models import Message, Role, User
from app.models.oauth_provider_config import OAuthProviderConfig
from app.extensions import db, login_manager, moment, whooshee, oauth, csrf, migrate
from app.config import config  # 导入存储配置的字典


def create_app(config_name=None):
    """
    创建 Flask web 应用程序实例。
    
    Args:
        config_name (str, optional): 应用程序配置名称。默认为 None，将从环境变量 'FLASK_ENV' 中获取，
            如果未设置则使用 'development' 作为默认值。
    
    Returns:
        Flask: 返回一个 Flask web 应用程序实例。
    
    Raises:
        ValueError: 如果给定的 `config_name` 不在配置字典 `config` 的键中，则引发 ValueError 异常。
    
    """
    if config_name is None:
        # 从环境变量中获取FLASK_ENV，并设置默认值，同时确保它是有效的配置名称
        config_name = os.getenv('FLASK_ENV', 'development')
        if config_name not in config:
            raise ValueError(f"Invalid config name: {config_name}. Must be one of {list(config.keys())}")

    app = Flask('app')

    # 导入配置，根据配置环境实例化对象
    app.config.from_object(config[config_name])

    # 注册扩展
    register_extensions(app)
    register_commands(app)
    register_blueprints(app)
    register_errors(app)
    register_shell_context(app)


    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    moment.init_app(app)
    whooshee.init_app(app)
    oauth.init_app(app)
    csrf.init_app(app)

def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(oauth_bp, url_prefix='/auth')

def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, User=User, Role=Role)

def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('error.html', description=e.description, code=e.code), 400

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('error.html', description=e.description, code=e.code), 403

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error.html', description=e.description, code=e.code), 404

    @app.errorhandler(413)
    def request_entity_too_large(e):
        return render_template('error.html', description=e.description, code=e.code), 413

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('error.html', description='Internal Server Error', code='500'), 500

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('error.html', description=e.description, code=e.code), 400



def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    def init():
        """Initialize Albumy."""
        click.echo('Initializing the database...')
        db.create_all()

        click.echo('Initializing the roles and permissions...')
        Role.init_role()

        click.echo('Done.')

    @app.cli.command()
    @click.option('--user', default=10, help='Quantity of users, default is 10.')
    @click.option('--message', default=50, help='Quantity of messages, default is 50.')
    def forge(user, message):
        """Generate fake data."""

        from app.utils import fake_admin, fake_user, fake_message

        db.drop_all()
        db.create_all()

        click.echo('Initializing the roles and permissions...')
        Role.init_role()
        click.echo('Generating the administrator...')
        fake_admin()
        click.echo('Generating %d users...' % user)
        fake_user(user)
        click.echo('Generating %d messages...' % message)
        fake_message(message)
        click.echo('Done.')
