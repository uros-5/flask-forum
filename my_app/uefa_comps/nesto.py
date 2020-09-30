class A(object):
	nesto1 = ""
	nesto2 = ""

	def print_dict(self):
		recnik = {k: v for k, v in self.__class__.__dict__.items() if not k.startswith('__') and "_" not in k}
		print(recnik)

a = A()
a.print_dict()