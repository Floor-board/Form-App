from flask import Flask, url_for, render_template, request

app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)
#global login
login = False
username = ''
email =  ''
password = ''
@app.route("/")
def render_index():
    return render_template('index.html')

@app.route("/response")
def render_response():
    global login
    if login == False:
        global username
        global email
        global password
        username = request.args['usrnm'] 
        email = request.args['email'] 
        password = request.args['pwrd']
        reply1 = username
        reply2 = email
        reply3 = password 
        
        login = True 
        return render_template('response.html', response1 = reply1, response2 = reply2, response3 = reply3)
    elif login == True:
        Bcolor = request.args['Mycolor']
        reply4 = Bcolor
        reply1 = username
        reply2 = email
        reply3 = password 
        return render_template('response.html', response1 = reply1, response2 = reply2, response3 = reply3, response4 = reply4)
if __name__=="__main__":
    app.run(debug=True)

