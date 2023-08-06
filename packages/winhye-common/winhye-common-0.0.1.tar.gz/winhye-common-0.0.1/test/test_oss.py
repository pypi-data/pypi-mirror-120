import os
import sys

PATH = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)), "src")
sys.path.append(PATH)
print(PATH)

from winhye_common.utils.oss_base import OssBucket


def test_oss():
    oss_config = {
        "AccessKey_ID": "LTAI5tFbpMr1R4CVCbUePMWy",
        "AccessKey_Secret": "MJ2WWUbIKDg4UY5EbEsgQ983Lkfwff",
        "endpoint": "oss-cn-beijing.aliyuncs.com",
        "bucket_name": "winhye-kaifa"
    }
    oss_conn = OssBucket(
        oss_config["AccessKey_ID"],
        oss_config["AccessKey_Secret"],
        oss_config["endpoint"],
        oss_config["bucket_name"]
    )
    url = oss_conn.get_url("alarm_3/前方道路已开通请做好行驶准备.mp3", expires=1000)
    print(f"url: {url}")


if __name__ == '__main__':
    test_oss()
