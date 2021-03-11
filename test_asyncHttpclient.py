from tornado.httpclient import AsyncHTTPClient

async def visit_baidu() :

	client = AsyncHTTPClient()
	
	response =  await client.fetch("http://www.baidu.com")
	
	# 异步获取结果 
	print(response.body.decode())


from tornado import gen

@gen.coroutine
def visit_baidu1() :

	client = AsyncHTTPClient()
	response =  yield client.fetch("http://www.baidu.com")
	# 异步获取结果 
	print(response.body.decode())


from tornado.ioloop import IOLoop

if __name__ == "__main__" :

	IOLoop.current().run_sync(visit_baidu)
