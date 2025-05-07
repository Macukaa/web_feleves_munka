from bottle import Bottle, run, route, redirect, request, response, error
import sqlite3
import os
filepath = os.path.abspath("teamfinder.db")
connection = sqlite3.connect("C:\Webprog\project\database.db")
cursor = connection.cursor()
app = Bottle()

@app.route('/')
def index():
    return '''
        <head>
            <title></title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 20px;
            }
            h1 {
                color: #333;
            }
            input[type="button"] {
                background-color: #4CAF50;
                color: white;
                padding: 10px 15px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            input[type="button"]:hover {
                background-color: #45a049;
            }
            hr {
                border: 1px solid #ccc;
                margin: 20px 0;
            }
        </style>
        </head>
        <h1>Üdvözöllek a weblapon</h1>
        <p>Kérlek jelentkezz be vagy regisztrálj</p>
        <input type="button" value="Bejelentkezés" onclick="window.location.href='/login'">
        <input type="button" value="Regisztráció" onclick="window.location.href='/register'">
    '''

@app.route('/login')
def login(): 
    return '''
        <head>
            <title>Bejelentkezés</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 20px;
            }
            h1 {
                color: #333;
            }
            input[type="text"], input[type="password"] {
                width: 20%;
                padding: 10px;
                margin: 10px 0;
                border: 1px solid #ccc;
                border-radius: 5px;
                box-sizing: border-box;
            }
            input[type="submit"] {
                background-color: #4CAF50;
                color: white;
                padding: 10px 15px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            input[type="submit"]:hover {
                background-color: #45a049;
            }
            hr {
                border: 1px solid #ccc;
                margin: 20px 0;
            }
        </style>
        </head>
        <h1>Bejelentkezés</h1>
        <form action="/login" method="post">
            <input type="text" name="username" placeholder="Felhasználónév" required>
            <input type="password" name="password" placeholder="Jelszó" required>
            <input type="submit" value="Bejelentkezés">
        </form>
    '''

@app.route('/login', method='POST')
def do_login():
    global username
    global password
    username = request.forms.get('username')
    password = request.forms.get('password')
    return handle_login(username, password)

def handle_login(username, password):
    users = [row[0] for row in cursor.execute("SELECT name FROM users").fetchall()]
    passwords = [row[0] for row in cursor.execute("SELECT password FROM users").fetchall()]
    for i in range(len(users)):
        if users[i] == username:
            if passwords[i] == password:
                response.set_cookie("islogin", "true", maxage=600, path="/")
                response.set_cookie("username", username, path="/")
                return redirect('/home')
               
            else:
                return '''
                   
                <script>
                    document.addEventListener("DOMContentLoaded", function() {
                    if(confirm("Hibás jelszó vagy felhasználónév!")) {
                    window.location.href = "/login";
                    } else {
                    window.location.href = "/login";
                    }
                    });
                </script>

    ''' 
    else:
        return '''
        <script>
            document.addEventListener("DOMContentLoaded", function() {
                if(confirm("Hibás jelszó vagy felhasználónév!")) {
                    window.location.href = "/login";
                } else {
                    window.location.href = "/login";
                }
            });
        </script>

        ''' 


@app.route('/register')
def register():
    return '''
        <head>
            <title>Regisztráció</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 20px;
            }
            h1 {
                color: #333;
            }
            input[type="text"], input[type="password"] {
                width: 20%;
                padding: 10px;
                margin: 10px 0;
                border: 1px solid #ccc;
                border-radius: 5px;
                box-sizing: border-box;
            }
            input[type="submit"] {
                background-color: #4CAF50;
                color: white;
                padding: 10px 15px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            input[type="submit"]:hover {
                background-color: #45a049;
            }
            hr {
                border: 1px solid #ccc;
                margin: 20px 0;
            }
        </style>
        </head>
        <h1>Regisztráció</h1>
        <form action="/register" method="post">
            <input type="text" name="username" placeholder="Felhasználónév" required>
            <input type="password" name="password" placeholder="Jelszó"  required>
            <input type="submit" value="Regisztráció">
        </form>
    '''

@app.route('/register', method='POST')
def do_register():
    username = request.forms.get('username')
    password = request.forms.get('password')
    return handle_register(username, password)

def handle_register(username, password):
    users = [row[0] for row in cursor.execute("SELECT name FROM users").fetchall()]
    if username in users:
        return '''
        <script>
            document.addEventListener("DOMContentLoaded", function() {
                if(confirm("Ez a felhasználónév már létezik!")) {
                    window.location.href = "/register";
                } else {
                    window.location.href = "/register";
                }
            });
        </script>

        ''' 
    else:
        cursor.execute("INSERT INTO users (name, password) VALUES (?, ?)", (username, password))
        connection.commit()
        return '''
        <script>
            document.addEventListener("DOMContentLoaded", function() {
                if(confirm("Sikeres regisztráció!")) {
                    window.location.href = "/home";
                } else {
                    window.location.href = "/home";
                }
            });
        </script>

        ''' 

@app.route('/home')
def home():
    islogin = request.get_cookie("islogin")
    if not islogin:
        return redirect('/login')
    else:
        username = request.get_cookie("username")
        posts_html = ""
        for row in cursor.execute(f"SELECT * FROM posts").fetchall():
            username = row[0]
            title = row[1]
            content = row[2]
            platforms = row[3]
            time = row[4]
            id = row[5]
            posts_html += f'''
                <h2>{title}</h2>
                <p>{content}</p>
                <p>Platform: {platforms}</p>
                <p>Időpont: {time}</p>
                <p>Felhasználó: {username}</p>
                <p>Játék: {row[7]}</p>
                <input type="button" value="Jelentkezés" onclick="window.location.href='/signup/{id}'">
                <hr>
            '''
        platform_filter = request.query.platform
        if platform_filter:
            username = request.get_cookie("username")
            filtered_posts_html = ""
            for row in cursor.execute(f"SELECT * FROM posts WHERE platforms=?", (platform_filter,)).fetchall():
                username = row[0]
                title = row[1]
                content = row[2]
                platforms = row[3]
                time = row[4]
                id = row[5]
                filtered_posts_html += f'''
                    <h2>{title}</h2>
                    <p>{content}</p>
                    <p>Platform: {platforms}</p>
                    <p>Időpont: {time}</p>
                    <p>Felhasználó: {username}</p>
                    <p>Játék: {row[7]}</p>
                    <input type="button" value="Jelentkezés" onclick="window.location.href='/signup/{id}'">
                    <hr>
                '''
            posts_html = filtered_posts_html

        return '''
                <head>
                    <title>Főoldal</title>
                <style>
                    body{
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f4;
                        margin: 0;
                        padding: 20px;
                    }
                    h1 {
                        color: #333;
                    }
                    hr {
                        border: 1px solid #ccc;
                        margin: 20px 0;
                    }
                    select {
                        padding: 10px;
                        margin: 10px 0;
                        border: 1px solid #ccc;
                        border-radius: 5px;
                        box-sizing: border-box;
                    }
                    input[type="button"] {
                        background-color: #4CAF50;
                        color: white;
                        padding: 10px 15px;
                        border: none;
                        border-radius: 5px;
                        cursor: pointer;
                    }
                    input[type="button"]:hover {
                        background-color: #45a049;
                        color: white;
                        transition: background-color 0.3s ease;
                    }
                    input[value="Profil"] {
                    position: absolute;
                    top: 20px;
                    right: 20px;
                    }
                    input[value="Poszt kiírása"] {
                    position: absolute;
                    top: 60px;
                    right: 20px;
                    }
                    input[value="Kijelentkezés"] {
                    position: absolute;
                    top: 100px;
                    right: 20px;
                    }
                </style>
                </head>
                ''' + f'''
                <h1>Főoldal</h1>
                <p>Üdvözöllek a főoldalon!</p>
                
                <label for="platforms">Válassz egy platformot:</label>
                <select name="platforms" id="platforms" onchange="window.location.href='/home?platform=' + this.value">
                    <option value="">Összes</option>
                    <option value="PC" {"selected" if platform_filter == "PC" else ""}>PC</option>
                    <option value="Xbox" {"selected" if platform_filter == "Xbox" else ""}>Xbox</option>
                    <option value="PlayStation" {"selected" if platform_filter == "PlayStation" else ""}>PlayStation</option>
                </select>
                <br>
                <hr>
                <h2>Posztok:</h2>
                <input type="button" value="Profil" onclick="window.location.href='/profile'">
                <input type="button" value="Poszt kiírása" onclick="window.location.href='/post'">
                <input type="button" value="Kijelentkezés" onclick="window.location.href='/logout'">
            ''' + posts_html
@app.route('/signup/<id>')
def signup_id(id):
    islogin = request.get_cookie("islogin")
    if not islogin:
        return redirect('/login')
    else:
        cursor.execute("SELECT * FROM posts WHERE id=?", (id,))
        row = cursor.fetchone()
        if row:
            title = row[1]
            content = row[2]
            platforms = row[3]
            time = row[4]
            username = row[0]
            game = row[7]
            return '''
                <head>
                    <title>Jelentkezés</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f4;
                        margin: 0;
                        padding: 20px;
                    }
                    h1 {
                        color: #333;
                    }
                    input[type="text"], input[type="password"] {
                        width: 20%;
                        padding: 10px;
                        margin: 10px 0;
                        border: 1px solid #ccc;
                        border-radius: 5px;
                        box-sizing: border-box;
                    }
                    input[type="submit"] {
                        background-color: #4CAF50;
                        color: white;
                        padding: 10px 15px;
                        border: none;
                        border-radius: 5px;
                        cursor: pointer;
                    }
                    input[type="submit"]:hover {
                        background-color: #45a049;
                    }
                    hr {
                        border: 1px solid #ccc;
                        margin: 20px 0;
                    }
                </style>
                </head>
                ''' + f'''
                <h1>{title}</h1>
                <p>{content}</p>
                <p>Platform: {platforms}</p>
                <p>Időpont: {time}</p>
                <p>Felhasználó: {username}</p>
                <p>Játék: {game}</p>
                <p>Jelentkezés:</p>
                <form action="/signup/{id}" method="post">
                    <input type="text" name="username" placeholder="Felhasználónév" maxlength="20" required>
                    <input type="text" name="connection" placeholder="Kapcsolatfelvétel" maxlength="20" required>
                    <input type="submit" value="Jelentkezés">
                </form>
            '''
        else:
            return '''
                <h1>Hiba</h1>
                <p>Nincs ilyen poszt!</p>
                <input type="button" value="Vissza" onclick="window.location.href='/home'">
            '''

@app.route('/signup/<id>', method='POST')
def do_signup(id):
    islogin = request.get_cookie("islogin")
    if not islogin:
        return redirect('/login')
    else:
        username = request.forms.get('username')
        user_connection = request.forms.get('connection')
        cursor.execute("INSERT INTO signup (username, connection, id) VALUES (?, ?, ?)", (username, user_connection, id))
        connection.commit()
        return '''
        <script>
            document.addEventListener("DOMContentLoaded", function() {
                if(confirm("Sikeres jelentkezés!")) {
                    window.location.href = "/home";
                } else {
                    window.location.href = "/home";
                }
            });
        </script>

        ''' 
@app.route('/post')
def post():
    islogin = request.get_cookie("islogin")
    if not islogin:
        return redirect('/login')
    else:
        return '''
            <head>
                <title>Poszt kiírása</title>
            </head>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 20px;
                }
                h1 {
                    color: #333;
                }
                form {
                    background-color: #fff;
                    padding: 20px;
                    border-radius: 5px;
                    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                }
                input[type="text"], input[type="password"], textarea, select {
                    width: 100%;
                    padding: 10px;
                    margin: 10px 0;
                    border: 1px solid
                    border-radius: 5px;
                    box-sizing: border-box;
                }
                input[type="submit"] {
                    background-color: #4CAF50;
                    color: white;
                    padding: 10px 15px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                }
                input[type="submit"]:hover {
                    background-color: #45a049;
                }
                hr {
                    border: 1px solid #ccc;
                    margin: 20px 0;
                }
            </style>
            <h1>Poszt kiírása</h1>
            <form action="/post" method="post">
                <input type="text" name="title" placeholder="Cím" maxlength="50"required>
                <textarea name="content" placeholder="Tartalom" maxlength="100" required></textarea>
                <input type="text" name="game" placeholder="Írd ide a játékot!" maxlength="50" required>
                <label for="platforms">Válassz egy platformot:</label>
                <select name="platforms" id="platforms" required>
                    <option value="PC">PC</option>
                    <option value="Xbox">XboX</option>
                    <option value="PlayStation">PlayStation</option>
                </select>
                <label for="Mikor?">Válassz egy időpontot:</label>
                <select name="Mikor?" id="Mikor?" required>
                    <option value="Hétköznap délelőtt">Hétköznap délelőtt</option>
                    <option value="Hétköznap délután">Hétköznap délután</option>
                    <option value="Hétvégén">Hétvégén</option>
                </select>

                <input type="submit" value="Poszt kiírása">
            </form>
        '''
@app.route('/post', method='POST')
def do_post():
    islogin = request.get_cookie("islogin")
    if not islogin:
        return redirect('/login')
    else:
        title = request.forms.get('title')
        content = request.forms.get('content')
        platforms = request.forms.get('platforms')
        time = request.forms.get('Mikor?')
        username = request.get_cookie("username")
        game = request.forms.get('game')
        cursor.execute("INSERT INTO posts (username, title, content, platforms, time, game) VALUES (?, ?, ?, ?, ?, ?)", (username, title, content, platforms, time, game))
        connection.commit()
        return '''
        <script>
            document.addEventListener("DOMContentLoaded", function() {
                if(confirm("Sikeres poszt kiírás!")) {
                    window.location.href = "/home";
                } else {
                    window.location.href = "/home";
                }
            });
        </script>

        ''' 
@app.route('/profile')
def profile():
    islogin = request.get_cookie("islogin")
    if not islogin:
        return redirect('/login')
    else:
        html =''
        html2 =''
        username = request.get_cookie("username")
        for row in cursor.execute("SELECT * FROM posts WHERE username=?", (username,)).fetchall():
            title = row[1]
            content = row[2]
            platforms = row[3]
            time = row[4]
            id = row[5]
            game = row[7]
            for row in cursor.execute("SELECT * FROM signup WHERE id=?", (id,)).fetchall():
                username = row[0]
                connection = row[1]
                html2 +=f'''
                    <h2>{title}</h2>
                    <p>Felhasználó: {username}</p>
                    <p>Kapcsolatfelvétel: {connection}</p>
                    <hr>
                '''
            html +=f'''
                <h2>{title}</h2>
                <p>{content}</p>
                <p>Platform: {platforms}</p>
                <p>Időpont: {time}</p>
                <p>Felhasználó: {username}</p>
                <p>Játék: {game}</p>
                <form action="/profile" method="post">
                    <input type="hidden" name="name" value="{id}">
                    <input type="submit" value="Törlés">
                </form>
                <hr>
                '''
        return '''
            <head>
                <title>Profil</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 20px;
                }
                h1 {
                    color: #333;
                }
                hr {
                    border: 1px solid #ccc;
                    margin: 20px 0;
                }
                input[type="button"] {
                    background-color: #4CAF50;
                    color: white;
                    padding: 10px 15px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                }
                input[type="button"]:hover {
                    background-color: #45a049;
                    color: white;
                    transition: background-color 0.4s ease;
                    color: white;
                }
                form {
                    background-color: #fff;
                    padding: 20px;
                    border-radius: 5px;
                    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                }
                input[type="text"], input[type="password"], textarea, select {
                    width: 100%;
                    padding: 10px;
                    margin: 10px 0;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    box-sizing: border-box;
                }
                input[type="submit"] {
                    background-color: #4CAF50;
                    color: white;
                    padding: 10px 15px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                }
                input[type="submit"]:hover {
                    background-color: #45a049;
                }
                hr {
                    border: 1px solid #ccc;
                    margin: 20px 0;
                }
                input[value="Vissza a főoldalra"] {
                    position: absolute;
                    top: 20px;
                    right: 20px;
                }
            </style>
            </head>
            ''' + f'''
            <h1>Profil</h1>
            <p>Itt található a profilod!</p>
            <p>Felhasználónév: {username}</p>
            <input type="button" value="Profil szerkesztése" onclick="window.location.href='/edit_profile'">
            <input type="button" value="Vissza a főoldalra" onclick="window.location.href='/home'">
            <p>Posztjaid:</p>
        '''+ html +'''<p>Jelentkezések:</p>''' + html2
@app.route('/profile', method='POST')
def do_profile():
    islogin = request.get_cookie("islogin")
    if not islogin:
        return redirect('/login')
    else:
        id = request.forms.get('name')
        cursor.execute("DELETE FROM posts WHERE id=?", (id,))
        connection.commit()
        cursor.execute("DELETE FROM signup WHERE id=?", (id,))
        connection.commit()
        return redirect('/profile')
@app.route('/edit_profile')
def edit_profile():
    islogin = request.get_cookie("islogin")
    if not islogin:
        return redirect('/login')
    else:
        return '''
            <head>
                <title>Profil szerkesztése</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 20px;
                }
                h1 {
                    color: #333;
                }
                input[type="text"], input[type="password"] {
                    width: 20%;
                    padding: 10px;
                    margin: 10px 0;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    box-sizing: border-box;
                }
                input[type="submit"] {
                    background-color: #4CAF50;
                    color: white;
                    padding: 10px 15px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                }
                input[type="submit"]:hover {
                    background-color: #45a049;
                }
                hr {
                    border: 1px solid #ccc;
                    margin: 20px 0;
                }
            </style>
            </head>
            <h1>Profil szerkesztése</h1>
            <form action="/edit_profile" method="post">
                <input type="text" name="username" placeholder="Új felhasználónév" required>
                <input type="password" name="password" placeholder="Új jelszó" required>
                <input type="submit" value="Profil mentése">
            </form>
        '''
@app.route('/edit_profile', method='POST')
def do_edit_profile():
    islogin = request.get_cookie("islogin")
    if not islogin:
        return redirect('/login')
    else:
        newusername = request.forms.get('username')
        newpassword = request.forms.get('password')
        cursor.execute("UPDATE users SET name=?, password=? WHERE name=?", (newusername, newpassword, username))
        connection.commit()
        return response.delete_cookie("islogin", path="/") ,'''
        <script>
            document.addEventListener("DOMContentLoaded", function() {
                if(confirm("Sikeres profil módosítás! Kérlek jelentkezz be újra!")) {
                    window.location.href = "/login";
                } else {
                    window.location.href = "/login";
                }
            });
        </script>

        ''' 
@app.route('/logout')
def logout():
    response.delete_cookie("islogin", path="/")
    return '''
        <script>
            document.addEventListener("DOMContentLoaded", function() {
                if(confirm("Sikeres kijelentkezés!")) {
                    window.location.href = "/";
                } else {
                    window.location.href = "/";
                }
            });
        </script>

        ''' 
@app.error(404)
def error404(error):
    return '''
        <head>
            <title>404 - Nem található</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 20px;
            }
            h1 {
                color: #333;
            }
           </style>
        </head>
        <h1>404 - Nem található</h1>
        <p>A keresett oldal nem található!</p>
        <input type="button" value="Vissza a főoldalra" onclick="window.location.href='/'">
    '''

app.run(host='localhost', port=8080, debug=True, reloader=True)
connection.close()