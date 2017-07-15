# encoding: utf-8

oss1 = dict(accessKeyId='6MKOqxGiGU4AUk44', accessKeySecret='ufu7nS8kS59awNihtjSonMETLI0KLy',
            host='http://post-test.oss-cn-hangzhou.aliyuncs.com', expire_time=30,
            upload_dir='user-dir/',
            callback_url="http://oss-demo.aliyuncs.com:23450",
            )
oss_data = {'user-dir': oss1,
            }

# from settings_local reload config
try:
    from settings_local import *
except ImportError:
    pass
