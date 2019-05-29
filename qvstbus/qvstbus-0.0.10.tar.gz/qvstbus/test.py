import __init__ as qvstbus
ip = '127.0.0.1'
def test(p):
	return 'hello {}'.format(p['name'])
def result(x):
	print(x)
def fa(a):		
	a.on('test a', test)
	a.call(to='a', method='test a', params={'name': 'a'}, callback=result)

qvstbus.register(ip=ip, name='a', callback=fa)
input()