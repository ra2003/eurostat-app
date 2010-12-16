from flask import Flask
from flaskext.genshi import Genshi, render_response
app = Flask(__name__)
genshi = Genshi(app)

@app.route('/')
def home():
    return render_response('index.html', dict())

@app.route('/embed')
def embed():
    return render_response('embed.html', dict())



if __name__ == '__main__':
    app.run(debug=True)

