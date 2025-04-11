import os
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


# 基础配置，使用继承的方式
class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')
    
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    
    # 是否追踪数据库修改，一般不开启, 会影响性能
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data.db')


    # Google Oauth2.0
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', "<your-id-ending-with>.apps.googleusercontent.com")
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET', "<your-secret>")
    GOOGLE_REQUEST_TOKEN_URL = os.getenv('GOOGLE_REQUEST_TOKEN_URL', "https://accounts.google.com/o/oauth2/auth")
    
    # Github OAuth2.0
    GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID', 'Ov23ctoHnbS9GqRiihyV')
    GITHUB_CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET', '2fe428f0157b077522fbc03a5f933e24e34e27d4')
    GITHUB_REQUEST_TOKEN_URL = os.getenv('GITHUB_REQUEST_TOKEN_URL', "https://github.com/login/oauth/authorize")

    # Twitter OAuth1.0
    TWITTER_CLIENT_ID = os.getenv('TWITTER_CLIENT_ID', 'TWITTER_CLIENT_ID')
    TWITTER_CLIENT_SECRET = os.getenv('TWITTER_CLIENT_SECRET', 'TWITTER_CLIENT_SECRET')
    TWITTER_REQUEST_TOKEN_URL = os.getenv('TWITTER_REQUEST_TOKEN_URL', "https://api.twitter.com/oauth/request_token")

    OAUTH_CREDENTIALS={
        'google': {
            'id': GOOGLE_CLIENT_ID,
            'secret': GOOGLE_CLIENT_SECRET
        },
        'github': {
            'id': GITHUB_CLIENT_ID,
            'secret': GITHUB_CLIENT_SECRET
        },
        'twitter': {
            'id': TWITTER_CLIENT_ID,
            'secret': TWITTER_CLIENT_SECRET
        }
    }

class DevelopmentConfig(BaseConfig):
    """
    开发环境
    """
    DEBUG = True


class ProductionConfig(BaseConfig):
    """
    生产环境
    """
    DEBUG = False


class TestingConfig(BaseConfig):
    """
    测试环境
    """
    TESTING = True
    WTF_CSRF_ENABLED = False
    # 在测试环境中，使用内存数据库
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # in-memory database
    
# 映射环境对象
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
