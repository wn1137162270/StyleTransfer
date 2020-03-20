from werkzeug.utils import secure_filename
from flask import Flask, jsonify, request, make_response, send_from_directory
import os
import requests
import FilenameUtil
import MultiStyleTransfer
app = Flask(__name__)
UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = {'png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'], strict_slashes=False)
def upload():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['img']
    outFileName = request.form['outFileName']
    algType = request.form['algType']
    if f and allowed_file(f.filename):
        file_name = secure_filename(f.filename)
        ext = file_name.rsplit('.', 1)[1]
        new_filename = FilenameUtil.create_uuid() + '.' + ext
        f.save(os.path.join(file_dir, new_filename))
        MultiStyleTransfer.evaluate(os.path.join(file_dir, new_filename),512,"models_images/21styles/" + algType + ".jpg","./output/"+outFileName,"models/21styles.model", 512, 128, 0)
        return jsonify({"success": 0, "msg": "上传成功"})
    else:
        return jsonify({"error": 1001, "msg": "上传失败"})

@app.route('/avatarUrl', methods=['POST'])
def avatarUrl():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    outFileName = request.form['outFileName']
    algType = request.form['algType']
    avatarUrl = request.form['avatarUrl']
    print(avatarUrl)
    avatarPath = os.path.join(file_dir, "112233.jpg");
    r = requests.request('get',avatarUrl)
    with open(avatarPath,'wb') as f: 
        f.write(r.content) 
    f.close()
    MultiStyleTransfer.evaluate(avatarPath,512,"models_images/21styles/" + algType + ".jpg","./output/"+outFileName,"models/21styles.model", 512, 128, 0)
    return jsonify({"success": 0, "msg": "上传成功"})

@app.route('/download/<string:filename>', methods=['GET'])
def download(filename):
    if request.method == "GET":
        if os.path.isfile(os.path.join('output', filename)):
            return send_from_directory('output', filename, as_attachment=True)
        pass

@app.route('/show/<string:filename>', methods=['GET'])
def show_picture(filename):
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if request.method == 'GET':
        if filename is None:
            pass
        else:
            image_data = open(os.path.join(file_dir, '%s' % filename), "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/png'
            return response


if __name__ == '__main__':
    app.run(debug=True)
