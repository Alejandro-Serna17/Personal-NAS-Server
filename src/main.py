from flask import Flask, request, redirect, url_for, send_from_directory, render_template, session
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import secrets
import os

hashed_password = "scrypt:32768:8:1$69COQCbA3a6IyQQW$62db8c66dbd04303fd84a950f7a3a1f8eaa95f8dac53def5ec07536097faa34a6b5ee3518229a1a9171bbb0ec0e8f7fcff69c0b9efdd3329ee8aad0ff8c8a612"

UPLOAD_FOLDER = os.path.expanduser("~/nas_share")
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip', 'mp4', 'mp3', 'csv'])

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

MAIN_PAGE = 'mainScreen.html'
LOGIN_PAGE = 'login.html'
INVALID_LOGIN_PAGE = 'invalid.html'

# Login form
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and check_password_hash(hashed_password, request.form['password']):
            session['logged_in'] = True
            return redirect(url_for('index', error='exists'))
        return render_template(INVALID_LOGIN_PAGE)
    
    return render_template(LOGIN_PAGE)

# Logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

# Require a login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Check for allowed file ext.
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Main index route (upload and list)
@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        file = request.files.get('file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.exists(filepath):
              return redirect(url_for('index'))
            file.save(filepath)
            return redirect(url_for('index'))

    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template(MAIN_PAGE, files=files)

# Delete Files
@app.route('/delete/<filename>', methods=['POST'])
@login_required
def delete_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    return redirect(url_for('index'))

# Download Files
@app.route('/files/<filename>')
@login_required
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

# Run the app
if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(host='0.0.0.0', port=8000, debug=False)
