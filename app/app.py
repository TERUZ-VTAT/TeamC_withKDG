from flask import Flask, render_template, redirect, request, url_for

# ログインで必要なimport
from flask_login import login_user, logout_user, login_required, current_user
# ログイン処理な必要なオブジェクトの定義
from .models.auth import init_auth

# 投稿編集に必要なimport
# from .forms import EditPostForm

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
    @login_required
    # @login_requiredのデコレータをつけることで、ログイン状態のみ表示
    def add_post():
        if request.method == "POST":
            postInfo = Post(
                title=request.form["title"],
                category=request.form["category"],
                content=request.form["content"],
                money=request.form["money"],
                company=request.form["company"],
                user_id=current_user.id,
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
        # return render_template("postList.html")
        return render_template("postList.html", posts=posts)

    @app.route("/profile")
    @login_required
    def profile():
        return render_template("profile.html")
    
    @app.route("/user_posts/<int:user_id>")
    @login_required
    def userPosts(user_id):
        user_posts = Post.query.filter_by(user_id=user_id).all()
        return render_template("user_posts.html", posts=user_posts)
    
    # 投稿編集機能
    # @app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
    # @login_required 
    # def edit_post(post_id):
    #     post = Post.query.get_or_404(post_id)
    #     form = EditPostForm(obj=post)

    #     if form.validate_on_submit():
    #         post.content = form.content.data
    #         db.session.commit()
    #         return redirect(url_for('userPosts', user_id=current_user.id))

    #     return render_template('edit_post.html', form=form, post=post)
    
    # 投稿削除の処理
    @app.route('/delete_post/<int:post_id>', methods=['POST'])
    def delete_post(post_id):
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        # ユーザーの投稿一覧画面にリダイレクト
        return redirect(url_for('userPosts', user_id=current_user.id))

    return app


app = create_app()

if __name__ == "__main__":
    app.run()
