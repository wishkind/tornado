import json

from playhouse.shortcuts import model_to_dict

from blog.handler import RedisHandler
from apps.models.reply_models import ReplyModel, ReplyInfoModel, ReplyCommentInfoModel
from apps.models.comment_models import CommentModel
from apps.utils.re_data_params import resSuccess
from apps.utils.utils import json_serial, get_ip_info


class PutReplyHandler(RedisHandler):
    async def put(self, *args, **kwargs):
        """添加评论回复"""
        params = json.loads(self.request.body.decode('utf-8'))
        try:
            headers = self.request.headers
            reply_data = params['from']
            reply_data_to = params['to']
            ip_info = get_ip_info(self.request.remote_ip)

            reply_com_info = await self.application.objects.create(
                ReplyCommentInfoModel, portrait=reply_data_to['portrait'], email=reply_data_to['email'],
                name=reply_data_to['name'], site=reply_data_to['site'], ip=self.request.remote_ip,
                agent=headers.get('User-Agent', ''), city=ip_info.get('city', None),
                country=ip_info.get('country', None),
                province=ip_info.get('province', None), lin_lat=ip_info.get('lin_lat', None)
            )

            reply_info = await self.application.objects.create(
                ReplyInfoModel, portrait=reply_data['portrait'], email=reply_data['email'],
                name=reply_data['name'], site=reply_data['site'], ip=self.request.remote_ip,
                agent=headers.get('User-Agent', ''), city=ip_info.get('city', None),
                country=ip_info.get('country', None),
                province=ip_info.get('province', None), lin_lat=ip_info.get('lin_lat', None)
            )

            comment = await self.application.objects.get(CommentModel, uuid=params['cid'])
            comment = await self.application.objects.create(
                ReplyModel, reply_info=reply_info.id, content=params['content'], article_id=params['article_id'],
                com_info=comment.comment_info_id, cid=params['cid'], reply_comment=reply_com_info.id
            )

            comment_reply = await self.application.objects.get(CommentModel, uuid=comment.cid)
            comment_reply.reply += 1
            await self.application.objects.update(comment_reply)

            re_data = resSuccess('成功')

        except ReplyModel.DoesNotExist as e:
            self.set_status(400)
            re_data = resSuccess('失败')

        self.finish(re_data)


class GetReplyHandler(RedisHandler):
    async def get(self, reply_cid, *args, **kwargs):
        """获取回复评论"""
        reply_data_list = []
        try:
            reply_data = await self.application.objects.execute(
                ReplyModel.extend()
                    .where(ReplyModel.cid==reply_cid, ReplyModel.state == 1)
                    .order_by(ReplyModel.update_time.desc())
            )

            for reply in reply_data:
                reply_dict = model_to_dict(reply)
                reply_data_list.append(reply_dict)

            re_data = resSuccess('成功')
            re_data['result'] = reply_data_list

        except CommentModel.DoesNotExist as e:
            self.set_status(400)
            re_data = resSuccess('失败')

        self.finish(json.dumps(re_data, default=json_serial))

