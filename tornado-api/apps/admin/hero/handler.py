import json
import math

from playhouse.shortcuts import model_to_dict

from apps.utils.decorators import authenticated_async
from blog.handler import RedisHandler

from apps.models.hero_models import HeroModels

from apps.utils.re_data_params import resSuccess
from apps.utils.utils import json_serial

from blog.settings import settings


class DelHeroHandler(RedisHandler):
    @authenticated_async
    async def delete(self, hero_uuid, *args, **kwargs):
        """删除留言板"""
        try:
            hero = await self.application.objects.get(HeroModels, uuid=hero_uuid)
            hero.state = 100
            await self.application.objects.update(hero)

            re_data = resSuccess('成功')

        except HeroModels.DoesNotExist as e:
            self.set_status(400)
            re_data = resSuccess('失败')

        self.finish(re_data)


class FilterHandler(RedisHandler):
    @authenticated_async
    async def get(self, *args, **kwargs):
        """条件筛选"""
        state = int(self.get_argument('state', 0))
        current_page = self.get_argument('current_page', 1)

        try:
            is_state = False
            hero = HeroModels.extends()

            if state == 102:
                state = 0
                is_state = True

            elif state == 103:
                state = 1
                is_state = True

            elif state == 104:
                state = 2
                is_state = True

            if is_state:
                hero = hero.where(HeroModels.state == state)

            hero_count = await self.application.objects.count(hero)
            hero_items = await self.application.objects.execute(
                hero.paginate(int(current_page), int(settings['page_size']))
            )

            hero_list = []
            for item in hero_items:
                hero_dict = model_to_dict(item)
                hero_list.append(hero_dict)

            re_data = resSuccess('成功')
            re_data['result'] = {
                'data': hero_list,
                'pagination': {
                    'current_page': current_page,
                    'page_size': int(settings['page_size']),
                    'total': hero_count,
                    'total_size': math.ceil(hero_count / int(settings['page_size']))
                }
            }

        except HeroModels.DoesNotExist:
            self.set_status(400)
            re_data = resSuccess('失败')

        self.finish(json.dumps(re_data, default=json_serial))


class EditAllHandler(RedisHandler):
    @authenticated_async
    async def post(self, *args, **kwargs):
        """批量修改   100:  删除  200:  通过 300:  不通过"""
        re_data = {}
        params = json.loads(self.request.body.decode('utf-8'))
        hero_uuid = params.get('hero_uuid', None)
        state = int(params.get('state', 0))

        if hero_uuid:
            for uuid in hero_uuid:
                try:
                    hero = await self.application.objects.get(
                        HeroModels.extends().where(HeroModels.uuid == uuid)
                    )

                    if state == 200:
                        hero.state = 1

                    elif state == 300:
                        hero.state = 2

                    elif state == 100:
                        hero.state = 100

                    await self.application.objects.update(hero)
                    re_data = resSuccess('成功')

                except HeroModels.DoesNotExist:
                    self.set_status(400)
                    re_data = resSuccess('失败')
        else:
            self.set_status(400)
            re_data = resSuccess('失败')

        self.finish(re_data)


class EditHeroHandler(RedisHandler):
    @authenticated_async
    async def post(self, hero_uuid, *args, **kwargs):
        """编辑留言板"""
        params = json.loads(self.request.body.decode('utf-8'))
        state = params.get('state', None)
        content = params.get('content', None)
        try:
            hero = await self.application.objects.get(
                HeroModels.extends().where(HeroModels.uuid == hero_uuid)
            )
            if content:
                hero.content = content

            if state or state == 0 or state == '0':
                hero.state = int(state)

            await self.application.objects.update(hero)

            re_data = resSuccess('成功')

        except HeroModels.DoesNotExist:
            self.set_status(400)
            re_data = resSuccess('失败')

        self.finish(re_data)


class GetHeroHandler(RedisHandler):
    @authenticated_async
    async def get(self, *args, **kwargs):
        """获取留言列表"""
        current_page = self.get_argument('current_page', 1)

        try:
            hero = HeroModels.extends()

            hero_items = await self.application.objects.execute(
                hero
                    .filter(HeroModels.state != 100)
                    .paginate(int(current_page), int(settings['page_size']))
            )

            hero_count = await self.application.objects.count(hero.filter(HeroModels.state != 100))

            hero_list = []
            for item in hero_items:
                hero_dict = model_to_dict(item)
                hero_list.append(hero_dict)

            re_data = resSuccess('成功')
            re_data['result'] = {
                'data': hero_list,
                'pagination': {
                    'current_page': current_page,
                    'page_size': int(settings['page_size']),
                    'total': hero_count,
                    'total_page': math.ceil(hero_count / int(settings['page_size']))
                }
            }

        except HeroModels.DoesNotExist as e:
            self.set_status(400)
            re_data = resSuccess('失败')

        self.finish(json.dumps(re_data, default=json_serial))


# ---------------------华丽的分割线---------------------


class GetHeroRHandler(RedisHandler):
    @authenticated_async
    async def get(self, *args, **kwargs):
        """获取已删除留言"""
        current_page = int(self.get_argument('current_page', 1))
        try:
            heroR = HeroModels.extends()
            heroR = heroR.filter(HeroModels.state == 100)

            heroR_items = await self.application.objects.execute(
                heroR.paginate(current_page, int(settings['page_size']))
            )

            heroR_count = await self.application.objects.count(heroR)

            heroR_list = []
            for item in heroR_items:
                heroR_dict = model_to_dict(item)
                heroR_list.append(heroR_dict)

            re_data = resSuccess('成功')
            re_data['result'] = {
                'data': heroR_list,
                'pagination': {
                    'current_page': current_page,
                    'page_size': int(settings['page_size']),
                    'total': heroR_count,
                    'total_page': math.ceil(heroR_count / int(settings['page_size']))
                }
            }

        except HeroModels.DoesNotExist as e:
            self.set_status(400)
            re_data = resSuccess('失败')

        self.finish(json.dumps(re_data, default=json_serial))


class EditHeroRHandler(RedisHandler):
    @authenticated_async
    async def post(self, heroR_uuid, *args, **kwargs):
        """编辑 已删除留言"""
        params = json.loads(self.request.body.decode('utf-8'))
        state = params.get('state', None)
        content = params.get('content', None)

        try:
            heroR = HeroModels.extends()
            heroR = await self.application.objects.get(
                heroR.where(HeroModels.uuid == heroR_uuid)
            )
            if content:
                heroR.content = content

            if state or state == 0 or state == '0':
                heroR.state = int(state)

            await self.application.objects.update(heroR)

            re_data = resSuccess('成功')

        except HeroModels.DoesNotExist:
            self.set_status(400)
            re_data = resSuccess('失败')

        self.finish(re_data)


class EditAllHeroRHandler(RedisHandler):
    @authenticated_async
    async def post(self, *args, **kwargs):
        """批量编辑已删除留言"""
        re_data = {}
        params = json.loads(self.request.body.decode('utf-8'))

        hero_uuid = params.get('hero_uuid', None)
        state = int(params.get('state', 0))

        if hero_uuid:
            for uuid in hero_uuid:
                try:
                    hero = await self.application.objects.get(
                        HeroModels.extends().where(HeroModels.uuid == uuid)
                    )
                    if state == 100:
                        await self.application.objects.delete(hero)

                    elif state == 200:
                        hero.state = 0

                    elif state == 300:
                        hero.state = 1

                    elif state == 400:
                        hero.state = 2

                    await self.application.objects.update(hero)
                    re_data = resSuccess('成功')

                except HeroModels.DoesNotExist:
                    self.set_status(400)
                    re_data = resSuccess('失败')
        else:
            self.set_status(400)
            re_data = resSuccess('失败')

        self.finish(re_data)


class DelHeroRHandler(RedisHandler):
    @authenticated_async
    async def delete(self, heroR_uuid, *args, **kwargs):
        """彻底删除  留言"""
        try:
            hero = await self.application.objects.get(HeroModels, uuid=heroR_uuid)
            await self.application.objects.delete(hero)

            re_data = resSuccess('成功')

        except HeroModels.DoesNotExist as e:
            self.set_status(400)
            re_data = resSuccess('失败')

        self.finish(re_data)
