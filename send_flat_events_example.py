# -*- coding: utf-8 -*-
import requests
import utils
import string
import random

import create_preflat_example


# -----------------------------------------------------------------------------
# API CONFIG
# NB: Our API uses HTTP Basic Auth. You have to use the API key as username and
#     leave the password blank for each request.
# -----------------------------------------------------------------------------
API_SERVER_URL = 'https://stage.flatfox.ch'
API_KEY = 'sk_xxxxxxxxxxxxxxxxxxxxxx'


# -----------------------------------------------------------------------------
# API ENDPOINTS
# -----------------------------------------------------------------------------
MY_FLAT_URL = '{host}/api/v1/my-flat/'.format(host=API_SERVER_URL)
MY_FLAT_DETAIL_URL = MY_FLAT_URL + '{pk}/'
MY_FLAT_EVENTS_URL = MY_FLAT_DETAIL_URL + 'events/'


def create_example_flat():
    """
    See `create_preflat_example.py` for more details.
    """
    advertiser_id = create_preflat_example.get_advertiser_id(name="Silvan Spross")
    return create_preflat_example.create_pre_listing(
        advertiser_id=advertiser_id,
        ref_property=''.join(random.sample(string.ascii_lowercase, 8)),
        ref_house=''.join(random.sample(string.ascii_lowercase, 8)),
        ref_object=''.join(random.sample(string.ascii_lowercase, 8)))


# def delete_listing(listing_pk):
#     """
#     ATTENTION (2018-04-19): This feature is not working atm.

#     A listing may be deleted by setting its state to "rem" on its detail URL.
#     A deleted listing may still be queried (e.g., using get_listings(status='rem'))
#     though, but it may not be changed afterwards, nor will it be visible on the
#     portal, except for advertisers.
#     """
#     url = MY_FLAT_DETAIL_URL.format(pk=listing_pk)
#     data = {
#         "status": "rem",
#     }
#     r = requests.patch(url, auth=(API_KEY, ''), json=data)
#     utils.print_response(r)
#     r.raise_for_status()


def send_contract_confirmed_event(flat_id):
    """
    Example of how to send a contract confirmed listing event.

    NB: This should be used if a contract was activated, but you can not tell
        flatfox which specific applicant it was. So in other words, if you can
        not use `choose_applicant_example.py`
    """
    url = MY_FLAT_EVENTS_URL.format(pk=flat_id)
    data = {"event": "CONTRACT_CONFIRMED"}

    r = requests.post(url, auth=(API_KEY, ''), json=data)
    utils.print_response(r)
    return r.json()


if __name__ == "__main__":
    flat = create_example_flat()
    send_contract_confirmed_event(flat_id=flat['pk'])
