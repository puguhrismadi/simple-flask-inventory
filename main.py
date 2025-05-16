from flask import Flask
from config import db
from controllers.barang_controller import barang_bp
from controllers.supplier_controller import supplier_bp
from controllers.lokasi_controller import lokasi_bp
from controllers.auth_controller import auth_bp
from controllers.arsip_controller import arsip_bp

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/uploads/arsip'

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(barang_bp)
app.register_blueprint(supplier_bp)
app.register_blueprint(lokasi_bp)
app.register_blueprint(arsip_bp)

if __name__ == '__main__':
    app.run(debug=True)
