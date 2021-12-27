# -*- coding: utf-8 -*-
import argparse
import logging
import sys

import lemon_map

config = lemon_map.LemonConfig.get_default_config()
logger = logging.getLogger(__name__)


def get_parser():
    new_parser = argparse.ArgumentParser()
    new_parser.add_argument("--auth", help="start dialog to setup auth data", action="store_true")
    new_parser.add_argument("--config_file", help="path to config file")
    return new_parser


def setup_auth():
    print("let's get an auth token by requesting an OTP on your mobile phone...")
    auth_file_destination = input(
        "where should the auth file saved? [{}] ".format(config.get("DEFAULT", "auth_file"))
    )
    phone_no = input("please enter your phone number in the format +xxxxx: ")
    auth = lemon_map.LemonAuth()
    try:
        auth.request_otp_by_phone(phone_number=phone_no)

        otp = input("please input the received OTP: ")
        auth.provide_otp(otp)
        if auth.token:
            print("Success, writing data to token file")
            auth.write_to_token_file(auth_file_destination)
    except lemon_map.LemonAuthException as ex:
        logger.error("something went wrong: %s", ex)


def run_main(args):
    ret_val = 0
    config_to_load = (
        args.config_file if args.config_file else lemon_map.LemonConfig.DEFAULT_CONFIG_FILE
    )
    config = lemon_map.LemonConfig().from_file(config_to_load)

    if args.auth:
        setup_auth()
    return ret_val


if __name__ == "__main__":
    parser = get_parser()
    parsed_args = parser.parse_args()
    exit_code = run_main(parsed_args)
    sys.exit(exit_code)
