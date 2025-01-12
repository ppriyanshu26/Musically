from flask import Flask, render_template, request, jsonify
import mysql.connector as mycon
import os, shutil, hashlib

app = Flask(__name__, static_url_path='/static')

HOST,USER,PASSWORD,DATABASE = "localhost","root","admin","musically"

PATH = "P:"

def hash_string(input_string):
    hasher = hashlib.sha256()
    hasher.update(input_string.encode('utf-8'))
    hashed_string = hasher.hexdigest()[:128]    
    return hashed_string


def folder_empty():
    folder_path = PATH+'/Project/Musically/songs/User'
    mp3_files_exist = False
    for filename in os.listdir(folder_path):
        if filename.endswith('.mp3'):
            mp3_files_exist = True
            break

    if mp3_files_exist:
        for filename in os.listdir(folder_path):
            if filename.endswith('.mp3'):
                file_path = os.path.join(folder_path, filename)
                os.remove(file_path)


def connect_mysql():
    global users
    connection = mycon.connect(host=HOST,user=USER,password=PASSWORD,database=DATABASE)
    cursor = connection.cursor()
    sql_query = "SELECT username, password FROM users"
    cursor.execute(sql_query)
    rows = cursor.fetchall()
    users = {}

    for row in rows:
        username = row[0].lower()
        password = row[1]
        users[username] = password
    cursor.close()
    connection.close()


@app.route('/')
def index():
    folder_empty()
    return render_template('login.html')

@app.route('/login')
def login():
    folder_empty()
    return render_template('login.html')

@app.route('/signup')
def signup():
    folder_empty()
    return render_template('signup.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/login', methods=['POST'])
def login_site():
    folder_empty()
    return render_template('login.html')

@app.route('/signup', methods=['POST'])
def signup_site():
    folder_empty()
    return render_template('signup.html')

@app.route('/signup_account', methods=['POST'])
def signup_credentials():
    connect_mysql()
    
    username = request.json.get('username')
    password = request.json.get('password')
    username = username.lower()
    hashed_pass = hash_string(password)

    if username == '':
        return jsonify({'success': False, 'message': 'Username cannot be empty'})
    elif not username.isalpha():
        return jsonify({'success': False, 'message': 'Only alphabets are allowed in username'})
    elif username in users:
        return jsonify({'success': False, 'message': 'Username already taken'})
    elif password == '':
        return jsonify({'success': False, 'message': 'Password cannot be empty'})
    else:
        connection = mycon.connect(host=HOST,user=USER,password=PASSWORD,database=DATABASE)
        cursor = connection.cursor()

        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_pass))
        connection.commit()
        cursor.close()
        connection.close()

        path = "W:/Project/Musically/users"
        folder_name = username
        folder_path = os.path.join(path, folder_name)
        os.mkdir(folder_path)
        return jsonify({'success': True, 'message': 'Welcome! Please log in to continue'})
    

@app.route('/home', methods=['POST'])
def login_credentials():
    global username
    connect_mysql()

    username = request.json['username']
    password = request.json['password']
    username = username.lower()
    hashed_pass = hash_string(password)

    if username in users and users[username] == hashed_pass:
        source_folder = PATH+'/Project/Musically/users/'+username
        destination_folder = PATH+'/Project/Musically/songs/User'
        mp3_files_exist = False
        for filename in os.listdir(source_folder):
            if filename.endswith('.mp3'):
                mp3_files_exist = True
                break
        if mp3_files_exist:
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)
            for filename in os.listdir(source_folder):
                if filename.endswith('.mp3'):
                    source_path = os.path.join(source_folder, filename)
                    destination_path = os.path.join(destination_folder, filename)
                    shutil.copy2(source_path, destination_path)
        return jsonify({'success': True, 'message': 'Login successful'})
    elif username == '':
        return jsonify({'success': False, 'message': 'Username cannot be empty'})
    elif not username.isalpha():
        return jsonify({'success': False, 'message': 'Only alphabets are allowed in username'})
    elif username not in users:
        return jsonify({'success': False, 'message': 'Username does not exist'})
    elif password == '':
        return jsonify({'success': False, 'message': 'Password cannot be empty'})
    else:
        return jsonify({'success': False, 'message': 'Incorrect password'})

        
@app.route('/file', methods=['POST'])
def upload_file():
    path = PATH+'/Project/Musically/users/'+username
    app.config['UPLOAD_FOLDER'] = path
    file = request.files['file']
    filename = file.filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    source_folder = PATH+'/Project/Musically/users/'+username
    destination_folder = PATH+'/Project/Musically/songs/User'
    for filename in os.listdir(source_folder):
        if filename.endswith('.mp3'):
            source_path = os.path.join(source_folder, filename)
            destination_path = os.path.join(destination_folder, filename)
            shutil.copy2(source_path, destination_path)
    return jsonify({'message': 'File uploaded successfully'})
    
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8000)
