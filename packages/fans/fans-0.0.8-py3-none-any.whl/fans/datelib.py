import datetime

import pytz


timezone = pytz.timezone('Asia/Shanghai')


class Now:

    def isoformat(self):
        return datetime.datetime.now(timezone).isoformat()


now = Now()
