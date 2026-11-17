MINI REDE SOCIAL - CONECTA (MYSQL / XAMPP)

CONFIGURACAO DO XAMPP

1. Abra o XAMPP Control Panel.
2. Inicie Apache e MySQL. A imagem da atividade mostra os dois servicos ativos.
3. Clique em Admin na linha do MySQL ou acesse http://localhost/phpmyadmin.
4. Abra a aba SQL e execute:

   CREATE DATABASE rede_social
   CHARACTER SET utf8mb4
   COLLATE utf8mb4_unicode_ci;

   (Se preferir, crie um banco com o nome rede_social pela opcao Novo.)

CONFIGURACAO E EXECUCAO DO FLASK

1. Abra o terminal dentro da pasta mini_rede_social.
2. (Opcional, recomendado) Crie e ative um ambiente virtual:
   python -m venv .venv
   .venv\Scripts\activate        (Windows)
3. Instale as dependencias:
   pip install -r requirements.txt
4. Confira a conexao em app.py:
   mysql+pymysql://root:@127.0.0.1:3306/rede_social?charset=utf8mb4
   Essa configuracao considera o XAMPP local, usuario root, senha vazia e porta 3306.
   Se voce configurou uma senha para o root, coloque-a depois de root: e antes de @.
   Exemplo: mysql+pymysql://root:SUA_SENHA@127.0.0.1:3306/rede_social?charset=utf8mb4
5. Execute:
   python app.py
6. Acesse no navegador:
   http://127.0.0.1:5000

IMPORTANTE
- O Apache e o MySQL precisam estar iniciados no XAMPP enquanto a aplicacao estiver usando o banco.
- O banco rede_social precisa existir antes de executar o Flask.
- As tabelas usuario e post serao criadas automaticamente pelo db.create_all() na primeira execucao.
- O Flask roda na porta 5000. O Apache do XAMPP usa as portas 80/443; nao ha conflito entre eles.
- As imagens enviadas ficam em static/uploads.

FUNCIONALIDADES
- Cadastro com nome, e-mail e senha protegida por generate_password_hash (scrypt).
- Login com check_password_hash, session e logout.
- Middleware @app.before_request protegendo as paginas internas.
- Upload PNG/JPG/JPEG/GIF com UUID e limite de 16 MB.
- Feed ordenado da publicacao mais recente para a mais antiga.
- Relacionamento Usuario (1) para Post (N).
- Chat coletivo em tempo real com Flask-SocketIO, eventos join e msg.

Antes de entregar, troque SECRET_KEY em app.py por uma chave propria e teste cadastro,
login, upload, feed e chat em duas janelas/navegadores.
