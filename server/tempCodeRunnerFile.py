@app.route('/signup_account', methods=['POST'])
def signup_credentials():
    connection = mycon.connect(
        host="localhost",
        user="root",
        password="admin",
        database="musically"
    )

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
    
    username = request.json.get('username')
    password = request.json.get('password')
    username = username.lower()
    hashed_pass = hash_string(password)

    if username == '':
        return jsonify({'success': False, 'message': 'Username cannot be empty'})
    elif username in users:
        return jsonify({'success': False, 'message': 'Username already taken'})
    elif password == '':
        return jsonify({'success': False, 'message': 'Password cannot be empty'})
    else:
        return jsonify({'success': True, 'message': 'Welcome! Please log in to continue'})
