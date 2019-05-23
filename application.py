from flask import Flask, request, jsonify
app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def hello():
    print("holaaa")
    if request.method == "GET":
        return "Hello"
    else:
        print(request.form)
        return jsonify("a")
