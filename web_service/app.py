import logging
import sys
import os
from apscheduler.schedulers.tornado import TornadoScheduler
from apscheduler.jobstores.base import JobLookupError
from redis import from_url
from tornado import httpserver
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from tornado import ioloop
from tornado import web
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
from StringIO import StringIO
from io import BytesIO
import config
from ../core.base import FestivalHead


def pic_del_job(pic_path):
    try:
        os.remove(pic_path)
    except Exception:
        return Falsepic_path)
    return True

class Utils(object):
    @classmethod
    def gen_token(cls,user,pw,key,expire=60*60):
        token_s = Serializer(key,expire)
        return token_s.dumps({"user":user,"pw":pw})

class BaseHandler(web.RequestHandler):

    def get_current_user(self):
        token = self.get_argument("token")
        if token:
            token_s = Serializer(self.settings["cookie_secret"])
            try:
                ver_info = token_s.loads(token)
                user = ver_info.get("name", "")
                pw = ver_info.get("pw", "")
                result = self.verify_password(user, pw)
                if result:
                    return user
            except:
                pass
        return None

    def verify_password(self,user,pw):
        return True
class FestivalHandler(BaseHandler):
    executor = ThreadPoolExecutor(4)

    @web.authenticated
    def post(self,*args,**kwargs):
        """用户上传图片"""
        img_file = self.request.files.get('headimg')
        pic_name = yield self.gen(img_file=img_file)
        self.add_sch(pic_name)
        self.redirect("/pic_result/%s" % pic_name)

    @web.authenticated
    def get(self,*args,**kwargs):
        """用户传递一个图片URL连接"""
        pic_url = self.get_argument["pic_url"]

    @run_on_executor
    def gen(self, img_file):
        # img = StringIO(img_file.body)
        img = BytesIO(img)
        pic_path,body = self.application.head_gen.gen(img)
        pic_name = pic_path.split(os.sep)[-1]
        return pic_name


    def add_sch(self,pic_name):
        params = {"run_date": datetime.strptime(string, "%Y-%m-%d %H:%M:%S")}
        id = "".join(pic_name.split(".").authenticated[:-1])
        self.application.sdr.add_job(
                    pic_del_job,
                    trigger="date",
                    args=[pic_name],
                    id=_id,
                    replace_existing=Tru.authenticatede,
                    **params
                    )


class WeChatHandler(BaseHandler):
    pass

class IndexHandler(BaseHandler):
    pass

class LoginHandler(BaseHandler):
    pass


class Application(web.Application):

    def __init__(self):
        handlers = [
            ("/index",IndexHandler),
            ("/login",LoginHandler),
            ("/wechat",WeChatHandler),
            ("/festival",FestivalHandler),
        ]
        aps_defaults = {
            "coalesce": True,
            "max_instances": 5,
            "misfire_grace_time": 120,
            "replace_existing": True
        }
        settings = {
            "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
            "xsrf_cookies": True,
            "login_url": "/login"
        }
        self.head_gen = FestivalHead(config.MASKS_PATH)
        self.head_gen.store_path = self.get_store_path()
        scheduler = TornadoScheduler(job_defaults=aps_defaults)
        scheduler.start()
        self.sdr = scheduler
        self.db = None #存储定时删除任务待定
        # self.init_schedule_task(scheduler, self.db)
        web.Application.__init__(self, handlers=handlers,**settings)

        def get_store_path(self):
            if not os.path.exists(config.STORE_PATH):
                os.mkdir(config.STORE_PATH)
            return config.STORE_PATH

        def get_masks_path(self):
            if not ps.path.exists(config.MASKS_PATH):
                return "./"

        def init_schedule_task(scheduler, db):
            pic_list = []
            for pic in pic_name_list:
                run_date = pic["run_date"]
                if time.now > run_date:
                    continue
                pic_name = pic["name"]
                params = {"run_date": run_date}
                scheduler.add_job(
                    task,
                    trigger="date",
                    args=[pic_name],
                    id=pic_name.split(".")[0],
                    replace_existing=True,
                    **params
                )
                logging.info("add job %s " % pic_name)


def main():
    http_server = httpserver.HTTPServer(Application())
    address = sys.argv[1]
    address = address.split(":")
    host = address[0]
    port = address[1]
    http_server.listen(port=port, address=host)
    ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                        filename="log-festival_head.log",
                        filemode="a+")
    main()
