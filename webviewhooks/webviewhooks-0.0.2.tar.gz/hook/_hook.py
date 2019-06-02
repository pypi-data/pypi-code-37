import sys
import frida
import time
from hook import prepare

code = """
setImmediate(
    function() {
            Java.perform(function() {
            console.log('hook prepare');
            var valueCallback;
            var runnable;
            var threadInstance;
            var clazz = Java.use('java.lang.Class');
            var thread = Java.use('java.lang.Thread');
            var runnableClass = Java.use('java.lang.Runnable');
            var webView = Java.use('android.webkit.WebView');
            var handler = Java.use('android.os.Handler');
            var handlerInstance = handler.$new();
            
            webView.setWebViewClient.overload('android.webkit.WebViewClient').implementation = function(view) {
                console.log('start hook setWebViewClient');
                var webViewClassName = view.getClass().toString();
                console.log(webViewClassName);
                var realWebViewClassName = webViewClassName.split(' ')[1];
                var array = realWebViewClassName.split('.');
                array = array.slice(0, array.length - 1);
                var classNamePrefix = array.join('.');
                console.log(classNamePrefix);
                var fakeClient = Java.use(classNamePrefix + '.WebViewClient');
                var valueCallbackClass = Java.use(classNamePrefix + '.ValueCallback');
                valueCallback = Java.registerClass({
                    name: 'looper.valueCallback',
                    implements: [valueCallbackClass],
                    methods: {
                        onReceiveValue: function(value) {
                            send(value.toString());
                            return value;
                        }
                    }
                });
                fakeClient.onPageFinished.overload(classNamePrefix + '.WebView', 'java.lang.String').implementation =
                 function(view, url) {
                    console.log('start hook onPageFinished');
                    handler.handleMessage.overload('android.os.Message').implementation = function(msg) {
                        console.log('start hook handleMessage');
                        var what = Java.cast(msg.getClass(), clazz).getDeclaredField('what').get(msg);
                        if(what == 10010) {
                            console.log('get web page html dom tree')
                            view.evaluateJavascript("javascript:document.getElementsByTagName('html')[0].innerHTML", valueCallback.$new());
                        }
                        return this.handleMessage(msg);
                    }
                    runnable = Java.registerClass({
                        name: 'looper.runnableClass',
                        implements: [runnableClass],
                        methods: {
                            run: function() {
                                    console.log('sub thread start run');
                                    threadInstance.sleep(2000);
                                    console.log('2s sleep end! start send message')
                                    handlerInstance.sendEmptyMessage(10010);
                                }
                        }
                    });
                    threadInstance = thread.$new(runnable.$new());
                    threadInstance.start();
                 }
                 this.setWebViewClient(view);
            }
        });
    }
);
"""


class HookError:
    def __init__(self, msg):
        self.arg = msg


class WebViewHook:
    device = None
    session = None
    pid = None

    def __init__(self, package_name, device_id, callback, adb_name='adb'):
        self.package_name = package_name
        self.device_id = device_id
        self.adb_name = adb_name
        self.callback = callback

    @staticmethod
    def get_device_by_id(did):
        phone = None
        try:
            phone = frida.get_device(did, 5)
        finally:
            return phone

    def on_message(self, message, data):
        type = message["type"]
        msg = message
        if type == "send":
            msg = message["payload"]
        elif type == 'error':
            msg = message['stack']
        else:
            msg = message
        print(msg)
        self.callback(msg)

    @staticmethod
    def start_app_and_inject_code(pkg):
        WebViewHook.pid = WebViewHook.device.spawn([pkg])
        print('{} pid: {}'.format(pkg, WebViewHook.pid))
        print('start app success')
        time.sleep(1)
        print('start attach target')
        WebViewHook.session = WebViewHook.device.attach(pkg)
        print('attach success')
        script = WebViewHook.session.create_script(code)
        script.on('message', WebViewHook.on_message)
        print('start inject script code')
        script.load()

    def hook(self):
        pkg = self.package_name
        did = self.device_id
        print('packageName: {} and deviceId: {}'.format(pkg, did))
        if type(pkg) != str or type(did) != str:
            raise HookError('packageName or deviceId field type must be string!')
        if not prepare.start_check(self.adb_name):
            raise RuntimeError('check env is error, please prepare the env is fine')
        print('start get device instance')
        WebViewHook.device = WebViewHook.get_device_by_id(did)
        if WebViewHook.device is None:
            raise HookError('get device is None')
        print('get device success')
        print('start app and inject')
        self.start_app_and_inject_code(pkg)
        sys.stdin.read()

    def clear(self):
        if WebViewHook.session is None:
            raise HookError('you should call hook function first')
        webviewhook.session.detach()
        webviewhook.device.kill(self.package_name)


if __name__ == '__main__':
    webviewhook = WebViewHook('com.hsw.zhangshangxian', '127.0.0.1:62001')
    webviewhook.hook()
