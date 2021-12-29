# -*- coding: utf-8 -*-

import json

import requests

from lemon_map.exceptions import LemonAuthException
from api_helper import LIME_API_BASE_URL


class LemonAuth:
    def __init__(self):
        self.token = None
        self.phone_number = None

    @classmethod
    def from_token_file(cls, token_file):
        new_cls = cls()
        with open(token_file) as a_fp:
            auth_data = json.load(a_fp)
        new_cls.token = auth_data.get("token")
        new_cls.phone_number = auth_data.get("phone_number")
        return new_cls

    def write_to_token_file(self, token_file):
        data = {
            "token": self.token,
            "phone_number": self.phone_number,
        }
        with open(token_file, "w") as a_fp:
            json.dump(data, a_fp, indent=2)

    def request_otp_by_phone(self, phone_number=None):
        if phone_number:
            self.phone_number = phone_number
        api_request = requests.get(
            LIME_API_BASE_URL + "/rider/v1/login", data={"phone": self.phone_number}
        )
        if not api_request.ok:
            raise LemonAuthException(
                "error requesting OTP: Response {}, {}".format(
                    api_request.status_code, api_request.content
                )
            )

    def provide_otp(self, otp):
        if not self.phone_number:
            raise LemonAuthException("cannot provide OTP without phone number!")

        api_request = requests.post(
            LIME_API_BASE_URL + "/rider/v1/login",
            json={"login_code": otp, "phone": self.phone_number},
        )
        if not api_request.ok:
            raise LemonAuthException(
                "error requesting OTP: Response {}, {}".format(
                    api_request.status_code, api_request.content
                )
            )
        data = json.loads(api_request.content)
        self.token = data.get("token")


if __name__ == "__main__":
    pass
