import os
import uuid
from datetime import datetime
from flask import render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models.database import db, Usuario, Post

FILE_TYPES = {"png", "jpg", "jpeg", "gif"}

def arquivos_permitidos(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in FILE_TYPES

def init_app(app):
    @app.before_request
    def check_auth():
        rotas_livres = {"home", "cadastro", "login"}
        if request.endpoint is None or request.endpoint in rotas_livres or request.endpoint == "static":
            return
        if "user_id" not in session:
            flash("Faça login para acessar essa página.", "warning")
            return redirect(url_for("login"))

    @app.route("/")
    def home():
        if "user_id" in session:
            return redirect(url_for("feed"))
        return render_template("home.html")

    @app.route("/cadastro", methods=["GET", "POST"])
    def cadastro():
        if request.method == "POST":
            nome = request.form.get("nome", "").strip()
            email = request.form.get("email", "").strip().lower()
            senha = request.form.get("senha", "")
            if not nome or not email or not senha:
                flash("Preencha todos os campos.", "danger")
                return redirect(url_for("cadastro"))
            if Usuario.query.filter_by(email=email).first():
                flash("Este e-mail já está cadastrado.", "danger")
                return redirect(url_for("cadastro"))
            senha_hash = generate_password_hash(senha, method="scrypt")
            novo_usuario = Usuario(nome=nome, email=email, senha=senha_hash)
            db.session.add(novo_usuario)
            db.session.commit()
            flash("Cadastro realizado! Faça login para continuar.", "success")
            return redirect(url_for("login"))
        return render_template("cadastro.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = request.form.get("email", "").strip().lower()
            senha = request.form.get("senha", "")
            usuario = Usuario.query.filter_by(email=email).first()
            if usuario and check_password_hash(usuario.senha, senha):
                session.clear()
                session["user_id"] = usuario.id
                session["usuario_nome"] = usuario.nome
                session["usuario_email"] = usuario.email
                session.permanent = True
                flash(f"Bem-vindo(a), {usuario.nome}!", "success")
                return redirect(url_for("feed"))
            flash("E-mail ou senha incorretos.", "danger")
        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.clear()
        flash("Você saiu da sua conta.", "info")
        return redirect(url_for("login"))

    @app.route("/feed")
    def feed():
        posts = Post.query.order_by(Post.data_post.desc()).all()
        return render_template("feed.html", posts=posts)

    @app.route("/upload", methods=["POST"])
    def upload():
        arquivo = request.files.get("file")
        legenda = request.form.get("legenda", "").strip()
        if not arquivo or arquivo.filename == "":
            flash("Selecione uma imagem.", "danger")
            return redirect(url_for("feed"))
        if not arquivos_permitidos(arquivo.filename):
            flash("Formato inválido. Envie PNG, JPG, JPEG ou GIF.", "danger")
            return redirect(url_for("feed"))

        extensao = secure_filename(arquivo.filename).rsplit(".", 1)[1].lower()
        nome_arquivo = f"{uuid.uuid4().hex}.{extensao}"
        caminho = os.path.join(current_app.config["UPLOAD_FOLDER"], nome_arquivo)
        arquivo.save(caminho)

        post = Post(
            imagem=nome_arquivo,
            legenda=legenda,
            usuario_id=session["user_id"]
        )
        db.session.add(post)
        db.session.commit()
        flash("Publicação enviada com sucesso!", "success")
        return redirect(url_for("feed"))

    @app.route("/chat")
    def chat_page():
        return render_template("chat.html")
