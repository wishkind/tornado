try:
    import cPickle as pickle
except:
    import pickle
import tornado.gen
import tornado.tcpclient
import time

class Message(object):
    def __init__(self, address, port, timeout=120):
        self._client = tornado.tcpclient.TCPClient()
        self.watches = set()
        self.address = address
        self.port = port
        self.timeout = timeout



    def add_client(self, user_id, socket):
        self.watches.add((uid, socket))
    
	
    def close(self, socket):
        logging.info('watches remove: %s' % socket.pid)
        for i in filter(lambda x:x[2]==socket, self.watches):
            self.watches.remove(i)
			
	
    @tornado.gen.coroutine
    def listen(self):
        try:
            logging.info('notify server: connect...')
            self.stream = yield self._client.connect(self.address, self.port)
        except:
            logging.warning('notify server: connect failed')
            self.connected = False
            tornado.ioloop.IOLoop.instance().add_timeout(time.time()+self.timeout, self.listen)

        else:
            data = yield self.stream.read_until('\r\n')
            message, operator_ids = pickle.loads(data)
            self.new_messages(message,operator_ids)


    def new_messages(self, message, operator_ids=None):
        # 发送到所有客户端
        logging.info("Sending new message to %r listeners", len(self.watches))
        for uid, socket in self.waiters:
            if  (operator_ids and uid in operator_ids):
                try:
                    socket.write_message(message)
                except:
                    logging.error("Error in watches callback", exc_info=True)
					
