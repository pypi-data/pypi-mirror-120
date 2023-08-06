from typing import List
from .client_functions import get, post, delete
from .exceptions import SignalBoxException


def create_items_recommender(access_token: str, base_url: str, common_id: str, name: str, default_item_id: str, item_ids: List[str] = None, number_items_to_recommend: int = None):
    json_params = {
        "commonId": common_id,
        "name": name,
        "itemIds": item_ids,
        "defaultItemId": default_item_id,
        "numberOfItemsToRecommend": number_items_to_recommend
    }
    r = post(f'{base_url}/api/recommenders/ItemsRecommenders/',
             json_params, access_token)
    if r.ok:
        return r.json()
    else:
        raise SignalBoxException(r.text)


def get_items_recommender(access_token: str, base_url: str, id):
    r = get(f'{base_url}/api/recommenders/ItemsRecommenders/{id}', access_token)
    if r.ok:
        return r.json()
    else:
        raise SignalBoxException(r.text)


def invoke_items_recommender(access_token: str, base_url: str, id: int, common_user_id: str, arguments: dict = None):
    json_params = {
        "commonUserId": common_user_id,
        "arguments": arguments
    }
    r = post(f'{base_url}/api/recommenders/ItemsRecommenders/{id}/invoke',
             json_params, access_token)
    if r.ok:
        return r.json()
    else:
        raise SignalBoxException(r.text)


def delete_items_recommender(access_token: str, base_url: str, id):
    r = delete(
        f'{base_url}/api/recommenders/ItemsRecommenders/{id}', access_token)
    if r.ok:
        return r.json()
    else:
        raise SignalBoxException(r.text)
