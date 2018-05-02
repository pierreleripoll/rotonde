from flask import *

app = Flask(__name__)

@app.route('/api/sum/<int:a>/<int:b>')
def sum(a, b):
    c = a + b
    return jsonify(args=[a, b], result=c)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
