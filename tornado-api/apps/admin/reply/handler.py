import math
import json

from playhouse.shortcuts import model_to_dict

from apps.utils.decorators import authenticated_async
from blog.handler import RedisHandler
from blog.settings import settings

from apps.models.reply_models import ReplyModel
from apps.models.comment_models import CommentModel
from apps.utils.utils import json_serial
from apps.utils.re_data_params import resSuccess


async def del_com_rep(self, reply):
    """删除评论的回复"""
    comment = await self.application.objects.get(
        CommentModel.select().where(CommentModel.uuid == reply.cid)
    )
    comment.reply -= 1

    await self.application.objects.update(comment)


class FilterReplyHandler(RedisHandler):
    @authenticated_async
    async def get(self, comment_uuid, *args, **kwargs):
        """筛选评论"""
        state = int(self.get_argument('state', 0))
        current_page = self.get_argument('current_page', 1)
        if comment_uuid:
            is_state = False
            try:
                reply = ReplyModel.extend()
                reply_count = reply.where(ReplyModel.cid == comment_uuid)

                if state == 101:
                    reply = reply.where(ReplyModel.cid == comment_uuid)

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
                    reply_count = reply.where(ReplyModel.cid == comment_uuid, ReplyModel.state == state)
                    reply = reply.where(ReplyModel.state == state, ReplyModel.cid == comment_uuid)

                else:
                    reply = reply.where(ReplyModel.cid == comment_uuid)

                reply_items = await self.application.objects.execute(reply)
                reply_count = await self.application.objects.count(reply_count)

                reply_list = []
                for item in reply_items:
                    reply_dict = model_to_dict(item)
                    reply_list.append(reply_dict)

                re_data = resSuccess('成功')
                re_data['result'] = {
                    'data': reply_list,
                    'pagination': {
                        'current_page': current_page,
                        'page_size': settings['page_size'],
                        'total': reply_count,
                        'total_page': math.ceil(reply_count / int(settings['page_size']))
                    }
                }
            except CommentModel.DoesNotExist:
                self.set_status(400)
                re_data = resSuccess('失败')
            except ReplyModel.DoesNotExist:
                self.set_status(400)
                re_data = resSuccess('失败')

        else:
            self.set_status(400)
            re_data = resSuccess('失败')

        self.finish(json.dumps(re_data, default=json_serial))


class EditAllReplyHandler(RedisHandler):
    @authenticated_async
    async def post(self, *args, **kwargs):
        """批量修改评论回复 100:  删除 200:  通过 300:  不通过"""
        re_data = resSuccess('成功')
        params = json.loads(self.request.body.decode('utf-8'))
        state = int(params.get('state', 0))
        reply_uuid = params.get('reply_uuid', [])

        is_state = True

        if reply_uuid:
            for uuid in reply_uuid:
                try:
                    reply = await self.application.objects.get(
                        ReplyModel, uuid=uuid
                    )

                    if state == 100:
                        await del_com_rep(self, reply)
                        await self.application.objects.delete(reply)

                        is_state = False

                    elif state == 300:
                        reply.state = 2

                    elif state == 200:
                        reply.state = 1

                    if is_state:
                        await self.application.objects.update(reply)
                    re_data = resSuccess('成功')

                except ReplyModel.DoesNotExist as e:
                    self.set_status(400)
                    re_data = resSuccess('失败')
        else:
            re_data = resSuccess('失败')

        self.finish(re_data)


class DelReplyHandler(RedisHandler):
    async def delete(self, reply_uuid, *args, **kwargs):
        """删除评论回复"""
        try:
            reply = await self.application.objects.get(ReplyModel, uuid=reply_uuid)
            await del_com_rep(self, reply)
            await self.application.objects.delete(reply)

            re_data = resSuccess('成功')

        except CommentModel.DoesNotExist as e:
            re_data = resSuccess('失败')

        self.finish(re_data)


class EditReplyHandler(RedisHandler):
    @authenticated_async
    async def post(self, reply_uuid, *args, **kwargs):
        """修改回复"""
        params = json.loads(self.request.body.decode('utf-8'))
        state = params.get('state', None)
        content = params.get('content', None)

        try:
            reply = await self.application.objects.get(
                ReplyModel, uuid=reply_uuid
            )

            if content:
                reply.content = content

            if state or state == 0 or state == '0':

                reply.state = int(state)

            await self.application.objects.update(reply)
            re_data = resSuccess('成功')

        except ReplyModel.DoesNotExist as e:
            self.set_status(400)
            re_data = resSuccess('失败')

        self.finish(re_data)


class GetReplyHandler(RedisHandler):
    @authenticated_async
    async def get(self, *args, **kwargs):
        """获取指定评论的所有回复"""

        comment_uuid = self.get_argument('comment_uuid', None)
        reply_page = self.get_argument('reply_page', 1)
        state = int(self.get_argument('state', 0))
        is_state = False

        if comment_uuid:
            reply = ReplyModel.extend()
            reply_count = reply.where(ReplyModel.cid == comment_uuid)

            if state == 101:
                reply = reply.where(ReplyModel.cid == comment_uuid)

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
                reply_count = reply.where(ReplyModel.cid == comment_uuid, ReplyModel.state == state)
                reply = reply.where(ReplyModel.state == state, ReplyModel.cid == comment_uuid)

            else:
                reply = reply.where(ReplyModel.cid == comment_uuid)

            reply_items = await self.application.objects.execute(
                reply.paginate(int(reply_page), int(settings['page_size']))
            )

            reply_count = await self.application.objects.count(reply_count)

            reply_list = []
            for item in reply_items:
                reply_dict = model_to_dict(item)
                reply_list.append(reply_dict)

            re_data = resSuccess('成功')
            re_data['result'] = {
                'total': reply_count,
                'data': reply_list,
                'pagination': {
                    'current_page': int(reply_page),
                    'page_size': int(settings['page_size']),
                    'total': reply_count,
                    'total_page': math.ceil(reply_count / int(settings['page_size']))
                }
            }

        else:
            self.set_status(400)
            re_data = resSuccess('失败')

        self.finish(json.dumps(re_data, default=json_serial))
