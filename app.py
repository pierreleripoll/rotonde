from flask import *

app = Flask(__name__)

@app.route('/api/sum/<int:a>/<int:b>')
def sum(a, b):
    c = a + b
    return jsonify(args=[a, b], result=c)

if __name__ == '__main__':
    app.run(debug=True)
