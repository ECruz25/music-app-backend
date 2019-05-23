from flask import Flask
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == 'GET':
        return "Hello World!"
    if request.method == 'POST':
        print(request)
