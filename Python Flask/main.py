from flask import Flask, render_template, jsonify, session, request, flash, Request
from flask_socketio import SocketIO
from database import Database
from flask_mail import Mail, Message


app = Flask(__name__)
app.config["SECRET_KEY"] = "THIS IS MY SECRET KEY & THE KEY IS REALLY LONG"
NAME_KEY = "nameKey"
socketio = SocketIO(app)

"""
-used for sending an email to account
-make sure that you aren't using a firewall,
-note that your python version has to be supported by eventlet version as well
"""

app.config['MAIL_SERVER'] = "smtp.googlemail.com" # don't touch this
app.config['MAIL_PORT'] = 587 # don't touch this
app.config['MAIL_USE_TLS'] = True # don't touch this
app.config['MAIL_USERNAME'] = "email@gmail.com"  # enter your email here
app.config['MAIL_DEFAULT_SENDER'] = "email@gmail.com" # enter your email here
app.config['MAIL_PASSWORD'] = "password" # put password here
mail = Mail(app)

@app.route("/", methods = ["POST", "GET"])
def sessions():
    """
    -Makes user have to enter username
    -Saves the name entered into sessions
    -Loads the messages HTML page after this
    :param: None
    :return: HTML page
    """
    if request.method == "POST":
        name = request.form["usernameInput"]
        if len(name) >= 1:
            session[NAME_KEY] = name
            return mainPage()
    return render_template("usernamePage.html")

@app.route("/mainPage", methods = ["GET", "POST"])
def mainPage():
    """
    -make sure that user has given a name AND request method is POST
    :param: None
    :return: HTML page
    """
    if NAME_KEY in session:
        return render_template("mainPageTwo.html")
    return render_template("usernamePage.html")


@app.route("/getName")
def getName():
    """
    -returns name from session 
    :param: None
    :return output: dictionary - json
    """
    output = {"name": ""}
    if NAME_KEY in session:
        output["name"] = session[NAME_KEY]
    print("output", output)
    return jsonify(output)

@app.route("/getMessages")
def getMessages():
    """
    -return all the messages from the database and display is on the screen
    :param: None
    :return: messages - json
    """
    dataBase = Database()
    messages = dataBase.getMessages()
    return jsonify(messages)


@app.route("/contact", methods = ["GET", "POST"])
def contact():
    """
    -make user go to contact page
    -get user email address and send message to email address linked to page
    :param: None
    :return: HTML page
    """
    if request.method == "GET":
        print("Hello")
        return render_template("contactTwo.html")
    print("Hello again")
    subject = request.form["subject"]
    email = request.form["emailAddress"]
    message = request.form["message"]
    print(subject, email, message)
    msg = Message(subject, recipients=["heidaranwari@gmail.com"], body=message)
    mail.send(msg)
    return render_template("contactTwo.html")


def messageReceived(methods = ["GET", "POST"]):
    print("Message was received")

@app.route("/logout")
def logout():
    """
    logs user out
    :param: None
    :return: None
    """
    session.pop(NAME_KEY, None)
    return sessions()


@socketio.on("my event")
def handle_my_custom_event(json, methods = ["GET", "POST"]):
    """
    -emit messages recieved to others and save it
    :param json: json
    :return json: json
    """
    input = dict(json)
    if "userName" in input and input["userName"] != "":
        dataBase = Database()
        dataBase.addMessage(input["message"], input["userName"])
    print("recieved my event" + str(json))
    socketio.emit("my response", json, callback=messageReceived)

if __name__ == "__main__":
    socketio.run(app, debug=True)
