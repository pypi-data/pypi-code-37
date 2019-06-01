class count:
	def __init__(self,f):
		self.count = 0
		self.f = f
	def __call__(self,*args):
		self.count += 1
		return self.f(*args)
	def howmany(self):
		return self.count
