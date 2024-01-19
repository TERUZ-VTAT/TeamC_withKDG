from datetime import datetime
from .database import db

# Postモデルの定義
class Post(db.Model):
    __tablename__ = 'posts'     # DBのテーブル作成時にpostで作成する
    id = db.Column(db.Integer, primary_key=True)                                   # カラム名idでInteger型
    title = db.Column(db.String(64), index=True)                      # カラム名titleでString型,64まで
    category = db.Column(db.String(64), index=True)
    money = db.Column(db.String(64))
    company = db.Column(db.String(64))
    content = db.Column(db.String(120), index=True, unique=True)                   # カラム名contentでString型,120まで
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)   # カラム名created_atでDateTime型
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def to_dict(self):
            return {
                'id': self.id,
                'title': self.title,
                'category': self.category,
                'content': self.content,
                'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                'user_id': self.user_id,
            }
