from .client_functions import get, post
from .exceptions import SignalBoxException


def create_recommender_target_variable_value(access_token: str, base_url: str, recommender_api_name: str, id: int, start, end, name: str, value: float):
    json_params = {
        "start": start,
        "end": end,
        "name": name,
        "value": value,
    }
    r = post(f'{base_url}/api/recommenders/{recommender_api_name}/{id}/TargetVariableValues',
             json_params, access_token)
    if r.ok:
        return r.json()
    else:
        raise SignalBoxException(r.text)


def get_recommender_target_variable_values(access_token: str, base_url: str, recommender_api_name: str, id: int, name: str = None):

    r = get(f'{base_url}/api/recommenders/{recommender_api_name}/{id}/TargetVariableValues?name={name if name is not None else ""}', access_token)
    if r.ok:
        return r.json()
    else:
        raise SignalBoxException(r.text)
