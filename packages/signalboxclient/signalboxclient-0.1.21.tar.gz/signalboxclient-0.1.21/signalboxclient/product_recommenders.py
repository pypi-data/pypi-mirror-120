from typing import List
from .client_functions import get, post, delete
from .exceptions import SignalBoxException
from .target_variables import create_recommender_target_variable_value, get_recommender_target_variable_values


def create_product_recommender(access_token: str, base_url: str, common_id: str, name: str, product_ids: List[str] = None):
    json_params = {
        "commonId": common_id,
        "name": name,
        "productIds": product_ids
    }
    r = post(f'{base_url}/api/recommenders/ProductRecommenders/',
             json_params, access_token)
    if r.ok:
        return r.json()
    else:
        raise SignalBoxException(r.text)


def get_product_recommender(access_token: str, base_url: str, id):
    r = get(f'{base_url}/api/recommenders/ProductRecommenders/{id}', access_token)
    if r.ok:
        return r.json()
    else:
        raise SignalBoxException(r.text)


def invoke_product_recommender(access_token: str, base_url: str, id: int, common_user_id: str):
    json_params = {
        "commonUserId": common_user_id
    }
    r = post(f'{base_url}/api/recommenders/ProductRecommenders/{id}/invoke',
             json_params, access_token)
    if r.ok:
        return r.json()
    else:
        raise SignalBoxException(r.text)


def get_parameterset_recommender(access_token: str, base_url: str, id):
    r = delete(
        f'{base_url}/api/recommenders/ProductRecommenders/{id}', access_token)
    if r.ok:
        return r.json()
    else:
        raise SignalBoxException(r.text)


def delete_product_recommender(access_token: str, base_url: str, id):
    r = delete(
        f'{base_url}/api/recommenders/ProductRecommenders/{id}', access_token)
    if r.ok:
        return r.json()
    else:
        raise SignalBoxException(r.text)


def create_target_variable_value(access_token: str, base_url: str, id: int, start, end, name: str, value: float):
    return create_recommender_target_variable_value(access_token, base_url, "ProductRecommenders", id, start, end, name, value)


def get_target_variable_values(access_token: str, base_url: str, id: int,  name: str = None):
    return get_recommender_target_variable_values(access_token, base_url, "ProductRecommenders", id, name)
