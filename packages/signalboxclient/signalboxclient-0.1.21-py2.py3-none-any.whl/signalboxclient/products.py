from .client_functions import get, post
from .pagination import pageQuery, PaginatedResponse
from .exceptions import SignalBoxException


def create_product(access_token: str, base_url: str, common_id: str, name: str, list_price: float, direct_cost: float, description: str):
    json_params = {
        "commonId": common_id,
        "name": name,
        "listPrice": list_price,
        "directCost": direct_cost,
        "description": description,
    }
    r = post(f'{base_url}/api/products',
             json_params, access_token)
    if r.ok:
        return r.json()
    else:
        raise SignalBoxException(r.text)


def query_products(access_token: str, base_url: str, page: int = None):
    r = get(f'{base_url}/api/products?{pageQuery(page)}', access_token)
    if r.ok:
        return PaginatedResponse(**r.json())
    else:
        raise SignalBoxException(r.text)
