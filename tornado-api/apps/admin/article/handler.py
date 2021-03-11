import json
import math

from playhouse.shortcuts import model_to_dict

from apps.utils.decorators import authenticated_async
from apps.utils.utils import json_serial
from apps.utils.re_data_params import resSuccess

from blog.handler import RedisHandler
from blog.settings import settings
from apps.models.article_models import ArticleModel
from apps.models.tag_models import TagModel


# 文章状态说明
# 1 == 正常发布   2 == 草稿箱  200 == 已删除


class AllArticleRHandler(RedisHandler):
    @authenticated_async
    async def post(self, *args, **kwargs):
        """批量操作已删除文章"""
        re_data = {}

        params = json.loads(self.request.body.decode('utf-8'))
        state = int(params.get('state', 0))
        article_uuid = params.get('article_uuid', [])

        if article_uuid:
            for uuid in article_uuid:
                try:
                    article = await self.application.objects.get(
                        ArticleModel, uuid=uuid, state=200
                    )

                    if state == 100:
                        article.state = 2
                        await self.application.objects.update(article)

                    elif state == 200:
                        await self.application.objects.delete(article)

                    re_data = resSuccess('成功')

                except ArticleModel.DoesNotExist as e:
                    self.set_status(400)
                    re_data = resSuccess('失败')
        else:
            re_data = resSuccess('失败')

        self.finish(re_data)


class EditArticleRHandler(RedisHandler):
    @authenticated_async
    async def post(self, article_uuid, *args, **kwargs):
        """还原已删除文章"""
        params = json.loads(self.request.body.decode('utf-8'))

        if article_uuid:
            try:
                update_article = await self.application.objects.get(ArticleModel, uuid=article_uuid, state=200)

                update_article.state = 2

                await self.application.objects.update(update_article)
                re_data = resSuccess('成功')

            except ArticleModel.DoesNotExist as e:
                self.set_status(400)
                re_data = resSuccess('失败')
        else:
            self.set_status(400)
            re_data = resSuccess('失败')

        self.finish(re_data)


class DelArticleRHandler(RedisHandler):
    @authenticated_async
    async def delete(self, article_uuid, *args, **kwargs):
        """彻底删除文章"""
        try:
            article = await self.application.objects.get(
                ArticleModel.select().where(ArticleModel.state == 200, ArticleModel.uuid == article_uuid)
            )
            await self.application.objects.delete(article)
            re_data = resSuccess('成功')

        except ArticleModel.DoesNotExist:
            self.set_status(400)
            re_data = resSuccess('失败')

        self.finish(re_data)


class GetArticleRHandler(RedisHandler):
    @authenticated_async
    async def get(self, *args, **kwargs):
        """获取已删除文章列表"""
        current_page = self.get_argument('current_page', 1)
        try:
            articles = await self.application.objects.execute(
                ArticleModel.select()
                    .where(ArticleModel.state == 200)
                    .paginate(int(current_page), int(settings['page_size']))
                    .order_by(ArticleModel.update_time.desc())
            )

            articles_count = await self.application.objects.count(
                ArticleModel.select().where(ArticleModel.state == 200)
            )

            article_list = []
            for article in articles:
                article = model_to_dict(article)
                tag_list = []
                for tag in str(article['tag']).split('|'):
                    if tag:
                        tag = await self.application.objects.get(TagModel, name=tag)
                        tag_list.append(model_to_dict(tag))

                article['tag'] = tag_list
                article_list.append(article)

            re_data = resSuccess('成功')
            re_data['result'] = {
                'data': article_list,
                'pagination': {
                    'current_page': int(current_page),
                    'page_size': int(settings['page_size']),
                    'total': articles_count,
                    'total_page': math.ceil(articles_count / int(settings['page_size']))
                }
            }

        except ArticleModel.DoesNotExist:
            re_data = resSuccess('失败')
            self.set_status(400)

        self.finish(json.dumps(re_data, default=json_serial))


class AllSketchHandler(RedisHandler):
    @authenticated_async
    async def post(self, *args, **kwargs):
        """批量操作草稿箱文章"""
        re_data = {}

        params = json.loads(self.request.body.decode('utf-8'))
        state = int(params.get('state', 0))
        sketch_uuid = params.get('sketch_uuid', [])

        if sketch_uuid:
            for uuid in sketch_uuid:
                try:
                    article = await self.application.objects.get(
                        ArticleModel, uuid=uuid
                    )

                    if article.title and article.content and article.desc and article.tag:
                        if state == 100:
                            article.state = 1

                        elif state == 200:
                            article.state = 200

                        await self.application.objects.update(article)
                        re_data = resSuccess('成功')

                    else:
                        re_data = resSuccess('失败', error='请完善文章信息在发布')
                        self.finish(re_data)
                        return False

                except ArticleModel.DoesNotExist as e:
                    self.set_status(400)
                    re_data = resSuccess('失败')
        else:
            re_data = resSuccess('失败')

        self.finish(re_data)


class PushSketchHandler(RedisHandler):
    @authenticated_async
    async def put(self, sketch_uuid, *args, **kwargs):
        """发布草稿箱文章"""
        try:
            article = await self.application.objects.get(ArticleModel, uuid=sketch_uuid, state=2)
            article.state = 1
            await self.application.objects.update(article)

            re_data = resSuccess('成功')

        except ArticleModel.DoesNotExist:
            self.set_status(400)
            re_data = resSuccess('失败')

        self.finish(re_data)


class DelSketchHandler(RedisHandler):
    @authenticated_async
    async def delete(self, sketch_uuid, *args, **kwargs):
        """删除文章草稿"""
        try:
            # await self.application.objects.delete(
            #     ArticleModel.select().where(ArticleModel.state == 2, ArticleModel.uuid == sketch_uuid)
            # )
            article = await self.application.objects.get(
                ArticleModel, uuid=sketch_uuid, state=2
            )
            article.state = 200
            await self.application.objects.update(article)

            re_data = resSuccess('成功')

        except ArticleModel.DoesNotExist:
            self.set_status(400)
            re_data = resSuccess('失败')

        self.finish(re_data)


class GetSketchHandler(RedisHandler):
    @authenticated_async
    async def get(self, *args, **kwargs):
        """获取草稿箱列表"""
        current_page = self.get_argument('current_page', 1)
        try:
            articles = await self.application.objects.execute(
                ArticleModel.select()
                    .where(ArticleModel.state == 2)
                    .paginate(int(current_page), int(settings['page_size']))
                    .order_by(ArticleModel.update_time.desc())
            )

            articles_count = await self.application.objects.count(
                ArticleModel.select().where(ArticleModel.state == 2)
            )

            article_list = []
            for article in articles:
                article = model_to_dict(article)
                tag_list = []
                for tag in str(article['tag']).split('|'):
                    if tag:
                        tag = await self.application.objects.get(TagModel, name=tag)
                        tag_list.append(model_to_dict(tag))

                article['tag'] = tag_list
                article_list.append(article)

            re_data = resSuccess('成功')
            re_data['result'] = {
                'data': article_list,
                'pagination': {
                    'current_page': int(current_page),
                    'page_size': int(settings['page_size']),
                    'total': articles_count,
                    'total_page': math.ceil(articles_count / int(settings['page_size']))
                }
            }

        except ArticleModel.DoesNotExist:
            re_data = resSuccess('失败')
            self.set_status(400)

        self.finish(json.dumps(re_data, default=json_serial))


class EditAllArticleHandler(RedisHandler):
    @authenticated_async
    async def post(self, *args, **kwargs):
        """批量操作文章"""
        re_data = {}

        params = json.loads(self.request.body.decode('utf-8'))
        state = int(params.get('state', 0))
        article_uuid = params.get('article_uuid', [])

        if article_uuid:
            for uuid in article_uuid:
                try:
                    article = await self.application.objects.get(
                        ArticleModel, uuid=uuid
                    )

                    if state == 100:
                        article.state = 2

                    elif state == 200:
                        article.state = 200

                    await self.application.objects.update(article)
                    re_data = resSuccess('成功')

                except ArticleModel.DoesNotExist as e:
                    self.set_status(400)
                    re_data = resSuccess('失败')
        else:
            re_data = resSuccess('失败')

        self.finish(re_data)


class ArticleHandler(RedisHandler):
    @authenticated_async
    async def get(self, *args, **kwargs):
        """获取文章列表"""
        re_list = []
        re_data = {}
        current_page = self.get_argument('current_page', None)
        if current_page:
            try:
                articles = await self.application.objects.execute(
                    ArticleModel.select()
                        .where(ArticleModel.state == 1)
                        .paginate(int(current_page), int(settings['page_size']))
                        .order_by(ArticleModel.update_time.desc())
                )
                articles_count = await self.application.objects.count(ArticleModel.select())

                for article in articles:
                    article = model_to_dict(article)
                    tag_list = []
                    for tag in str(article['tag']).split('|'):
                        if tag:
                            tag = await self.application.objects.get(TagModel, name=tag)
                            tag_list.append(model_to_dict(tag))

                    article['tag'] = tag_list
                    re_list.append(article)

                re_data = resSuccess('成功')
                re_data['result'] = {
                    'data': re_list,
                    'pagination': {
                        'current_page': int(current_page),
                        'page_size': int(settings['page_size']),
                        'total': articles_count,
                        'total_page': math.ceil(articles_count / int(settings['page_size']))
                    }
                }

            except ArticleModel.DoesNotExist as e:
                self.set_status(400)
                re_data = resSuccess('失败')

        self.finish(json.dumps(re_data, default=json_serial))

    @authenticated_async
    async def put(self, *args, **kwargs):
        """添加文章"""
        re_data = {}
        params = json.loads(self.request.body.decode('utf-8'))
        try:
            article = await self.application.objects.create(
                ArticleModel, content=params['content'], title=params['title'], desc=params['desc'],
                keyword=params['keyword'], editContent=params['editContent'],
                tag='|'.join(params['tag']), state=params['state'])

            if article:
                re_data = resSuccess('成功')

        except ArticleModel.DoesNotExist as e:
            self.set_status(400)
            re_data = resSuccess('失败')

        self.finish(re_data)


class OperationArticleHandler(RedisHandler):
    @authenticated_async
    async def get(self, article_uuid, *args, **kwargs):
        """查询文章"""
        if article_uuid:
            try:
                article = await self.application.objects.get(ArticleModel, uuid=article_uuid)
                article = model_to_dict(article)
                tag_list = []
                for tag in str(article['tag']).split('|'):
                    if tag:
                        tag = await self.application.objects.get(TagModel, name=tag)
                        tag_list.append(model_to_dict(tag))

                article['tag'] = tag_list

                re_data = resSuccess('成功')
                re_data['result'] = article

            except ArticleModel.DoesNotExist as e:
                self.set_status(400)
                re_data = resSuccess('失败')

        else:
            self.set_status(400)
            re_data = resSuccess('失败')

        self.finish(json.dumps(re_data, default=json_serial))

    @authenticated_async
    async def post(self, article_uuid, *args, **kwargs):
        """修改文章"""
        article = json.loads(self.request.body.decode('utf-8'))

        if not article:
            self.set_status(400)
            re_data = resSuccess('失败')
            self.finish(re_data)

        if article_uuid:
            try:
                update_article = await self.application.objects.get(ArticleModel, uuid=article_uuid)
                for key, value in article.items():
                    if isinstance(value, list) and key == 'tag':
                        tag_list = []
                        for item in value:
                            tag = await self.application.objects.get(TagModel, uuid=item)
                            tag_list.append(tag.name)
                        update_article.tag = '|'.join(tag_list)
                    elif isinstance(value, (str, int)):
                        setattr(update_article, f'{key}', value)

                await self.application.objects.update(update_article)
                re_data = resSuccess('成功')

            except ArticleModel.DoesNotExist as e:
                self.set_status(400)
                re_data = resSuccess('失败')
        else:
            self.set_status(400)
            re_data = resSuccess('失败')

        self.finish(json.dumps(re_data, default=json_serial))

    @authenticated_async
    async def delete(self, article_uuid, *args, **kwargs):
        """删除文章"""
        if article_uuid:
            try:
                article = await self.application.objects.get(ArticleModel, uuid=article_uuid)
                article.state = 200
                await self.application.objects.update(article)

                re_data = resSuccess('成功')
            except ArticleModel.DoesNotExist as e:
                self.set_status(400)
                re_data = resSuccess('失败')
        else:
            self.set_status(400)
            re_data = resSuccess('失败')

        self.finish(re_data)
