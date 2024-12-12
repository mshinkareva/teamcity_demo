import os

import requests
import json
from loguru import logger


class OneSignalAdapter:

    def __init__(self, settings):
        self.settings = settings
        self.auth_key = os.getenv("ONE_SIGNAL_AUTH_KEY")
        self.app_id = os.getenv("ONE_SIGNAL_APP_ID")

    def upload_pushes(self, pushes, delivery_time_of_day="15:00:00"):
        for push in pushes:
            header = {"Content-Type": "application/json; charset=utf-8",
                      "Authorization": "Basic " + self.auth_key}

            payload = {"app_id": self.app_id,
                       "include_external_user_ids": push.user_ids,
                       "channel_for_external_user_ids": "push",
                       "headings": {"en": push.title},
                       "contents": {"en": push.text},
                       "large_icon": push.picture,
                       "delayed_option": "timezone",
                       "delivery_time_of_day": delivery_time_of_day,
                       "app_url": "https://app.flingfm.com/book/" + push.book_id}

            logger.info(f'{payload}')


            req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
            logger.info(f'{req.status_code} {req.status_code} {req.text}')
