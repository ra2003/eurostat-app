from flask import Flask, request
from flaskext.genshi import Genshi, render_response
app = Flask(__name__)
genshi = Genshi(app)

@app.route('/')
def home():
    dataset_id = 'teina011'
    return render_response('index.html', dict(dataset_id=dataset_id))

@app.route('/embed')
def embed():
    dataset_id = request.args.get('datasetId', 'teina011')
    return render_response('embed.html', dict(dataset_id=dataset_id))


if __name__ == '__main__':
    app.run(debug=True)

