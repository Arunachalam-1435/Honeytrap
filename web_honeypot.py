import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request, url_for

logging_format = logging.Formatter('%(asctime)s %(message)s')
logger = logging.getLogger("HTTPLogger")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler('http_audit.log',maxBytes=2000, backupCount=5)
handler.setFormatter(logging_format)
logger.addHandler(handler)

def web_honeypot(inp_username="admin", inp_password="password"):
    app = Flask(__name__, template_folder="templates", static_folder="templates", static_url_path='/')
    @app.route('/')
    def index():
        return render_template("login.html")
    
    @app.route('/user-login', methods=['POST']) 
    def login():
        username = request.form['username']
        password = request.form['password']
        ip_address = request.remote_addr
        logger.info(f"Client with IP Address: {ip_address} entered\n Username: {username} and Password {password}")
        if username == inp_username and password == inp_password:
            return "APRIL FOOOOOOOOOOOOOOOOLLLLLLLLLLLLLLL!!!!!!!!!!!!"
        else:
            return "Invalid Username or Password. Try Again"
    return app

def run_web_honeypot(port=8000, inp_username="admin", inp_password="password"):
    app = web_honeypot(inp_username, inp_password)
    app.run(debug=True, port=port, host="0.0.0.0")
    return app
if __name__ == "__main__":
    run_web_honeypot()