from flask import Flask, request, jsonify, session
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
from video import Video

app = Flask(__name__)
cors = CORS()
cors.init_app(app, resource={r"/api/*": {"origins": "*"}})
test = None
@app.route('/upload', methods=['POST'])
def upload():
    for fname in request.files:
        f = request.files.get(fname)
        print(f)
    f.save('./uploads/%s' % secure_filename(fname))
    session['test'] = Video('./uploads/'+fname)
    frame_array = test.treatement()
    #test.save_ressource()
    return str(frame_array)

@app.route('/save', methods=['GET'])
def save():
    keyframes = request.args.get('keyframes')
    session['test'].save_ressource(keyframes)

if __name__ == '__main__':
    if not os.path.exists('./uploads'):
        os.mkdir('./uploads')
    app.run(debug=True)