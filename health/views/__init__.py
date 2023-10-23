"""Views, one for each health page."""
from health.views.accounts import acc_login, show_chatpage, show_chatuserpage,\
    acc_logout, acc_first_create, acc_second_create, acc_delete, acc_edit, acc_pwd, show_firstpage, show_add
from health.views.check_login import check_login
from health.views.comments_operation import comments_operation
from health.views.explore import explore
from health.views.follow_relation import follow_relation
from health.views.index import show_index
from health.views.like_operation import like_operation
from health.views.new_post import new_post
from health.views.post import post
from health.views.user_followers import user_followers
from health.views.user_following import user_following
from health.views.user_page import user_page
from health.views.uploads import download_file, download_css
