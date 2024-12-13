import os
import time

import requests
import json
from loguru import logger

DOWNLOAD_PATH = os.path.join(os.getcwd(), "downloaded_file.csv.gz")


class OneSignalAdapter:

    def __init__(self, settings):
        self.settings = settings
        self.auth_key = os.getenv("ONE_SIGNAL_AUTH_KEY")
        self.app_id = os.getenv("ONE_SIGNAL_APP_ID")
        self.base_url = "https://onesignal.com/api/v1"
        self.headers = {"Content-Type": "application/json; charset=utf-8",
                        "Authorization": f"Basic {self.auth_key}"}

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

    def export_subscriptions_to_csv(self):
        url = f"{self.base_url}/players/csv_export?app_id={self.app_id}"
        payload = {
            "app_id": self.app_id,
            "extra_fields": ["external_user_id", "unsubscribed_at"],
            "last_active_since": int(os.getenv("LAST_ACTIVE_SINCE", "0")),  # UNIX timestamp
            "segment_name": "Subscribed Users"
        }

        self.headers.update({"accept": "application/json"})
        response = requests.post(url, headers=self.headers, json=payload)
        logger.info(f'{response.status_code} {response.text}')
        return response.json()

    def download_csv_with_retries(self, url, download_path=DOWNLOAD_PATH, max_retries=5, backoff_factor=3):
        retries = 0
        while retries < max_retries:
            try:
                with requests.get(url, stream=True) as response:
                    if response.status_code == 200:
                        logger.info(f"Начнется скачивание {download_path}")
                        with open(download_path, "wb") as f:
                            for chunk in response.iter_content(chunk_size=8192):
                                f.write(chunk)
                        logger.info(f"Файл успешно скачан: {download_path}")
                        return download_path
                    elif response.status_code == 404:
                        logger.warning(f"Файл еще не готов. Попытка {retries + 1}/{max_retries}.")
                    else:
                        logger.error(f"Ошибка при скачивании файла: {response.status_code}, {response.text}")
            except requests.exceptions.RequestException as e:
                logger.error(f"Ошибка сети: {e}")

            retries += 1
            sleep_time = backoff_factor ** retries
            logger.info(f"Ждем {sleep_time} секунд перед повторной попыткой.")
            time.sleep(sleep_time)





