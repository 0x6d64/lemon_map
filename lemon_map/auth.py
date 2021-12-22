# -*- coding: utf-8 -*-

import requests

from .exceptions import LemonAuthException


class LemonAuth:
    def __init__(self):
        self.token = None
        self.phone_number = None

    def request_otp_by_phone(self):
        api_request = requests.get(
            "https://web-production.lime.bike/api/rider/v1/login", data={"phone": self.phone_number}
        )
        if not api_request.ok:
            raise LemonAuthException(
                "error requesting OTP: Response {}, {}".format(
                    api_request.status_code, api_request.content
                )
            )

    def provide_otp(self):
        pass


if __name__ == "__main__":
    pass
