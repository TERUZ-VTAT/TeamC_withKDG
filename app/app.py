from flask import Flask, render_template, redirect, request, url_for

# ログインで必要なimport
from flask_login import login_user, logout_user, login_required
# ログイン処理な必要なオブジェクトの定義
from .models.auth import init_auth

from .models.database import init_db, db
from .models.post import Post
from .models.user import User

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")
    # サーバー側で保持しておく必要があるシークレットキー。セッション等に必要。ランダムな値を使用する。
    app.secret_key = 'secret_key_here' 

    # ログイン処理のオプジェクトを設定
    init_auth(app)
    init_db(app)

    # 新規登録処理
    @app.route("/signup", methods=["GET", "POST"])
    def signup():
        if request.method == "POST":
            user = User(
                username=request.form["username"],
                email=request.form["email"],
                password=request.form["password"],
            )

            if user.is_duplicate_email():
                return redirect(url_for("signup"))
            db.session.add(user)
            db.session.commit()

            login_user(user)
            return render_template("login.html")
        return render_template("signup.html")

    # ログイン用の処理
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            user = User.query.filter_by(email=request.form["email"]).first()
            if user is not None and user.verify_password(request.form["password"]):
                login_user(user)
                return redirect(url_for("postList"))
        return render_template("login.html")

    # ログアウト処理
    @app.route("/logout")
    def logout():
        logout_user()
        return redirect(url_for("login"))

    @app.route("/post", methods=["GET", "POST"])
    @login_required  # @login_requiredのデコレータをつけることで、ログイン状態のみ表示
    def add_post():
        if request.method == "POST":
            postInfo = Post(
                title=request.form["title"],
                content=request.form["content"],
                money=request.form["money"],
                company=request.form["company"]
            )
            db.session.add(postInfo)
            db.session.commit()
            return redirect("/postlist")
        else:
            return render_template("post.html")
        
    @app.route("/post_detail/<int:id>")
    @login_required
    def postDetail(id):
        details = Post.query.get(id)
        return render_template("post_detail.html", details=details)


    @app.route("/postlist")
    # @login_required  
    # @login_requiredのデコレータをつけることで、ログイン状態のみ表示
    def postList():
        posts = Post.query.all()
        return render_template("postList.html", posts=posts)
    
    @app.route("/")
    @login_required
    def account():
        return render_template("")

    return app

app = create_app()

if __name__ == "__main__":
    app.run()
