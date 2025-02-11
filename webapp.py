import pymongo
from flask import Flask, request, render_template, flash, url_for
from markupsafe import Markup
from flask import redirect
from flask import session
import os
import sys
import pprint
from flask_oauthlib.client import OAuth
from flask import render_template
from markupsafe import Markup
from pymongo import DESCENDING 

# This code originally from https://github.com/lepture/flask-oauthlib/blob/master/example/github.py
# Edited by P. Conrad for SPIS 2016 to add getting Client Id and Secret from
# environment variables, so that this will work on Heroku.
# Edited by S. Adams for Designing Software for the Web to add comments and remove flash messaging

app = Flask(__name__)

app.debug = False #Change this to False for production
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' #Remove once done debugging

app.secret_key = os.environ['SECRET_KEY'] #used to sign session cookies
oauth = OAuth(app)
oauth.init_app(app) #initialize the app to be able to make requests for user information

#Set up GitHub as OAuth provider
github = oauth.remote_app(
    'github',
    consumer_key=os.environ['GITHUB_CLIENT_ID'], #your web app's "username" for github's OAuth
    consumer_secret=os.environ['GITHUB_CLIENT_SECRET'],#your web app's "password" for github's OAuth
    base_url='https://api.github.com/',
    request_token_params={'scope': 'user:email'}, #request read-only access to the user's email.  For a list of possible scopes, see developer.github.com/apps/building-oauth-apps/scopes-for-oauth-apps
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',  
    authorize_url='https://github.com/login/oauth/authorize' #URL for github's OAuth login
)

connection_string = os.environ["MONGO_CONNECTION_STRING"]
db_name = os.environ["MONGO_DBNAME"]

client = pymongo.MongoClient(connection_string)
db = client[db_name]
collection=db['database1collection']
x=0

for anything in collection.find():
    print(anything)
       
#context processors run before templates are rendered and add variable(s) to the template's context
#context processors must return a dictionary
#this context processor adds the variable logged_in to the conext for all templates
@app.context_processor
def inject_logged_in():
    is_logged_in = 'github_token' in session #this will be true if the token is in the session and false otherwise
    return {"logged_in":is_logged_in}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/page1')
def page1():
    return render_template('page1.html')

@app.route('/page2')
def page2():
    return render_template('page2.html')

@app.route('/answerForumOne',methods=['GET','POST'])
def renderForumOneAnswers():
    if "user_data" in session:
        forumPost=request.form['ques1']
        doc = {"username":session['user_data']['login'], "number":"ee","text":forumPost}
     
        collection.insert_one(doc)
    for anything in collection.find():
        firstPost=anything["text"]
    firstPost=get_posts()    
    return render_template('page1.html', firstPost=firstPost)

   
#def get_posts():
  #  option = []
  #  for s in collection.find().sort('_id', DESCENDING):
      #  formatted_post = f"<pre>{s['username']} : {s['text']}</pre>"

    return render_template('page1.html')
#redirect to GitHub's OAuth page and confirm callback URL
@app.route('/login')
def login():
    return github.authorize(callback=url_for('authorized', _external=True, _scheme='https'))#https://www.perplexity.ai/search/im-getting-this-error-on-githu-R6uLkA9sR_Go8xtSsoG7JQ

@app.route('/logout')
def logout():
    session.clear()
    return render_template('message.html', message='You were logged out')

@app.route('/login/authorized')
def authorized():
    resp = github.authorized_response()
    if resp is None:
        session.clear()
        message = 'Access denied: reason=' + request.args['error'] + ' error=' + request.args['error_description'] + ' full=' + pprint.pformat(request.args)      
    else:
        try:
            session['github_token'] = (resp['access_token'], '') #save the token to prove that the user logged in
            session['user_data']=github.get('user').data
            #pprint.pprint(vars(github['/email']))
            #pprint.pprint(vars(github['api/2/accounts/profile/']))
            message='You were successfully logged in as ' + session['user_data']['login'] + '.'
        except Exception as inst:
            session.clear()
            print(inst)
            message='Unable to login, please try again.  '
    return render_template('index.html', message=message)

@app.route('/googleb4c3aeedcc2dd103.html')
def render_google_verification():
    return render_template('googleb4c3aeedcc2dd103.html')

def get_posts():
    messages=[]
    userName=[]
    for s in collection.find():
        messages.append(s["text"])
        userName.append(s["username"])
    option=""
    for s in collection.find():
        option += Markup("<pre>" + str(s["username"]) + " : " + str(s["text"])  + "</pre>") #Use Markup so <, >, " are not escaped lt, gt, etc.
    return option
   
#the tokengetter is automatically called to check who is logged in.
@github.tokengetter
def get_github_oauth_token():
    return session['github_token']   

if __name__ == '__main__':
    app.run()

