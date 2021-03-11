import json
import math

from playhouse.shortcuts import model_to_dict

from apps.models.comment_models import CommentModel
from apps.utils.utils import json_serial
from apps.utils.re_data_params import resSuccess

from blog.handler import RedisHandler
from blog.settings import settings

from apps.models.tag_models import TagModel
from apps.models.article_models import ArticleModel


class getAllArticleHandler(RedisHandler):
    async def get(self, *args, **kwargs):
        """文章归档"""
        try:
            articles = await self.application.objects.execute(
                ArticleModel.select().order_by(ArticleModel.update_time.desc())
            )

            article_data = {}
            article_list = []
            month_set = set()

            for article in articles:
                article_dict = model_to_dict(article)
                year = str(article_dict['update_time'].year)
                month = str(article_dict['update_time'].month)
                tag_list = []
                for tag in str(article_dict['tag']).split('|'):
                    if tag:
                        tag = await self.application.objects.get(TagModel, name=tag)
                        tag_list.append(model_to_dict(tag))

                article_dict['tag'] = tag_list

                if year not in article_data.values():
                    article_year = article_data.get(year, None)
                    if article_year:
                        for year in article_year:
                            if year.get(month, None):
                                year[month].append(article_dict)
                                month_set.add(month)

                            else:
                                if month not in month_set:
                                    year[month] = [article_dict]
                                    month_set.add(month)

                    else:
                        _month = {}
                        _month[month] = [article_dict]
                        article_data[year] = [_month]

            for article_key, article_value in article_data.items():
                month_list = []
                for month_data in article_value:
                    for month_key, month_value in month_data.items():
                        month_list.append({
                            'articleList': month_value,
                            'month': '0' + month_key if int(month_key) < 10 else month_key
                        })
                article_list.append({
                    'year': article_key,
                    'monthList': month_list
                })

            re_data = resSuccess('成功')
            re_data['result'] = article_list

        except ArticleModel.DoesNotExist as e:
            self.set_status(400)
            re_data = resSuccess('失败')
        except TagModel.DoesNotExist as e:
            self.set_status(400)
            re_data = resSuccess('失败')

        self.finish(json.dumps(re_data, default=json_serial))


class LikeArticleHandler(RedisHandler):
    async def post(self, article_id, *args, **kwargs):
        """添加文章喜欢"""
        try:
            article = await self.application.objects.get(ArticleModel, uuid=article_id)
            article.likes += 1
            await self.application.objects.update(article)
            re_data = resSuccess('成功')
        except ArticleModel.DoesNotExist as e:
            re_data = resSuccess('失败')
        self.finish(re_data)

    async def delete(self, article_id, *args, **kwargs):
        """删除文章喜欢"""
        try:
            article = await self.application.objects.get(ArticleModel, uuid=article_id)
            article.likes -= 1
            await self.application.objects.update(article)
            re_data = resSuccess('成功')
        except ArticleModel.DoesNotExist as e:
            re_data = resSuccess('失败')
        self.finish(re_data)


class ArticleHandler(RedisHandler):
    async def get(self, *args, **kwargs):
        """分页获取文章列表页  每页十条"""
        re_list = []

        hot = self.get_argument("hot", None)
        current_page = self.get_argument("article_page", None)
        tag_page = self.get_argument("tag_page", 1)
        keyword_page = self.get_argument("keyword_page", 1)
        keyword = self.get_argument("keyword", None)
        article_tag = self.get_argument('tag', None)

        page = current_page

        try:
            article_model = ArticleModel.select().where(ArticleModel.state==1)
            articles = ''

            if keyword:
                articles = await self.application.objects.execute(
                    ArticleModel.select()
                        .where(ArticleModel.state==1, ArticleModel.title.contains(str(keyword)))
                        .paginate(int(keyword_page), int(settings['page_size']))
                        .order_by(ArticleModel.update_time.asc())
                )

                article_counts = ArticleModel.select().where(
                    ArticleModel.state==1, 
                    ArticleModel.title.contains(str(keyword))
                )
                page = int(keyword_page)

            elif article_tag and article_tag != 'all':
                tag_model = await self.application.objects.get(TagModel, uuid=article_tag)
                articles = await self.application.objects.execute(
                    ArticleModel.select()
                        .where(ArticleModel.tag.contains(tag_model.name), ArticleModel.state==1)
                        .paginate(int(tag_page), int(settings['page_size']))
                        .order_by(ArticleModel.update_time.desc())
                )

                article_counts = ArticleModel.select().where(
                    ArticleModel.tag.contains(tag_model.name),
                    ArticleModel.state==1
                )
                page = int(tag_page)

            else:
                if current_page:
                    articles = await self.application.objects.execute(
                        article_model
                            .paginate(int(current_page), int(settings['page_size']))
                            .order_by(ArticleModel.update_time.desc())
                    )

                elif hot:
                    article_model = article_model.order_by(ArticleModel.views.desc()).limit(10)
                    articles = await self.application.objects.execute(article_model)

                article_counts = article_model

            articles_count = await self.application.objects.count(article_counts)

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
                'list': re_list,
                'pagination': {
                    'current_page': page,
                    'page_size': 10,
                    'total': articles_count,
                    'total_page': math.ceil(articles_count / 10)
                }
            }

        except ArticleModel.DoesNotExist as e:
            self.set_status(400)
            re_data = resSuccess('失败')
        except TagModel.DoesNotExist as e:
            self.set_status(400)
            re_data = resSuccess('失败')

        self.finish(json.dumps(re_data, default=json_serial))


class ArticleIDHandler(RedisHandler):
    async def get(self, article_uuid, *args, **kwargs):
        """根据ID获取文章"""
        tag_list = []
        try:
            article = await self.application.objects.get(ArticleModel, uuid=article_uuid)
            article.views += 1
            await self.application.objects.update(article)

            # comment_count = await self.application.objects.count(
            #     CommentModel.extend().where(CommentModel.state == 1, CommentModel.article == article.id)
            # )

            article = model_to_dict(article)
            for tag in article['tag'].split('|'):
                tag_dict = await self.application.objects.get(TagModel, name=tag)
                tag_dict = model_to_dict(tag_dict)
                tag_list.append(tag_dict)

            article['tag'] = tag_list
            # article['comment_count'] = comment_count

            re_data = resSuccess('成功')
            re_data['result'] = article

        except ArticleModel.DoesNotExist as e:
            self.set_status(400)
            re_data = resSuccess('失败')

        self.finish(json.dumps(re_data, default=json_serial))

