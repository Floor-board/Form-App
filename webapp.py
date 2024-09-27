from flask import Flask, url_for, render_template, request

app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)

@app.route("/")
def render_index():
    return render_template('index.html')

@app.route("/response")
def render_response():
    username = request.args['usrnm'] 
    email = request.args['email'] 
    password = request.args['pwrd'] 
    
    reply1 = "Your Username is: " + username
    reply2 = "Your Email is: " + email
    reply3 = "Your Password is: " + password 
    
    return render_template('response.html', response1 = reply1, response2 = reply2, response3 = reply3)

if __name__=="__main__":
    app.run(debug=True)

