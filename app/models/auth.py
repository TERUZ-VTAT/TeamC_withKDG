from flask_login import LoginManager

# ログイン管理のオブジェクトを定義
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message = ""

def init_auth(app):
    login_manager.init_app(app)
