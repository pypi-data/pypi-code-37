import websocket
import json
import time
import random
try:
	import _thread as thread
except:
	import thread
class QvstBus:		
	@staticmethod
	def register(ip, name, callback=None, port=2019):
		obj = QvstBus()	
		def startConnection(obj):
			needsReboot = False
			obj.ws = websocket.WebSocketApp('ws://{0}:{1}'.format(ip, port))							
			thread.start_new_thread(obj.ws.run_forever,())			
			obj.ip = ip
			obj.name = name		
			obj.requestMap = {}
			obj.methodMap = {}			
			def on_bin_open(ws):				
				ws.send(json.dumps({'name': obj.name, 'type': 'binary'}))
				ws.on_message = on_bin_message	
			def on_bin_message(ws, msg):
				if (msg != 'ok'):
					print(msg)
					return
				print('bin websocket connected')
				obj.ws.on_message = on_receive
				if (callback is not None):
					callback(obj)

			def on_open(ws):				
				ws.send(json.dumps({'name': obj.name}))	

			def on_message(ws, msg):								
				if (msg != 'ok'):
					print(msg)
					return		
				print('websocket connected')		
				obj.wsBin = websocket.WebSocketApp('ws://{0}:{1}'.format(ip, port))	
				thread.start_new_thread(obj.wsBin.run_forever, ())
				obj.wsBin.on_open = on_bin_open

					
			def help(stupid_arg):
				return list(filter(lambda x: x is not 'help', obj.methodMap.keys()))		
			def on_close(ws):
				print('websocket closed')							
				if (needsReboot):
					startConnection(obj)
			def on_error(ws, err):
				if (str(err).find('Connection timed out') != -1):
					ws.close()
					needsReboot = True
				else:
					raise Exception('websocket connection error {}'.format(err))		
			def on_receive(ws, msg):
				msg = json.loads(msg)			
				data = msg['data']
								
				if ('method' in data):
					error = None
					result = None
					try:
						result = obj.methodMap.get(data['method'])(data['params'])
					except Exception as e:
						error = 'method execution error: {}'.format(str(e))
					obj._response(msg['from'], data['id'], result, error)
				else:
					if (data['error'] is not None):
						obj._log('request error: {}'.format(data['error']))
					else:
						try:
							obj.requestMap.get(data['id'])(data['result'])
							del obj.requestMap[data['id']]
						except Exception:
							obj._log('response error')	
			obj.ws.on_open = on_open
			obj.ws.on_message = on_message
			obj.ws.on_error = on_error		
			obj.ws.on_close = on_close
			obj.on('help', help)	
		startConnection(obj)
		
				

	def on(self, methodName, callback):
		self.methodMap[methodName] = callback

	def call(self, to, method, params, callback):
		id = self._uuid()
		msg = {
			'from': self.name,
			'to': to,
			'data': {
				'id': id,
				'method': method,
				'params': params
			}
		}
		self.requestMap[id] = callback
		self._send(msg)

	def _log(self, msg):
		print(msg)

	def _send(self, msg):		
		msg = json.dumps(msg)
		self.ws.send(msg)

	def _uuid(self):
		return '{0}{1}'.format(round(time.time() * 1000), str(random.random())[2:])

	def _response(self, to, id, result, error):
		msg = {
			'from': self.name,
			'to': to,
			'data': {
				'id': id,
				'result': result,
				'error': error
			}
		}
		self._send(msg)		
register = QvstBus.register
