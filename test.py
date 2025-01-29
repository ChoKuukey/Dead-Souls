from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
<<<<<<< HEAD
    return "<p>Привет, Виталя!</p> \
            <p>Тирах-Тирах!!!</p>"
=======
    return "<p>Привет!</p>"
>>>>>>> 37e475313aca5d4bd269076279e35bacebecc77c
