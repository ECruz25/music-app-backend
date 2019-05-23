from flask import Flask, request
app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def hello():
    
    if request.method == "GET":
        return "Hello"
    else:
        print(request)
        return 200
