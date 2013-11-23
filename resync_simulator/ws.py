import logging
from tornado.web import Application
from tornado.websocket import WebSocketHandler

class WSInterface(Application):
    def __init__(self,source,port=8889):    
        """Initializes WS interface with default settings and handlers"""
        self.logger = logging.getLogger('ws')
        self.logger.info("Setting up WS server on port %d" % (port))
        #self.source = source
        #ChangeNotificationHandler.source=self.source
        ChangeNotificationHandler.logger=self.logger
        #ChangeNotificationHandler.changememory = self.source.changememory
        handlers = [(r"/changenotification", ChangeNotificationHandler)]
        Application.__init__(self, handlers, {})
        self.listen(port)

class ChangeNotificationHandler(WebSocketHandler):

    # How do we set this data up as instance vars rather than class vars?
    # with web app for tornado one specified a dict in the handler setting...
    destinations = set()
    #source = None
    #changememory = None
    logger = None

    def open(self):
        ChangeNotificationHandler.destinations.add(self)
        ChangeNotificationHandler.logger.info("Connection opened")

    def on_message(self, message):
        """We don't take messages, just dump them on the floor"""
        ChangeNotificationHandler.logger.info("Incoming message ignored")

    def on_close(self):
        ChangeNotificationHandler.destinations.remove(self)
        ChangeNotificationHandler.logger.info("Connection closed")

    #@classmethod
    #def generate_change_list(cls):
    #    """Serialize the changes in the changememory"""
    #    change_list = cls.changememory.generate()
    #    change_list.describedby = cls.source.describedby_uri
    #    change_list.up = cls.source.capability_list_uri
    #    change_list.md_from = change_list.resources[0].timestamp
    #    change_list.md_until = 'now'
    #    return change_list.as_xml()

    @classmethod
    def send_updates(cls, msg, num=0, frm=None):
        cls.logger.info("Sending %d updates for %d destinations" % (num,len(cls.destinations)))
        for dest in cls.destinations:
            if dest != frm:
                try:
                    dest.write_message(msg)
                except:
                    pass # logging goes here
