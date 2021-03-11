import shenjian


user_key = '3ac5cd07fc-MTY0Nzk5ND'
user_secret = 'IzYWM1Y2QwN2ZjZj-f20ae0565f16479'
app_id = '2977480'


crawler = shenjian.Crawler(user_key, user_secret, app_id)
crawler.config_proxy(shenjian.proxy_type.PROXY_TYPE_BETTER)

params = {}
# params["crawlerStore"] = True
# params["pageNum"] = 10
# params["productUrl"] = "https://item.jd.com/3724805.html"
# params["keywords"] = ["男装","女装"]

# crawler.config_custom(params)

result1 = crawler.start(1)
result2 = crawler.get_status()

result3 = crawler.pause()

params['verifyCode'] = '123456'
result4 = crawler.config_custom(params)

result5 = crawler.resume()

print(result1)
print(result2)
print(result3)
print(result4)
print(result5)

result6 = crawler.get_status()
print(result6)
