import json
import math

from playhouse.shortcuts import model_to_dict

from apps.utils.decorators import authenticated_async
from apps.utils.re_data_params import resSuccess
from apps.utils.utils import json_serial
from blog.handler import RedisHandler
from blog.settings import settings

from apps.models.note_models import NoteModel


class GetNoteHandler(RedisHandler):
    @authenticated_async
    async def get(self, *args, **kwargs):
        """获取友情链接list"""

        current_page = self.get_argument('current_page', 1)

        try:
            notes = await self.application.objects.execute(NoteModel.select())

            note_count = await self.application.objects.count(NoteModel.select())

            note_list = []
            for note in notes:
                note_dict = model_to_dict(note)
                note_list.append(note_dict)

            re_data = resSuccess('成功')
            re_data['result'] = {
                'data': note_list,
                'pagination': {
                    'current_page': int(current_page),
                    'page_size': int(settings['page_size']),
                    'total': note_count,
                    'total_page': math.ceil(note_count / int(settings['page_size']))
                }
            }

        except NoteModel.DoesNotExist as e:
            self.set_status(400)
            re_data = resSuccess('失败')

        self.finish(json.dumps(re_data, default=json_serial))


class AddNoteHandler(RedisHandler):
    @authenticated_async
    async def put(self, *args, **kwargs):
        """添加项目"""
        re_data = {}
        params = json.loads(self.request.body.decode('utf-8'))

        try:
            note = await self.application.objects.create(
                NoteModel, name=params['name'], desc=params['desc'],
                logo=params['logo'] or '', link=params['link'] or '',
                state=params['state']
            )

            if note:
                re_data = resSuccess('成功')

        except NoteModel.DoesNotExist as e:
            self.set_status(400)
            re_data = resSuccess('失败')

        self.finish(re_data)


class DelNoteHandler(RedisHandler):
    @authenticated_async
    async def delete(self, note_uuid, *args, **kwargs):
        """删除项目"""
        if note_uuid:
            try:
                note = await self.application.objects.get(NoteModel, uuid=note_uuid)
                await self.application.objects.delete(note)

                re_data = resSuccess('成功')
            except NoteModel.DoesNotExist as e:
                self.set_status(400)
                re_data = resSuccess('失败')
        else:
            self.set_status(400)
            re_data = resSuccess('失败', error='请选择删除的友链')

        self.finish(re_data)


class GetIdNoteHandler(RedisHandler):
    async def get(self, note_uuid, *args, **kwargs):
        """根据ID获取项目"""
        if note_uuid:
            try:
                note = await self.application.objects.get(NoteModel, uuid=note_uuid)
                note_dict = model_to_dict(note)

                re_data = resSuccess('成功')
                re_data['result'] = note_dict

            except NoteModel.DoesNotExist as e:
                self.set_status(400)
                re_data = resSuccess('失败')
        else:
            self.set_status(400)
            re_data = resSuccess('失败')

        self.finish(json.dumps(re_data, default=json_serial))


class EditNoteHandler(RedisHandler):
    @authenticated_async
    async def post(self, note_uuid, *args, **kwargs):
        """编辑项目"""
        params = json.loads(self.request.body.decode('utf-8'))

        if not params:
            self.set_status(400)
            re_data = resSuccess('失败')
            self.finish(re_data)

        if note_uuid:
            try:
                note = await self.application.objects.get(NoteModel, uuid=note_uuid)
                for key, value in params.items():
                    setattr(note, f'{key}', value)

                await self.application.objects.update(note)
                re_data = resSuccess('成功')

            except NoteModel.DoesNotExist as e:
                self.set_status(400)
                re_data = resSuccess('失败')
        else:
            self.set_status(400)
            re_data = resSuccess('失败')

        self.finish(json.dumps(re_data, default=json_serial))


class AllNoteHandler(RedisHandler):
    @authenticated_async
    async def post(self, *args, **kwargs):
        """批量操作"""
        re_data = {}
        params = json.loads(self.request.body.decode('utf-8'))
        state = int(params.get('state', 0))
        note_uuid = params.get('note_uuid', [])

        if note_uuid:
            for uuid in note_uuid:
                try:
                    note = await self.application.objects.get(NoteModel, uuid=uuid)

                    if state == 100:
                        note.state = 2
                        await self.application.objects.update(note)

                    elif state == 200:
                        note.state = 1
                        await self.application.objects.update(note)

                    elif state == 300:
                        await self.application.objects.delete(note)

                    re_data = resSuccess('成功')

                except NoteModel.DoesNotExist as e:
                    self.set_status(400)
                    re_data = resSuccess('失败')

        else:
            re_data = resSuccess('失败')

        self.finish(re_data)


class FilterNoteHandler(RedisHandler):
    @authenticated_async
    async def get(self, *args, **kwargs):
        """过滤筛选 项目"""
        state = int(self.get_argument('state', 0))
        current_page = self.get_argument('current_page', 1)
        is_state = False

        try:
            note = NoteModel.select()

            if state == 200:
                state = 2
                is_state = True

            elif state == 300:
                state = 1
                is_state = True

            if is_state:
                note = note.where(NoteModel.state == state)

            note_count = await self.application.objects.count(note)

            note_items = await self.application.objects.execute(
                note.paginate(int(current_page), int(settings['page_size']))
            )

            note_list = []
            for item in note_items:
                project_dict = model_to_dict(item)
                note_list.append(project_dict)

            re_data = resSuccess('成功')
            re_data['result'] = {
                'data': note_list,
                'pagination': {
                    'current_page': current_page,
                    'page_size': int(settings['page_size']),
                    'total': note_count,
                    'total_size': math.ceil(note_count / int(settings['page_size']))
                }
            }

        except NoteModel.DoesNotExist:
            self.set_status(400)
            re_data = resSuccess('失败')

        self.finish(json.dumps(re_data, default=json_serial))
