from AuthX.resources.social_messages import get_error_message


class SocialException(Exception):
    _base_url: str

    @classmethod
    def setup(cls, base_url: str) -> None:
        cls._base_url = base_url

    def __init__(self, msg: str, status_code: int, *args):
        self.content = get_error_message(msg, self._base_url)
        self.status_code = status_code
        super().__init__(*args)
