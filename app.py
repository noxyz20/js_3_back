from flask import Flask, request, jsonify, session, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
from video import Video
import json

app = Flask(__name__)
cors = CORS()
cors.init_app(app, resource={r"/api/*": {"origins": "*"}})
app.config.update(SECRET_KEY=os.urandom(24))

@app.route('/upload', methods=['POST'])
def upload():
    for fname in request.files:
        f = request.files.get(fname)
        print(f)
    f.save('./uploads/%s' % secure_filename(fname))
    curr_video = Video('./uploads/'+fname)
    
    frame_array = curr_video.treatement()
    
    name, video, frame = curr_video.export()
    
    session['name'] = json.dumps(name)
    session['video'] = json.dumps(video)
    session['frame'] = json.dumps(frame)

    return str(frame_array)

@app.route('/save', methods=['GET'])
def save():
    keyframes = request.args.get('keyframes')

    curr_video = Video(session.get('video'), session.get('name'), session.get('frame'))
    curr_video.save_ressource(keyframes)

@app.route("/src/<path:filename>")
def static_dir(filename):
    print(filename)
    return send_from_directory("",filename)

if __name__ == '__main__':
    if not os.path.exists('./uploads'):
        os.mkdir('./uploads')
    app.run(debug=True)