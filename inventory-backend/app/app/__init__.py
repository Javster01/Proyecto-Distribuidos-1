from flask import Flask
from flask_cors import CORS
from flask_mysqldb import MySQL

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    CORS(app)
    
    # Inicializar MySQL
    mysql = MySQL(app)
    app.mysql = mysql
    
    with app.app_context():
        from .routes import bp as main_bp
        app.register_blueprint(main_bp)
        
        return app
