from videotosmi import Video
from ConfigHelper import Config
from deepgeo import Utils
import http.server as BaseHTTPServer
import shutil
import cgi

class ServerConfig:
    IP = "127.0.0.1"
    PORT = 80
    MODEL_NAME = "mscoco"
    MODEL_CONFIG_PATH = ""
    MODEL_ENGINE = "maskrcnn"
    FRAME_SET = 60
    ROTATION= -90
    FILTER = []
    IS_RANDOM_NAME = True
    VIDEO_FOLDER = ""
    def toFile(self, path):
        config = Config(self)
        config.toFile(path)

    def fromFile(self, path):
        config = Config(path)
        config.setObject(self)

def save_file(obj, image_path, filename):
    
    file = obj.file.read()
    open(image_path + "/%s" % filename, "wb").write(file)
    return image_path+filename

class Server:
    def __init__(self, config:ServerConfig):
        self.config = config
        self.server = self._init_Server_()
    
    def _init_Server_(self):
        CONFIG = self.config
        class __(BaseHTTPServer.BaseHTTPRequestHandler):
            def __init__(self, *args):
                self.video = Video()
                self.config = CONFIG
                self.video.add_model(self.config.MODEL_NAME,self.config.MODEL_ENGINE,self.config.MODEL_CONFIG_PATH)
                self.config.VIDEO_FOLDER = Utils.create_folder(self.config.VIDEO_FOLDER)
                BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, *args)
            
            def write_file(self, file_path):
                with open(file_path, 'rb') as content:
                    shutil.copyfileobj(content, self.wfile)
                
            def write_data(self, data):
                try:
                    self.wfile.write(data)
                except Exception as e:
                    print(e, " Fixed: change UTF-8")
                    self.wfile.write(bytes(data, "utf-8"))
            def do_GET(self):
                url = str(self.path).split("/")[-1]
                ext = url.split(".")[-1]
                if len(url) <= 4 or ext!="smi":
                    self.send_response(404)
                    self.end_headers()
                else:
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Content-type', 'application/text; charset=utf-8')
                    self.end_headers()
                    self.write_file(self.config.VIDEO_FOLDER+url)

            def do_POST(self):
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST',
                            'CONTENT_TYPE': self.headers['Content-Type'],
                            })
                key = list(form.keys())[0]
                obj = form[key]
                filename = str(obj).split("FieldStorage('"+key+"', '")[1].split("', ")[0]
                if self.config.IS_RANDOM_NAME:
                    filename= Utils.create_name(filename.split(".")[-1],self.config.VIDEO_FOLDER)
                
                img_names = save_file(obj,image_path=self.config.VIDEO_FOLDER, filename=filename)
                self.video.detect(img_names,self.config.MODEL_NAME, frame_set=self.config.FRAME_SET, rotation=self.config.ROTATION, ftr=self.config.FILTER)
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                file_name = img_names.split(".")[0].split("/")[-1]+".smi"
                
                self.write_data(file_name)
        return __

    def Run(self):
        s = BaseHTTPServer.HTTPServer((self.config.IP, self.config.PORT), self.server)
        print("{}:{} ... 대기".format(str(self.config.IP), str(self.config.PORT)))
        s.serve_forever()