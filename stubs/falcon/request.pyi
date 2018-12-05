from typing import Dict


class Request:
    params: Dict[str, str]

class RequestOptions:
    auto_parse_form_urlencoded: bool = ...
