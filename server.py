import os, sys, flask
from flask import render_template, send_file
base_path = os.path.dirname(__file__)
class_path = os.path.join(base_path, "classes")
data_path = os.path.join(base_path, "data")
config_path = os.path.join(base_path, "config/")
sys.path.insert(0, base_path)
sys.path.insert(1, class_path)
sys.path.insert(2, data_path)

WSGI_PATH_PREFIX = ''
from flask import redirect, url_for
import basicServer_services as services
class Config():
    def __init__(self,app,WSGI_PATH_PREFIX):
        self.app = app
        # register managers and then services
        print'----------------------------------------------------------------------------'
        print '                   WSGIPrefix set to %s'%WSGI_PATH_PREFIX
        self.srvs = services.register_services(app, WSGI_PATH_PREFIX)

# create application
application = flask.Flask(__name__, static_url_path='/static')
application.config['CONFIG_PATH'] = config_path
application.config['DATA_PATH'] = data_path

cfg = None


@application.route(WSGI_PATH_PREFIX + '/basicServer')
def index():
    print 'comming here'
    return render_template("index.html")
    # return "<b>hello</b>"

def set_wsgi_prefix(prefix='/'):
    print 'comming in setWsgi'
    WSGI_PATH_PREFIX = prefix
    cfg = Config(application, WSGI_PATH_PREFIX)

@application.route(WSGI_PATH_PREFIX + '/')
def root():
    print 'comming in root'
    return render_template("index.html", title='Projects')
    # return redirect(url_for('index'))


if __name__ == '__main__':
    WSGI_PATH_PREFIX = '/basicServer'
    cfg = Config(application, WSGI_PATH_PREFIX)
    dport = int(sys.argv[1]) if len(sys.argv) > 1 else 5050
    application.run(host='0.0.0.0',port=dport,debug=True,use_reloader=True,processes=100,static_files={'/':'static'})
else:
    cfg = Config(application, WSGI_PATH_PREFIX)