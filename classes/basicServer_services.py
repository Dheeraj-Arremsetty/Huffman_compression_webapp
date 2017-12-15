import os, json
import pdb
import uuid
from flask import jsonify, request, Response, redirect, url_for, render_template, send_file
import huffman_text
from werkzeug.utils import secure_filename
BASE_PATH = str(os.path.realpath(__file__))
BASE_PATH = BASE_PATH.replace('basicServer_services.pyc', '')
BASE_PATH = BASE_PATH.replace('basicServer_services.pyo', '')
BASE_PATH = BASE_PATH.replace('basicServer_services.py', '')
UPLOAD_FOLDER = '../data/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


CLASS_PATH = BASE_PATH.replace('classes', '')

def register_services(app, WSGI_PATH_PREFIX):
    BaseServices(app, WSGI_PATH_PREFIX)


class BaseServices:
    def __init__(self, app, WSGI_PATH_PREFIX):
        self.session_users = {}
        self.app = app
        self.DATA_PATH = self.app.config['DATA_PATH']

        print'----------------------------------------------------------------------------'
        print '                        Elastic is Stretching'
        print'----------------------------------------------------------------------------'
        print '                        Register MDMDQ API'
        print'----------------------------------------------------------------------------'
        #       ----------------------------------------------------------------------------
        #                                 MDMDQ Services
        #       ----------------------------------------------------------------------------
        self.app.add_url_rule(WSGI_PATH_PREFIX + '/services/demo', 'demo', self.demo, methods=['POST', 'GET'])
        self.app.add_url_rule(WSGI_PATH_PREFIX + '/services/giveJson', 'giveJson', self.giveJson, methods=['POST', 'GET'])
        self.app.add_url_rule(WSGI_PATH_PREFIX + '/services/add', 'add', self.add, methods=['POST', 'GET'])
        self.app.add_url_rule(WSGI_PATH_PREFIX + '/services/upload_file', 'upload_file', self.add, methods=['POST', 'GET'])
        self.app.add_url_rule(WSGI_PATH_PREFIX + '/services/upload', 'upload', self.upload,
                              methods=['POST', 'GET'])
        self.app.add_url_rule(WSGI_PATH_PREFIX + '/services/download', 'download', self.download,
                              methods=['POST', 'GET'])
        self.app.add_url_rule(WSGI_PATH_PREFIX + '/services/decrypt_page', 'decrypt_page', self.decrypt_page,
                              methods=['POST', 'GET'])
        self.app.add_url_rule(WSGI_PATH_PREFIX + '/services/upload_decrypt', 'upload_decrypt', self.upload_decrypt,
                              methods=['POST', 'GET'])

        self.app.add_url_rule(WSGI_PATH_PREFIX + '/services/word_cloud', 'word_cloud', self.word_cloud,
                              methods=['POST', 'GET'])




    def demo(self):
        return  'In DEMO method'

    def giveJson(self):
        _d = {i:i*'*' for i in xrange(55)}
        print _d
        return jsonify({"data":_d})

    def getparams(self, request):
        return request.form if (request.method == 'POST') else request.args

    def add(self):
        #http://0.0.0.0:5050/basicServer/services/add?a=100&b=200
        params = self.getparams(request)
        a =params.get('a',5)
        b =params.get('b',10)
        c = int(a)+int(b)
        return str(c)

    def allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def upload_file(self):
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                # flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                # flash('No selected file')
                return redirect(request.url)
            if file and self.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(self.app.config['UPLOAD_FOLDER'], filename))
                return redirect(url_for('uploaded_file',
                                        filename=filename))
        return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
          <p><input type=file name=file>
             <input type=submit value=Upload>
        </form>
        '''

    # @app.route("/upload", methods=["POST"])
    def upload(self):
        print "inside upload....!.!"
        folder_name = str(uuid.uuid4())#request.form['superhero']
        '''
        # this is to verify that folder to upload to exists.
        if os.path.isdir(os.path.join(APP_ROOT, 'files/{}'.format(folder_name))):
            print("folder exist")
        '''
        target = os.path.join(self.DATA_PATH, '{}'.format(folder_name))
        print(target)
        if not os.path.isdir(target):
            os.mkdir(target)
            target = os.path.join(target, '{}'.format("Encrypt"))
            os.mkdir(target)
        print(request.files.getlist("file"))
        for upload in request.files.getlist("file"):
            print(upload)
            print("{} is the file name".format(upload.filename))
            filename = upload.filename
            # This is to verify files are supported
            ext = os.path.splitext(filename)[1]
            if (ext == ".jpg") or (ext == ".txt"):
                print("File supported moving on...")
            else:
                render_template("Error.html", message="Files uploaded are not supported...")
            destination = "/".join([target, filename])
            print("Accept incoming file:", filename)
            print("Save it to:", destination)
            upload.save(destination)
            stats = self.encode_file(target, filename, folder_name, ext)
        # return send_file(target+'/output.bin', as_attachment=True)
        # return send_from_directory("images", filename, as_attachment=True)#json.dumps(temp)
        return render_template("upload_success.html", uuid=folder_name, download_path=target+'/output.bin', file_size=stats["file_size"], word_cloud_data = json.dumps(stats["word_cloud_data"]))

    def encode_file(self, folder_path, input_file_name, uuid, ext):
        pass
        if ext == ".txt":
            type="word"
        else:
            type="image"
        input_file_path = "/".join([folder_path, input_file_name])
        # pdb.set_trace()
        stats = huffman_text.start(input_file_path, output_path=folder_path+"/",filename="output", run_type = type, mode = "encrypt", uuid=uuid, folder_path=self.DATA_PATH)
        return stats

    def decrypt_file(self, path="",filename="",uuid="",data_path=""):
        return huffman_text.start(path, output_path="", filename=filename, run_type="word", mode="decrypt",uuid=uuid,data_path=data_path)

    def download(filename):
        try:
            filename =  request.args['filename']
            return send_file(filename, as_attachment=True)
        except Exception as e:
            return render_template("error.html")

    def decrypt_page(self):
        return render_template("decrypt.html")

    def word_cloud(message):
        import json
        d= {'data': [{"text":"study","size":40},{"text":"motion","size":15},{"text":"forces1","size":10}] }
        # _temp = json.dumps({"text":"study","size":40})
        message = request.args['message']
        message = json.loads(message)
        return render_template("word_cloud.html", message= message)



    def upload_decrypt(self):
        print "inside upload....!.!"
        folder_name = request.form['uuid']#str(uuid.uuid4())#request.form['superhero']
        print folder_name
        '''
        # this is to verify that folder to upload to exists.
        if os.path.isdir(os.path.join(APP_ROOT, 'files/{}'.format(folder_name))):
            print("folder exist")
        '''
        target = os.path.join(self.DATA_PATH, '{}'.format(folder_name))
        if folder_name == "":
            return render_template("Error.html", message="Encrypted file not found, please check UUID")
        print(target)
        if os.path.isdir(target):
            target = os.path.join(target, '{}'.format("Decrypt"))
            if not os.path.isdir(target):
                os.mkdir(target)
        else:
            return render_template("Error.html", message="Encrypted file not found, please check UUID")
        print(request.files.getlist("file"))
        for upload in request.files.getlist("file"):
            print(upload)
            print("{} is the file name".format(upload.filename))
            filename = upload.filename
            # This is to verify files are supported
            ext = os.path.splitext(filename)[1]
            if (ext == ".bin"):
                print("File supported moving on...")
            else:
                render_template("Error.html", message="Files uploaded are not supported...")
            destination = "/".join([target, filename])
            print("Accept incoming file:", filename)
            print("Save it to:", destination)
            upload.save(destination)
        path = self.decrypt_file(path= os.path.join(self.DATA_PATH, '{}'.format(folder_name)),filename=filename, uuid=folder_name, data_path=self.DATA_PATH)

        import json
        temp = {'data': [{"text":"study","size":40},{"text":"motion","size":15},{"text":"forces","size":100}] }
        temp = json.dumps(temp)
        return render_template("decrypt_success.html", uuid=folder_name, download_path=path, message=temp)