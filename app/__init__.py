from .blog_app import app
from . import views  # 这里必须import views一下，不然views这里不运行

from .views.tm_views import tm

app.register_blueprint(tm, url_prefix='/tm')
