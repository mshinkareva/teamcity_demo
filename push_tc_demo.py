import argparse
from datetime import datetime, timedelta

import pytz
from loguru import logger

from one_signal.connect import OneSignalAdapter
from one_signal.models import FlingPush
from one_signal.utils import load_csv_to_model, get_external_ids


one_signal = OneSignalAdapter("")

def make_push(t_zone, external_id):
    tz_info =  pytz.timezone(t_zone)
    push_time= (datetime.now() + timedelta(minutes=2)).astimezone(tz_info).strftime("%H:%M:%S")

    test_push = [FlingPush(book_id='MarkedJPSina', picture='https://storage.googleapis.com/fling-b827e.appspot.com/Books/MarkedJPSina/90a2fc7c0023de43c4377188ff67c38e377d310e_cover.jpg', text='Dive into 8 new releases, starting with Marked by JP Sina', title='👠 NEW PUSH FROM TC ', user_ids = [f'{external_id}'])]
    logger.info(test_push)
    one_signal.upload_pushes(test_push, push_time)
    logger.info('Done')

def save_subscribers():
    url = one_signal.export_subscriptions_to_csv()['csv_file_url']
    subscribers_file = one_signal.download_csv_with_retries(url)
    subscribers_models = load_csv_to_model(subscribers_file)
    with open('subscribers.txt', 'w') as file:
        for subscriber in subscribers_models:
            file.write(f'{subscriber.external_user_id}\n')



if __name__ == "__main__":


    parser = argparse.ArgumentParser(description="Example script with argparse.")
    parser.add_argument("--user_external_id", type=str, help="user_external_id", required=True)
    parser.add_argument("--timezone", type=str, help="timezone", required=True)
    args = parser.parse_args()

    # make_push(args.timezone, args.user_external_id)
    save_subscribers()






