# upload_aliyunoss
# server
pip install -r requirements.txt
python my_oss_token_upload.py

# get token for floor
http://localhost:8080/token/floor

# test upload to aliyun oss
http://localhost:8080/testoss/floor


# server for callback
callback server should be in an internet site.
run :
    python callback_app_server.py 

app server, run:     
python test_oss_token_upload_callback.py

maybe you need to change callback url, the default is davidzhang.xin which can not be ready.
you can define you own oss_data in setting_local.py

