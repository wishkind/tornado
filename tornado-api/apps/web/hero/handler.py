import json
import math

from playhouse.shortcuts import model_to_dict

from apps.models.hero_models import HeroModels, HeroInfoModels

from apps.utils.re_data_params import resSuccess
from apps.utils.utils import get_ip_info, json_serial

from blog.settings import settings
from blog.handler import RedisHandler


class AddHeroHandler(RedisHandler):
    async def put(self, *args, **kwargs):
        """添加留言"""
        params = json.loads(self.request.body.decode('utf-8'))

        try:
            headers = self.request.headers
            hero_data = params['author']
            ip_info = get_ip_info('58.101.33.178' if self.request.remote_ip == '127.0.0.1' else self.request.remote_ip)

            hero_info = await self.application.objects.create(
                HeroInfoModels, portrait=hero_data['portrait'], email=hero_data['email'],
                name=hero_data['name'], site=hero_data['site'], ip=self.request.remote_ip,
                agent=headers.get('User-Agent', ''), city=ip_info['city'], country=ip_info['country'],
                province=ip_info['province'], lin_lat=ip_info['lin_lat'],
            )

            await self.application.objects.create(
                HeroModels, hero_info=hero_info.id, content=params['content']
            )

            re_data = resSuccess('成功')

        except HeroModels.DoesNotExist as e:
            self.set_status(400)
            re_data = resSuccess('失败')
        except HeroInfoModels.DoesNotExist as e:
            self.set_status(400)
            re_data = resSuccess('失败')
        self.finish(re_data)


class HeroHandler(RedisHandler):
    async def get(self, *args, **kwargs):
        """获取留言列表"""
        current_page = int(self.get_argument('current_page', 1))
        hero_list = []

        try:
            hero = HeroModels.extends()
            hero_items = await self.application.objects.execute(
                hero.paginate(current_page, int(settings['page_size']))
            )
            for item in hero_items:
                hero_dict = model_to_dict(item)
                hero_list.append(hero_dict)

            hero_count = await self.application.objects.count(hero)

            re_data = resSuccess('成功')
            re_data['result'] = {
                'list': hero_list,
                'pagination': {
                    'current_page': current_page,
                    'page_size': 10,
                    'total': hero_count,
                    'total_page': math.ceil(hero_count / 10)
                }
            }

        except HeroModels.DoesNotExist as e:
            self.set_status(400)
            re_data = resSuccess('失败')
        self.finish(json.dumps(re_data, default=json_serial))
