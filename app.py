from flask import Flask, request, jsonify, session
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
from video import Video

app = Flask(__name__)
cors = CORS()
cors.init_app(app, resource={r"/api/*": {"origins": "*"}})

@app.route('/upload', methods=['POST'])
def upload():
    for fname in request.files:
        f = request.files.get(fname)
        print(f)
    f.save('./uploads/%s' % secure_filename(fname))
    curr_video = Video('./uploads/'+fname)
    
    frame_array = curr_video.treatement()
    
    (session['name'], session['video'], session['frame'], session['film']) = curr_video.export()
    return str(frame_array)

@app.route('/save', methods=['GET'])
def save():
    keyframes = request.args.get('keyframes')

    curr_video = Video(session['video'], session['name'], session['frame'], session['film'])
    curr_video.save_ressource(keyframes)

if __name__ == '__main__':
    if not os.path.exists('./uploads'):
        os.mkdir('./uploads')
    app.run(debug=True)