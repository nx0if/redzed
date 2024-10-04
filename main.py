from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/welcome', methods=['GET'])
def welcome():
    return jsonify({"status": "welcome"})

if __name__ == '__main__':
    app.run(debug=True)
