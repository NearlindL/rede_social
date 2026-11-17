from flask import session
from flask_socketio import emit

def init_app(socketio):
    @socketio.on("join")
    def on_join():
        nome = session.get("usuario_nome", "Usuário")
        emit("showmsg", {"usuario": "Sistema", "mensagem": f"{nome} entrou no chat."}, broadcast=True)

    @socketio.on("msg")
    def on_message(data):
        if "user_id" not in session:
            return
        nome = session.get("usuario_nome", "Usuário")
        mensagem = str(data.get("mensagem", "")).strip()[:500]
        if mensagem:
            emit("showmsg", {"usuario": nome, "mensagem": mensagem}, broadcast=True)
