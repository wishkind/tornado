import json
import math

from playhouse.shortcuts import model_to_dict
from blog.handler import RedisHandler
from apps.utils.utils import json_serial
from apps.utils.re_data_params import resSuccess

from apps.models.article_models import ArticleModel
from apps.models.tag_models import TagModel


class TagHandler(RedisHandler):
    async def get(self, *args, **kwargs):
        """获取标签列表"""
        try:
            tags = await self.application.objects.execute(TagModel.select())

            re_list = []
            for tag in tags:
                tag_dict = model_to_dict(tag)
                tag_dict['ta_count'] = await self.application.objects.count(
                    ArticleModel.select().where(ArticleModel.state == 1, ArticleModel.tag.contains(tag_dict['name']))
                )
                re_list.append(tag_dict)

            re_data = resSuccess('成功')

            re_data['result'] = {
                'list': re_list,
                'pagination': {
                    'current_page': 1,
                    'page_size': 10,
                    'total': len(re_list),
                    'total_count': math.ceil(len(re_list) / 10)
                }
            }

        except TagModel.DoesNotExist:
            self.set_status(400)
            re_data = resSuccess('失败')

        self.finish(json.dumps(re_data, default=json_serial))

