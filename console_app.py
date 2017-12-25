# coding:utf-8
import os
import sys
import platform
from core.base import FestivalHead
if __name__ == "__main__":
    ori_pic_path = sys.argv[1]
    o = FestivalHead()
    result_pic = o.gen(ori_pic_path)
    print "Result:"
    print "relpath:",result_pic
    print "abspath:",os.path.abspath(result_pic)
    os_type = platform.system()
    if os_type == "Linux":
        cmd = "xdg-open %s" % result_pic
    elif os_type == "Windows":
        cmd = "mspaint %s" % result_pic
    else:
        cmd = "open %s" % result_pic
    try:
        os.system(cmd)
    except Exception:
        pass
