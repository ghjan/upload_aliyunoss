# upload_aliyunoss
# server
pip install -r requirements.txt
python my_oss_token_upload.py

# get token for floor
http://localhost:8080/token/floor

# test upload to aliyun oss
http://localhost:8080/testoss/floor


# server for callback
python test_oss_token_upload_callback.py
#maybe you need to change callback url, the default is davidzhang.xin which can not be ready.
