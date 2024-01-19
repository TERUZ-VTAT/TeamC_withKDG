from datetime import datetime
from .database import db
from .auth import login_manager

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    # username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(255), index=True, unique=True)   # passwordをハッシュ化し、保存
    email = db.Column(db.String(120), index=True, unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # passwordをハッシュ化し、保存する
    @property
    def password(self):
        raise AttributeError("読み取り不可")
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


    # ログイン処理時に使用する関数
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    # 新規登録時に使用する関数
    def is_duplicate_email(self):
        return User.query.filter_by(email=self.email).first() is not None

# ログインしているユーザーのセッション等を管理
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
