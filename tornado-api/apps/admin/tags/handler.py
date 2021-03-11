import json

from playhouse.shortcuts import model_to_dict

from apps.utils.decorators import authenticated_async
from apps.utils.utils import json_serial
from apps.utils.re_data_params import resSuccess
from apps.models.tag_models import TagModel
from apps.models.article_models import ArticleModel

from blog.handler import RedisHandler


class TagHandler(RedisHandler):
    @authenticated_async
    async def put(self, *args, **kwargs):
        """添加标签"""
        params = json.loads(self.request.body.decode('utf-8'))
        try:
            await self.application.objects.create(TagModel, name=params['name'], desc=params['desc'])
            re_data = resSuccess('成功')
        except TagModel.DoesNotExist as e:
            self.set_status(400)
            re_data = resSuccess('失败')

        self.finish(re_data)

    @authenticated_async
    async def get(self, *args, **kwargs):
        """获取标签"""
        re_list = []
        try:
            tags = await self.application.objects.execute(TagModel.select().order_by(TagModel.update_time.desc()))

            for tag in tags:
                tag_dict = model_to_dict(tag)
                tag_count = await self.application.objects.count(ArticleModel.select().where(ArticleModel.tag==tag_dict['name']))
                tag_dict['count'] = tag_count
                re_list.append(tag_dict)

            re_data = resSuccess('成功')
            re_data['result'] = {
                'list': re_list,
                'pagination': {
                    'current_page': 1,
                    'page_size': 50,
                    'total': len(re_list)
                }
            }
        except TagModel.DoesNotExist as e:
            self.set_status(400)
            re_data = resSuccess('失败')
        self.finish(json.dumps(re_data, default=json_serial))

    @authenticated_async
    async def post(self, *args, **kwargs):
        """修改标签"""
        params = json.loads(self.request.body.decode('utf8'))
        try:
            tags = await self.application.objects.get(TagModel, uuid=params['uuid'])
            tags.name = params['name']
            tags.desc = params['desc']
            await self.application.objects.update(tags)

            re_data = resSuccess('成功')

        except TagModel.DoesNotExist as e:
            self.set_status(400)
            re_data = resSuccess('失败')
        self.finish(json.dumps(re_data, default=json_serial))

    @authenticated_async
    async def delete(self, *args, **kwargs):
        """删除标签"""
        param = self.request.arguments
        try:
            await self.application.objects.execute(TagModel.delete().where(TagModel.uuid==param['uuid'][0].decode('utf-8')))
            re_data = resSuccess('成功')
        except TagModel.DoesNotExist as e:
            self.set_status(400)
            re_data = resSuccess('失败')

        self.finish(re_data)
