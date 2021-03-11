import json

from playhouse.shortcuts import model_to_dict

from apps.utils.re_data_params import resSuccess
from apps.utils.utils import json_serial
from blog.handler import RedisHandler

from apps.models.note_models import NoteModel


class GetNoteHandler(RedisHandler):
    async def get(self, *args, **kwargs):
        """获取友情链接list"""

        try:
            notes = await self.application.objects.execute(NoteModel.select().where(NoteModel.state == 1))

            note_list = []
            for note in notes:
                note_dict = model_to_dict(note)
                note_list.append(note_dict)

            re_data = resSuccess('成功')
            re_data['list'] = note_list

        except NoteModel.DoesNotExist as e:
            self.set_status(400)
            re_data = resSuccess('失败')

        self.finish(json.dumps(re_data, default=json_serial))
