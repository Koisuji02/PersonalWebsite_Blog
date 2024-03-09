import sqlite3

DATABASE_PATH = 'db/blog.db'

# db con tabella UTENTI(id, email, password), POST (id, titolo, materia, like, html), LIKES (id_utente, id_post) [per legare utente e post in modo che risulti tra i suoi post "salvati" preferiti]

#! TROVA UTENTI TRAMITE EMAIL
def get_user_by_email(email):
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM UTENTI WHERE email = ?'
    cursor.execute(sql, (email,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user

#! TROVA UTENTI TRAMITE ID
def get_user_by_id(id):
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM UTENTI WHERE id = ?'
    cursor.execute(sql, (id,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user

#! AGGIUNGERE UTENTE AL DB
def add_user(user):
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'INSERT INTO UTENTI(email,password) VALUES(?,?)'
    # se si riesce nell'esecuzione di aggiungere un utente
    try:
        cursor.execute(sql, (user['email'], user['password']))
        conn.commit()
        success = True

    # altrimenti si verifica eccezione
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success

#! PRENDI SINGOLO POST DA ID
def get_post(id):
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM POST WHERE POST.id = ?'
    cursor.execute(sql, (id,))
    post = cursor.fetchone()

    cursor.close()
    conn.close()

    return post

#! PRENDI TUTTI I POSTS
def get_posts():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM POST ORDER BY POST.id DESC'
    cursor.execute(sql)
    posts = cursor.fetchall()

    cursor.close()
    conn.close()

    return posts

#! PRENDI TUTTI GLI UTENTI
def get_users():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM UTENTI'
    cursor.execute(sql)
    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return users

#! PRENDI TUTTI I LIKES (TABELLA CON ASSOCIAZIONE UTENTE-POST)
def get_likes():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM LIKES'
    cursor.execute(sql)
    likes = cursor.fetchall()

    cursor.close()
    conn.close()

    return likes

#! PRENDI TUTTI GLI UTENTI CHE HANNO MESSO LIKE AD UNO SPECIFICO POST (per poi fare comparazione se utente ha già messo like a quel post)
def get_users_likes(id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    sql = 'SELECT id_utente FROM LIKES WHERE id_post = ?'
    cursor.execute(sql, (id,))
    users_like = cursor.fetchall()

    cursor.close()
    conn.close()

    return users_like

#! CERCA POST
def search_posts(query):
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # USO "LIKE" PER CERCARE I POST PER TITOLO
    sql = 'SELECT * FROM POST WHERE titolo LIKE ?'
    cursor.execute(sql, ('%' + query + '%',))
    filtered_posts = cursor.fetchall()

    cursor.close()
    conn.close()

    return filtered_posts

#! FITLRA PER MATERIA
def get_posts_by_materia(materia):
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM POST WHERE materia = ? ORDER BY id DESC'
    cursor.execute(sql, (materia,))
    posts = cursor.fetchall()

    cursor.close()
    conn.close()

    return posts

#! POST PIACIUTI PER UTENTE
def get_liked_posts(user_id):
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Seleziona i post che sono stati marcati come preferiti dall'utente specifico
    sql = 'SELECT POST.* FROM POST, LIKES WHERE POST.id = LIKES.id_post AND LIKES.id_utente = ? ORDER BY POST.id DESC'
    cursor.execute(sql, (user_id,))
    liked_posts = cursor.fetchall()

    cursor.close()
    conn.close()

    return liked_posts

#! AGGIUNGO LIKE (id_utente, id_post) ALLA TABELLA LIKES
def add_like(user_id, post_id):
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'INSERT INTO LIKES(id_utente,id_post) VALUES(?,?)'
    # se si riesce nell'esecuzione di aggiungere un like
    try:
        cursor.execute(sql, (user_id, post_id))
        conn.commit()
        success = True

    # altrimenti si verifica eccezione
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success

#! INCREMENTO LIKE DEL POST
def add_post_like(post_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    sql = 'UPDATE POST SET like=like+1 WHERE id=?'
    try:
        cursor.execute(sql, (post_id,))
        conn.commit()
        success = True

    # altrimenti si verifica eccezione
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success

#! TOLGO LIKE (id_utente, id_post) DALLA TABELLA LIKES
def delete_like(user_id, post_id):
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'DELETE FROM LIKES WHERE id_utente = ? AND id_post = ?'
    # se si riesce nell'esecuzione di aggiungere un like
    try:
        cursor.execute(sql, (user_id, post_id))
        conn.commit()
        success = True

    # altrimenti si verifica eccezione
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success

#! INCREMENTO LIKE DEL POST
def delete_post_like(post_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    sql = 'UPDATE POST SET like=like-1 WHERE id=?'
    try:
        cursor.execute(sql, (post_id,))
        conn.commit()
        success = True

    # altrimenti si verifica eccezione
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success