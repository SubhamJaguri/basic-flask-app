from flask import Flask, url_for, send_from_directory, request, jsonify, Blueprint , render_template
import os
#from PIL import Image
from werkzeug import secure_filename
#from extract_metadata import get_metadata
def get_metadata():
    files = []
    json_object = {"files": []}
    with open("saved_files.txt", "r") as file:
        while True:
            line = file.readline()
            if not line:
                break
            else:
                files.append(line.strip())
    for i in files:
        metadata = {}
        metadata['Name'] = i.split("uploads")[-1].replace("/", "")
        metadata['Size'] = os.stat(i).st_size/1000000
        im = Image.open(i)
        width, height = im.size
        metadata['Resolution'] = str(width) + "x" + str(height)
        metadata['URL'] = "/img/" + metadata['Name']

        json_object['files'].append(metadata)

    os.remove("saved_files.txt")
    # [os.remove(i) for i in files]

    return json_object
app = Flask(__name__)

ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'pgm']
PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = '{}/uploads/'.format(PROJECT_HOME)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

blueprint = Blueprint('site', __name__, static_url_path='/img', static_folder=PROJECT_HOME + "/uploads")
app.register_blueprint(blueprint)

def get_extension(name):
    if name.split(".")[-1] in ALLOWED_EXTENSIONS:
        return True
    else:
        return False


def create_new_folder(local_dir):
    newpath = local_dir
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath

@app.route('/', methods = ["GET",'POST'])
def api_root():
    if request.method == 'POST' and request.files['file']:
        if os.path.exists("saved_files.txt"):
            os.remove("saved_files.txt")

        img = request.files.getlist("file")
        if not all([get_extension(secure_filename(i.filename)) for i in img]):
            return """
            Allowed types are only {} <br/>
            Change line 12 in server.py for
            additional extensions
            """.format(ALLOWED_EXTENSIONS)
        for i in img:
            img_name = secure_filename(i.filename)
            create_new_folder(app.config['UPLOAD_FOLDER'])
            saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
            with open("saved_files.txt", "a") as file:
                file.write(saved_path + "\n")
            file.close()
            i.save(saved_path)
        metadata = get_metadata()
        return jsonify(metadata)
    else:
    	return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = False)
