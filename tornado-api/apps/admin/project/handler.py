import json
import math

from playhouse.shortcuts import model_to_dict

from apps.utils.decorators import authenticated_async
from apps.utils.re_data_params import resSuccess
from apps.utils.utils import json_serial
from blog.settings import settings
from blog.handler import RedisHandler

from apps.models.project_models import ProjectModel


class GetProjectHandler(RedisHandler):
    @authenticated_async
    async def get(self, *args, **kwargs):
        """获取项目list"""
        current_page = self.get_argument('current_page', 1)
        try:
            projects = await self.application.objects.execute(
                ProjectModel.select().paginate(int(current_page), int(settings['page_size']))
            )

            project_count = await self.application.objects.count(ProjectModel.select())

            project_list = []
            for project in projects:
                project_dict = model_to_dict(project)
                project_list.append(project_dict)

            re_data = resSuccess('成功')
            re_data['result'] = {
                'data': project_list,
                'pagination': {
                    'current_page': int(current_page),
                    'page_size': int(settings['page_size']),
                    'total': project_count,
                    'total_page': math.ceil(project_count / int(settings['page_size']))
                }
            }

        except ProjectModel.DoesNotExist as e:
            self.set_status(400)
            re_data = resSuccess('失败')

        self.finish(json.dumps(re_data, default=json_serial))


class PutProjectHandler(RedisHandler):
    @authenticated_async
    async def put(self, *args, **kwargs):
        """添加项目"""
        re_data = {}
        params = json.loads(self.request.body.decode('utf-8'))
        try:
            project = await self.application.objects.create(
                ProjectModel, icon=params['icon'], github=params['github'], desc=params['desc'],
                view=params['view'], title=params['title'])

            if project:
                re_data = resSuccess('成功')

        except ProjectModel.DoesNotExist as e:
            self.set_status(400)
            re_data = resSuccess('失败')

        self.finish(re_data)


class DelProjectHandler(RedisHandler):
    @authenticated_async
    async def delete(self, project_uuid, *args, **kwargs):
        """删除项目"""
        if project_uuid:
            try:
                project = await self.application.objects.get(ProjectModel, uuid=project_uuid)
                await self.application.objects.delete(project)

                re_data = resSuccess('成功')
            except ProjectModel.DoesNotExist as e:
                self.set_status(400)
                re_data = resSuccess('失败')
        else:
            self.set_status(400)
            re_data = resSuccess('失败', error='请选择删除的项目')

        self.finish(re_data)


class GetIdProjectHandler(RedisHandler):
    async def get(self, project_uuid, *args, **kwargs):
        """根据ID获取项目"""
        if project_uuid:
            try:
                project = await self.application.objects.get(ProjectModel, uuid=project_uuid)
                project_dict = model_to_dict(project)

                re_data = resSuccess('成功')
                re_data['result'] = project_dict

            except ProjectModel.DoesNotExist as e:
                self.set_status(400)
                re_data = resSuccess('失败')
        else:
            self.set_status(400)
            re_data = resSuccess('失败')

        self.finish(json.dumps(re_data, default=json_serial))


class EditProjectHandler(RedisHandler):
    @authenticated_async
    async def post(self, project_uuid, *args, **kwargs):
        """编辑项目"""
        params = json.loads(self.request.body.decode('utf-8'))

        if not params:
            self.set_status(400)
            re_data = resSuccess('失败')
            self.finish(re_data)

        if project_uuid:
            try:
                project = await self.application.objects.get(ProjectModel, uuid=project_uuid)
                for key, value in params.items():
                    setattr(project, f'{key}', value)

                await self.application.objects.update(project)
                re_data = resSuccess('成功')

            except ProjectModel.DoesNotExist as e:
                self.set_status(400)
                re_data = resSuccess('失败')
        else:
            self.set_status(400)
            re_data = resSuccess('失败')

        self.finish(json.dumps(re_data, default=json_serial))


class AllProjectHandler(RedisHandler):
    @authenticated_async
    async def post(self, *args, **kwargs):
        """批量操作"""
        re_data = {}
        params = json.loads(self.request.body.decode('utf-8'))
        state = int(params.get('state', 0))
        project_uuid = params.get('project_uuid', [])
        if project_uuid:
            for uuid in project_uuid:
                try:
                    project = await self.application.objects.get(ProjectModel, uuid=uuid)

                    if state == 100:
                        project.state = 2
                        await self.application.objects.update(project)

                    elif state == 200:
                        project.state = 1
                        await self.application.objects.update(project)

                    elif state == 300:
                        await self.application.objects.delete(project)

                    re_data = resSuccess('成功')

                except ProjectModel.DoesNotExist as e:
                    self.set_status(400)
                    re_data = resSuccess('失败')

        else:
            re_data = resSuccess('失败')

        self.finish(re_data)


class FilterProjectHandler(RedisHandler):
    @authenticated_async
    async def get(self, *args, **kwargs):
        """过滤筛选 项目"""
        state = int(self.get_argument('state', 0))
        current_page = self.get_argument('current_page', 1)
        is_state = False

        try:
            project = ProjectModel.select()

            if state == 200:
                state = 2
                is_state = True

            elif state == 300:
                state = 1
                is_state = True

            if is_state:
                project = project.where(ProjectModel.state == state)

            project_count = await self.application.objects.count(project)

            project_items = await self.application.objects.execute(
                project.paginate(int(current_page), int(settings['page_size']))
            )

            project_list = []
            for item in project_items:
                project_dict = model_to_dict(item)
                project_list.append(project_dict)

            re_data = resSuccess('成功')
            re_data['result'] = {
                'data': project_list,
                'pagination': {
                    'current_page': current_page,
                    'page_size': int(settings['page_size']),
                    'total': project_count,
                    'total_size': math.ceil(project_count / int(settings['page_size']))
                }
            }

        except ProjectModel.DoesNotExist:
            self.set_status(400)
            re_data = resSuccess('失败')

        self.finish(json.dumps(re_data, default=json_serial))
