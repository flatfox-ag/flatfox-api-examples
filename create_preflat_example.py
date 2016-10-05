# -*- coding: utf-8 -*-
import requests
import utils
import base64


# -----------------------------------------------------------------------------
# API CONFIG
# NB: Our API uses HTTP Basic Auth. You have to use the API key as username and
#     leave the password blank for each request.
# -----------------------------------------------------------------------------
API_SERVER_URL = 'https://flatfox.ch'
API_KEY = 'sk_xxxxxxxxxxxxxxxxxxxxxx'


# -----------------------------------------------------------------------------
# API ENDPOINTS
# -----------------------------------------------------------------------------
MY_FLAT_URL = '{host}/api/v1/my-flat/'.format(host=API_SERVER_URL)
MY_FLAT_APPLY_PDF_URL = '{host}/api/v1/my-flat/{pk}/apply-cards-pdf/'


def create_pre_flat():
    """
    Example of how to create a pre-flat.

    For all possible values see:
    https://flatfox.ch/api-docs/#!/my-flat/My_Flat_POST

    NB: Keep in mind: only one active flat with the same ref_property,
        ref_house and ref_object can exist.
    """
    data = {
        "status": "pre",

        "ref_property": "12",
        "ref_house": "23",
        "ref_object": "39",

        "street": "Uetlibergstrasse",
        "street_number": "129",
        "zipcode": "8045",
        "city": u"Zürich",

        "floor": None,
        "number_of_rooms": "3.0",
        "rent_charges": 100,
        "rent_gross": 2070
    }
    r = requests.post(MY_FLAT_URL, auth=(API_KEY, ''), data=data)
    utils.print_response(r)
    return r.json()


def get_apply_pdf(flat_pk):
    """
    Get apply pdf with newly created flat pk.
    The endpoint returns a JSON with a pdf field which contains a base64
    encoded pdf file:

        {
            "pdf": "JVBERi0xLjUKJbXtrvsKMyAwIG9iago8PCAvTGVuZ3RoIDQg...",
        }

    """
    url = MY_FLAT_APPLY_PDF_URL.format(host=API_SERVER_URL, pk=flat_pk)
    r = requests.get(url, auth=(API_KEY, ''), stream=True)
    content = base64.b64decode(r.json()['pdf'])

    filename = '{pk}_apply_form.pdf'.format(pk=flat_pk)
    with open(filename, 'wb') as out_file:
        out_file.write(content)
    del r


if __name__ == "__main__":
    # First create a pre-flat
    flat = create_pre_flat()

    # Then get the apply pdf
    get_apply_pdf(flat_pk=flat['pk'])

    # Now a file named apply_form.pdf should be created
    # next to this script
