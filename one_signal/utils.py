import pandas as pd

from one_signal.models import Subscription


def load_csv_to_model(csv_path)->set[Subscription]:
    df = pd.read_csv(csv_path)
    df = df.where(pd.notnull(df), None)
    return {Subscription(**row.to_dict()) for _, row in df.iterrows()}


def get_external_ids(csv_path):
    models = load_csv_to_model(csv_path)
    return {model.external_user_id for model in models}