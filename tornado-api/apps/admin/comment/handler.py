import json
import math

from playhouse.shortcuts import model_to_dict
from blog.handler import RedisHandler
from blog.settings import settings

from apps.utils.utils import json_serial
from apps.utils.re_data_params import resSuccess
from apps.utils.decorators import authenticated_async

from apps.models.comment_models import CommentModel
from apps.models.article_models import ArticleModel
from apps.models.reply_models import ReplyModel


async def del_com_rep(self, comment):
    """删除评论和对应所有的回复"""
    article = await self.application.objects.get(
        ArticleModel.select().where(ArticleModel.id == comment.article_id)
    )
    article.comments -= 1

    await self.application.objects.execute(
        ReplyModel.delete().where(
            ReplyModel.cid == comment.uuid
        )
    )

    await self.application.objects.update(article)


class DelCommentHandler(RedisHandler):
    async def delete(self, comment_uuid, *args, **kwargs):
        """删除评论"""
        try:
            comment = await self.application.objects.get(CommentModel, uuid=comment_uuid)

            await del_com_rep(self, comment)

            await self.application.objects.delete(comment)

            re_data = resSuccess('成功')

        except CommentModel.DoesNotExist as e:
            re_data = resSuccess('失败')

        self.finish(re_data)


class FilterCommentHandler(RedisHandler):
    @authenticated_async
    async def get(self, article_uuid, *args, **kwargs):
        """筛选评论"""
        state = int(self.get_argument('state', 0))
        current_page = self.get_argument('current_page', 1)

        if article_uuid:
            is_state = False
            try:
                article = await self.application.objects.get(ArticleModel, uuid=article_uuid)
                comment = CommentModel.extend()

                if state == 101:
                    comment = comment.where(CommentModel.article == article.id)

                elif state == 102:
                    state = 0
                    is_state = True

                elif state == 103:
                    state = 1
                    is_state = True

                elif state == 104:
                    state = 2
                    is_state = True

                if is_state:
                    comment = comment.where(CommentModel.state == state, CommentModel.article == article.id)

                else:
                    comment = comment.where(CommentModel.article == article.id)

                comments = await self.application.objects.execute(
                    comment.paginate(int(current_page), int(settings['page_size']))
                )

                comment_count = await self.application.objects.count(comment)

                comment_list = []
                for comment in comments:
                    comment_dict = model_to_dict(comment)
                    comment_list.append(comment_dict)

                re_data = resSuccess('成功')
                re_data['result'] = {
                    'data': comment_list,
                    'pagination': {
                        'current_page': current_page,
                        'page_size': settings['page_size'],
                        'total': comment_count,
                        'total_page': math.ceil(comment_count / int(settings['page_size']))
                    }
                }
            except CommentModel.DoesNotExist:
                self.set_status(400)
                re_data = resSuccess('失败')
            except ArticleModel.DoesNotExist:
                self.set_status(400)
                re_data = resSuccess('失败')

        else:
            self.set_status(400)
            re_data = resSuccess('失败')

        self.finish(json.dumps(re_data, default=json_serial))


class EditAllCommentHandler(RedisHandler):
    @authenticated_async
    async def post(self, *args, **kwargs):
        """批量修改评论 100:  删除 200:  通过 300:  不通过"""
        re_data = resSuccess('成功')
        params = json.loads(self.request.body.decode('utf-8'))
        state = int(params.get('state', 0))
        comment_uuid = params.get('comment_uuid', [])

        is_state = True

        if comment_uuid:
            for uuid in comment_uuid:
                try:
                    comment = await self.application.objects.get(
                        CommentModel, uuid=uuid
                    )

                    if state == 100:
                        await del_com_rep(self, comment)
                        await self.application.objects.delete(comment)

                        is_state = False

                    elif state == 300:
                        comment.state = 2

                    elif state == 200:
                        comment.state = 1

                    if is_state:
                        await self.application.objects.update(comment)
                    re_data = resSuccess('成功')

                except CommentModel.DoesNotExist as e:
                    self.set_status(400)
                    re_data = resSuccess('失败')
        else:
            re_data = resSuccess('失败')

        self.finish(re_data)


class EditCommentHandler(RedisHandler):
    @authenticated_async
    async def post(self, comment_uuid, *args, **kwargs):
        """修改评论"""
        params = json.loads(self.request.body.decode('utf-8'))
        state = params.get('state', None)
        content = params.get('content', None)
        try:
            comment = await self.application.objects.get(
                CommentModel, uuid=comment_uuid
            )

            if content:
                comment.content = content

            if state or state == 0 or state == '0':
                comment.state = int(state)
            await self.application.objects.update(comment)
            re_data = resSuccess('成功')

        except CommentModel.DoesNotExist as e:
            self.set_status(400)
            re_data = resSuccess('失败')

        self.finish(re_data)


class GetCommentHandler(RedisHandler):
    @authenticated_async
    async def get(self, *args, **kwargs):
        """获取评论列表"""
        current_page = int(self.get_argument('current_page', 1))
        article_uuid = self.get_argument('article_uuid')
        state = int(self.get_argument('state', 1))
        is_state = False
        try:
            article = await self.application.objects.get(ArticleModel, uuid=article_uuid)
            comment = CommentModel.extend()
            comment_count = comment.where(CommentModel.article == article.id)

            if state == 104:
                state = 2
                is_state = True

            elif state == 103:
                state = 1
                is_state = True

            elif state == 102:
                state = 0
                is_state = True

            if is_state:
                comment_count = comment.where(CommentModel.article == article.id, CommentModel.state == state)
                comment = comment.where(CommentModel.article == article.id, CommentModel.state == state)

            else:
                comment = comment.where(CommentModel.article == article.id)

            comments = await self.application.objects.execute(
                comment.paginate(current_page, int(settings['page_size']))
            )

            comment_count = await self.application.objects.count(comment_count)

            comment_list = []
            for comment in comments:
                comment_dict = model_to_dict(comment)
                comment_list.append(comment_dict)

            re_data = resSuccess('成功')
            re_data['result'] = {
                'data': comment_list,
                'pagination': {
                    'current_page': current_page,
                    'page_size': int(settings['page_size']),
                    'total': comment_count,
                    'total_page': math.ceil(comment_count / int(settings['page_size']))
                }
            }

        except ArticleModel.DoesNotExist as e:
            self.set_status(400)
            re_data = resSuccess('失败')

        self.finish(json.dumps(re_data, default=json_serial))

