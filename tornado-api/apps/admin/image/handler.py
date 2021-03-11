import json
import uuid

import aiofiles
import os

from playhouse.shortcuts import model_to_dict

from apps.utils.decorators import authenticated_async
from apps.utils.utils import json_serial
from blog.handler import RedisHandler

from apps.models.image_models import ImageModel


class ImageHandler(RedisHandler):
    @authenticated_async
    async def get(self, *args, **kwargs):
        """获取图片列表"""
        re_data = {}

        try:
            images = await self.application.objects.execute(ImageModel.select().order_by(ImageModel.update_time.desc()))
            re_list = []
            for image in images:
                tag_dict = model_to_dict(image)
                tag_count = await self.application.objects.count(ImageModel.select().where(ImageModel.tag==tag_dict['tag']))
                tag_dict['count'] = tag_count
                tag_dict['tag'] = tag_dict['tag'].split('*')
                re_list.append(tag_dict)

            re_data['code'] = 1
            re_data['message'] = '图片获取成功'
            re_data['result'] = {
                'list': re_list,
            }

        except ImageModel.DoesNotExist as e:
            self.set_status(400)
            re_data['code'] = 0
            re_data['message'] = '查询失败'

        self.finish(json.dumps(re_data, default=json_serial))

    @authenticated_async
    async def post(self, *args, **kwargs):
        """上传图片"""
        re_data = {}

        files_meta = self.request.files.get("files", None)
        tag_meta = self.request.arguments.get('tag', [])
        # tag_meta = self.request.arguments['tag']
        if not files_meta:
            self.set_status(400)
            re_data['code'] = 0
            re_data["message"] = "请上传图片"

        else:
            new_filename = ""
            for meta in files_meta:
                filename = meta["filename"]
                new_filename = "{uuid}_{filename}".format(uuid=str(uuid.uuid1()).replace('-', ''), filename=filename)
                file_path = os.path.join(self.settings["MEDIA_ROOT"], 'images', new_filename)
                async with aiofiles.open(file_path, 'wb') as f:
                    await f.write(meta['body'])

            tag_list = []
            for tag in tag_meta:
                tag_list.append(tag.decode('utf-8'))

            url_path = str(self.settings['IMAGE_URL'] + new_filename)
            await self.application.objects.create(ImageModel, image_name=str(new_filename),
                                                  tag='*'.join(tag_list),
                                                  url_path=url_path)
            re_data['code'] = 1
            re_data['message'] = '上传成功'
            re_data['url_path'] = url_path

        self.finish(re_data)

    @authenticated_async
    async def delete(self, *args, **kwargs):
        """删除图片"""
        re_data = {}

        param = self.request.arguments

        try:
            await self.application.objects.execute(
                ImageModel.delete().where(ImageModel.uuid==param['uuid'][0].decode('utf-8'))
            )
            file_path = os.path.join(self.settings["MEDIA_ROOT"], 'images', param['image_name'][0].decode('utf-8'))
            if os.path.exists(file_path):
                os.remove(file_path)

            re_data['code'] = 1
            re_data['message'] = '删除成功'
        except ImageModel.DoesNotExist as e:
            self.set_status(400)
            re_data['code'] = 0
            re_data['message'] = '删除失败'

        self.finish(re_data)
