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
MY_FLAT_URL = '{host}/api/v1/listing/'.format(host=API_SERVER_URL)
MY_FLAT_DETAIL_URL = MY_FLAT_URL + '{pk}/'
MY_FLAT_EVENTS_URL = MY_FLAT_DETAIL_URL + 'event/'


def create_example_flat():
    """
    See `create_preflat_example.py` for more details.
    """
    return create_preflat_example.create_pre_listing(
        ref_property=''.join(random.sample(string.ascii_lowercase, 8)),
        ref_house=''.join(random.sample(string.ascii_lowercase, 8)),
        ref_object=''.join(random.sample(string.ascii_lowercase, 8)))


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
    # We just create an example listing to test the event api.
    #
    # If you need the `flat_id` of an existing listing take a look at:
    # `get_listings(status, ref_property, ref_house, ref_object)` in
    # `reate_preflat_example.py`
    flat = create_example_flat()
    send_contract_confirmed_event(flat_id=flat['pk'])
