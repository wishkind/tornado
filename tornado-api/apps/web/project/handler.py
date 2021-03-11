import json

from playhouse.shortcuts import model_to_dict

from apps.utils.re_data_params import resSuccess
from apps.utils.utils import json_serial
from blog.handler import RedisHandler

from apps.models.project_models import ProjectModel


class GetProjectHandler(RedisHandler):
    async def get(self, *args, **kwargs):
        """获取项目list"""

        try:
            projects = await self.application.objects.execute(ProjectModel.select())

            project_list = []
            for project in projects:
                project_dict = model_to_dict(project)
                project_list.append(project_dict)

            re_data = resSuccess('成功')
            re_data['list'] = project_list

        except ProjectModel.DoesNotExist as e:
            self.set_status(400)
            re_data = resSuccess('失败')

        self.finish(json.dumps(re_data, default=json_serial))
