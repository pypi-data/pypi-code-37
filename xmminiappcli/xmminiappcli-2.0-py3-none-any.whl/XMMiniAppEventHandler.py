from watchdog.events import RegexMatchingEventHandler, FileSystemEvent
from .Notification import NotificationCenter, Notification

class XMMiniAppEventHandler(RegexMatchingEventHandler): 

    APP_JSON_REGEX = [r".+?/app\.json$"]

    def __init__(self):
        super().__init__(self.APP_JSON_REGEX)

    # def on_created(self, event):
    #     self.process(event)
    
    def on_modified(self, event):
        self.process(event)
    
    def on_deleted(self, event):
        self.process(event)

    def process(self, event):
        # event.event_type 
        src_path = event.src_path
        if "app.json" not in src_path:
            return
        
        notification = Notification("App_Json_Change_Notification")
        NotificationCenter().post_notification(notification) 