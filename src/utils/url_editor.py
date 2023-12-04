from typing import Iterable, Union, Dict, Literal
from urllib.parse import urlparse, parse_qs, urlencode


def unparse_qs(qs: Dict[str, str]):
    """
    {'q': ['패딩'], 'a': ['ss']} -> q=패딩&a=ss
    """
    return "&".join(
        ["&".join(map(lambda x: f"{key}={x}", qs[key])) for key in qs.keys()]
    )


def encode_query_params(url: str, __params_to_encode: Union[str, Iterable[str]]):
    """
    특정 params를 인코딩한 url을 return
    """
    parsed_url = urlparse(url)
    qs = parse_qs(parsed_url.query)
    not_encoded_qs = {
        key: qs[key] for key in qs.keys() if key not in __params_to_encode
    }
    encoded_qs = {key: qs[key] for key in qs.keys() if key in __params_to_encode}

    return f"{url.split('?')[0]}?{'&'.join([unparse_qs(not_encoded_qs), urlencode(encoded_qs)])}"


def remove_query_params(url: str, __params_to_remove: Union[str, Iterable[str]]):
    """
    특정 params를 제거한 url을 return
    """

    # 키워드가 하나만 들어왔을 경우 리스트로 감싸기
    if isinstance(__params_to_remove, str):
        __params_to_remove = [__params_to_remove]

    parsed_url = urlparse(url)
    qs = parse_qs(parsed_url.query)
    new_qs = {key: qs[key] for key in qs.keys() if key not in __params_to_remove}

    return f"{url.split('?')[0]}?{unparse_qs(new_qs)}"
