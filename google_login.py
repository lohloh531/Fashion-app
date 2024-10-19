from flask import Flask, url_for, redirect, session
from authlib.integrations.flask_client import OAuth 

app = Flask(_name_)
app.secret.key = 'random secret'

oauth = OAuth(app)
google = oauth.register(
    name = 'google',
    client_id = '226621739167-rv920bjgu6744rvgcsrni0gv1vpcb3vm.apps.googleusercontent.com',
    client_secret='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',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    acess_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapls.com/oauth2/v1',
    client_kwargs={'scope':'openid profile email'},
)

@app.route('/')
def hello_world():
    email = dict(session).get('email',None)
    return f'Hello, {email}!'

@app.route('/login')
def login():
    google = oauth.create_client('google')
    redirected_url = url_for('authorize', _external=True)
    return oauth.twitter.authorize_redirect(redirect_url)

@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    resp.raise_for_status()
    user_info = resp.json()
    # do something with the token and profile
    session['email']=user_info['email']
    return redirect('/')

