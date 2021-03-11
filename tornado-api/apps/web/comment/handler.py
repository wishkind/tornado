import json
import re

from playhouse.shortcuts import model_to_dict

from apps.models.reply_models import ReplyModel
from blog.handler import RedisHandler

from apps.utils.re_data_params import resSuccess
from apps.utils.utils import json_serial, get_ip_info
from apps.models.comment_models import CommentModel, CommentInfoModel
from apps.models.article_models import ArticleModel


class LikeCommentHandler(RedisHandler):
    async def post(self, comment_uuid, *args, **kwargs):
        """喜欢评论"""
        try:
            comment = await self.application.objects.get(CommentModel, uuid=comment_uuid)
            comment.likes += 1
            await self.application.objects.update(comment)
            re_data = resSuccess('成功')
        except CommentModel.DoesNotExist as e:
            re_data = resSuccess('失败')
        self.finish(re_data)

    async def delete(self, comment_uuid, *args, **kwargs):
        """删除评论喜欢数"""
        try:
            comment = await self.application.objects.get(CommentModel, uuid=comment_uuid)
            comment.likes -= 1
            await self.application.objects.update(comment)
            re_data = resSuccess('成功')
        except CommentModel.DoesNotExist as e:
            re_data = resSuccess('失败')
        self.finish(re_data)


class PutCommentHandler(RedisHandler):
    async def put(self, *args, **kwargs):
        """添加评论"""
        params = json.loads(self.request.body.decode('utf-8'))
        try:
            headers = self.request.headers
            author = params['author']

            ip_info = get_ip_info(self.request.remote_ip)

            article = await self.application.objects.get(ArticleModel, uuid=params['article_id'])

            comment_info = await self.application.objects.create(
                CommentInfoModel, ip=self.request.remote_ip, agent=str(headers.get('User-Agent', '')),
                city=ip_info.get('city', None), country=ip_info.get('country', None),
                province=ip_info.get('province', None),
                lin_lat=ip_info.get('lin_lat', None),
                name=author['name'], email=author['email'], site=author['site'], portrait=author['portrait']
            )

            await self.application.objects.create(
                CommentModel, article=article.id, content=params['content'],
                comment_info=comment_info.id
            )

            article.comments += 1
            await self.application.objects.update(article)

            re_data = resSuccess('成功')

        except CommentModel.DoesNotExist as e:
            self.set_status(400)
            re_data = resSuccess('失败')

        except ArticleModel.DoesNotExist as e:
            self.set_status(400)
            re_data = resSuccess('失败')

        self.finish(re_data)


class CommentHandler(RedisHandler):
    async def get(self, *args, **kwargs):
        """获取评论列表"""
        re_data = {}
        comment_list = []
        article_id = self.get_argument('article_id', None)
        if article_id:
            try:

                article = await self.application.objects.get(ArticleModel, uuid=article_id)

                comments = await self.application.objects.execute(
                    CommentModel.extend()
                        .where(CommentModel.article==article.id, CommentModel.state == 1)
                        .order_by(CommentModel.update_time.desc())
                )

                for comment in comments:
                    comment_dict = model_to_dict(comment)
                    # reply_count = await self.application.objects.count(
                    #     ReplyModel.extend().where(ReplyModel.cid == comment_dict['uuid'], ReplyModel.state == 1)
                    # )
                    # comment_dict['reply_count'] = reply_count
                    comment_list.append(comment_dict)

                re_data = resSuccess('成功')
                re_data['data'] = comment_list

            except CommentModel.DoesNotExist as e:
                self.set_status(400)
                re_data = resSuccess('失败')

        self.finish(json.dumps(re_data, default=json_serial))

