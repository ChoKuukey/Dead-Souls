from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return """
    <p>Hello, World!</p>
    <h1>Сева какашка</h1>

    """

if __name__ == "__main__":
    app.run(host="192.168.3.123", port=5000)