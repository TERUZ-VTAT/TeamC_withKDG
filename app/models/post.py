from datetime import datetime
from .database import db

# Postモデルの定義
class Post(db.Model):
    __tablename__ = 'post'     # DBのテーブル作成時にpostで作成する
    id = db.Column(db.Integer, primary_key=True)                                   # カラム名idでInteger型
    title = db.Column(db.String(64), index=True, unique=True)                      # カラム名titleでString型,64まで
    content = db.Column(db.String(120), index=True, unique=True)                   # カラム名contentでString型,120まで
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)   # カラム名created_atでDateTime型

    def to_dict(self):
            return {
                'id': self.id,
                'title': self.title,
                'content': self.content,
                'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            }
