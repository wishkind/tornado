from apps.web.article.urls import url_pattern as article_urls
from apps.web.tags.urls import url_pattern as tag_urls
from apps.web.comment.urls import url_pattern as comment_urls
from apps.web.reply.urls import url_pattern as reply_urls
from apps.web.hero.urls import url_pattern as hero_urls
from apps.web.project.urls import url_pattern as project_urls
from apps.web.note.urls import url_pattern as note_urls

url_pattern = ()

url_pattern += article_urls
url_pattern += tag_urls
url_pattern += comment_urls
url_pattern += reply_urls
url_pattern += hero_urls
url_pattern += note_urls
url_pattern += project_urls
