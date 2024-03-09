# import module
from flask import Flask, render_template, request, session, redirect, flash, url_for
import dao
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User

# create the application
app = Flask(__name__)
app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

#TODO Capire come caricare il sito gratis online

#! HOMEPAGE + FILTRO PER MATERIA (DA NAVBAR)
@app.route('/', methods=['GET', 'POST'])
def home():
    materia_filter = request.args.get('materia')
    posts = dao.get_posts_by_materia(materia_filter) if materia_filter else dao.get_posts()
    return render_template('home.html', posts=posts, materia_filter=materia_filter)


#! POST.HTML PER OGNI SINGOLO POST (quello che prima era single.html)
@app.route('/posts/<int:id>')
def post_html(id):
    post = dao.get_post(id)
    # passo la lista degli utenti che hanno messo like a quello specifico post
    users_like = dao.get_users_likes(id)
    return render_template('articoli/' + post['html'], post=post, users=users_like)

#! GESTIONE NUOVI LIKES
@app.route('/posts/<int:post_id>/<int:user_id>')
@login_required
def new_like(post_id, user_id):
    # qua incremento il numero di like nella tabella POST e verifico che sia andato ok
    success = dao.add_post_like(post_id)
    #!DEBUG SU ADD_POST
    #if success:
        #flash('Like aggiunto correttamente in POST', 'success')
    #else:
        #flash('Errore nell\'aggiunta del like in POST: riprova!', 'danger')
        #return redirect(url_for('post_html', id=post_id))
    
    # qua aggiungo una entry nella tabella LIKES con l'utente e il post
    success = dao.add_like(user_id, post_id)
    #!DEBUG SU ADD_LIKE
    #if success:
        #flash('Like aggiunto correttamente in LIKES', 'success')
    #else:
        #flash('Errore nell\'aggiunta del like in LIKES: riprova!', 'danger')
    return redirect(url_for('post_html', id=post_id))

#! GESTIONE NUOVI LIKES
@app.route('/posts/<int:post_id>/<int:user_id>/remove')
@login_required
def remove_like(post_id, user_id):
    # qua incremento il numero di like nella tabella POST e verifico che sia andato ok
    success = dao.delete_post_like(post_id)
    #!DEBUG SU ADD_POST
    #if success:
        #flash('Like aggiunto correttamente in POST', 'success')
    #else:
        #flash('Errore nell\'aggiunta del like in POST: riprova!', 'danger')
        #return redirect(url_for('post_html', id=post_id))
    
    # qua aggiungo una entry nella tabella LIKES con l'utente e il post
    success = dao.delete_like(user_id, post_id)
    #!DEBUG SU ADD_LIKE
    #if success:
        #flash('Like aggiunto correttamente in LIKES', 'success')
    #else:
        #flash('Errore nell\'aggiunta del like in LIKES: riprova!', 'danger')
    return redirect(url_for('post_html', id=post_id))

#! NO_AUTENTICATO FLASH
@app.route('/no_autenticated')
def no_authenticated():
    flash('Per mettere like devi essere loggato! Fai il login.', 'danger')
    return redirect(url_for('login'))

#! LOGIN MANAGER (come flask deve caricare l'utente dal dao)
@login_manager.user_loader
def load_user(user_id):
    utente = dao.get_user_by_id(user_id)

    if utente is not None:
        user = User(id=utente['id'], email=utente['email'], password=utente['password'])
    else:
        user = None

    return user

#! LOGIN
@app.route('/accedi')
def login():
    return render_template('login.html')

@app.route('/accedi', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user = dao.get_user_by_email(email)

    # se non c'è utente o password sbagliata
    if not user or not check_password_hash(user['password'], password):
        flash('Credenziali non valide, riprovare!', 'danger')
        return redirect(url_for('login'))
    
    # altrimenti se tutto ok
    else:
        new = User(id=user['id'], email=user['email'], password=user['password'])
        login_user(new, True)
        flash('Login con successo!', 'success')

        return redirect(url_for('home'))

#! SIGNUP (REGISTRAZIONE)
@app.route('/iscriviti')
def signup():
    return render_template('signup.html')


@app.route('/iscriviti', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user_in_db = dao.get_user_by_email(email)

    if user_in_db:
        flash('C\'è già un utente registrato con questo nickname!', 'danger')
        return redirect(url_for('signup'))
    else:
        new_user = {
            "email": email,
            "password": generate_password_hash(password, method='pbkdf2:sha256')
        }

        success = dao.add_user(new_user)

        if success:
            flash('Utente creato correttamente', 'success')
            return redirect(url_for('home'))
        else:
            flash('Errore nella creazione del utente: riprova!', 'danger')

    return redirect(url_for('signup'))

#! LOGOUT (ESCI)
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

#! SEARCH POST PER TITOLO
@app.route('/search')
def search():
    query = request.args.get('query', '')
    # Use the query to filter posts
    filtered_posts = dao.search_posts(query)
    return render_template('search_results.html', query=query, posts=filtered_posts)

#! POST PIACIUTI DALL'UTENTE
@app.route('/liked_posts')
@login_required
def liked_posts():
    # Retrieve posts liked by the current user
    liked_posts = dao.get_liked_posts(current_user.id)
    return render_template('liked_posts.html', posts=liked_posts)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)