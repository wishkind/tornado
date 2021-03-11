import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from apps.models.image_models import ImageModel
from apps.models.article_models import ArticleModel
from apps.models.tag_models import TagModel
from apps.models.user_models import UserModel
from apps.models.comment_models import CommentModel, CommentInfoModel
from apps.models.reply_models import ReplyInfoModel, ReplyModel, ReplyCommentInfoModel
from apps.models.hero_models import HeroModels, HeroInfoModels
from apps.models.project_models import ProjectModel
from apps.models.note_models import NoteModel
from blog.settings import database


def init():
    # 生成表
    database.create_tables([NoteModel])


def test():
    user = UserModel.get()
    user.save()


if __name__ == "__main__":
    # test()
    init()
