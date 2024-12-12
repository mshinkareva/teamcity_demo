import argparse
from datetime import datetime, timedelta

import pytz
from loguru import logger

from one_signal.connect import OneSignalAdapter
from one_signal.models import FlingPush

if __name__ == "__main__":
    one_signal = OneSignalAdapter("")

    parser = argparse.ArgumentParser(description="Example script with argparse.")
    parser.add_argument("--user_external_id", type=str, help="user_external_id", required=True)
    parser.add_argument("--timezone", type=str, help="timezone", required=True)

    args = parser.parse_args()
    user_external_id = args.user_external_id
    timezone = args.timezone

    tz_info =  pytz.timezone(timezone)
    push_time= (datetime.now() + timedelta(minutes=1)).astimezone(tz_info).strftime("%H:%M:%S")

    test_push = [FlingPush(book_id='MarkedJPSina', picture='https://storage.googleapis.com/fling-b827e.appspot.com/Books/MarkedJPSina/90a2fc7c0023de43c4377188ff67c38e377d310e_cover.jpg', text='Dive into 8 new releases, starting with Marked by JP Sina', title='👠 NEW PUSH FROM TC ', user_ids = [f'{user_external_id}'])]
    logger.info(test_push)

    one_signal.upload_pushes(test_push, push_time)
    logger.info('Done')


