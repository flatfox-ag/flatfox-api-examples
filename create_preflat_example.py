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
EMPLOYEE_LOOKUP_URL = '{host}/api/v1/employee/'.format(host=API_SERVER_URL)


def get_advertiser_id(name):
    """
    Example how to look up an employee by email or name.
    Goal is to get the employees user ID to use as advertiser for the pre flat.

    The endpoint /api/v1/employee/ takes `fuzzy_name` OR `email` address as
    filter attribute. The result would look like this:

        [
            {
              "pk": 9012,
              "dossier_pk": 31777,
              "first_name": "Silvan",
              "last_name": "Spross",
              "name": "Silvan Spross",
              "avatar_url": "/media/images/26fae47e85ale.jpg",
              "avatar_color": null,
              "organization": null,
              "num_applications": {
                "total": 10,
              },
              "phone_number": "079 393 92 12",
              "email": "silvan.spross@flatfox.ch"
            },
            ...
        ]

    """
    r = requests.get(EMPLOYEE_LOOKUP_URL, auth=(API_KEY, ''), params={
        'fuzzy_name': name,  # Or for exact matches only: 'email': email,
    })
    utils.print_response(r)
    return r.json()[0]['pk']


def get_existing_pre_flat():
    """
    Example how to get an already existing pre flat.

    We add query parameters to the my-flat-list api to filter by ref and
    status like:

        /api/v1/my-flat/?ref_property=12&ref_house=23&ref_object=39&status=pre

    """
    params = {
        "status": "pre",
        "ref_property": "12",
        "ref_house": "23",
        "ref_object": "39",
    }
    r = requests.get(MY_FLAT_URL, auth=(API_KEY, ''), params=params)
    utils.print_response(r)

    if r.json()['count'] > 0:
        return r.json()['results'][0]

    return None


def create_pre_flat(advertiser_id):
    """
    Example of how to create a pre-flat.

    For all possible values see:
    https://flatfox.ch/api-docs/#!/my-flat/My_Flat_POST

    NB: Keep in mind: only one active flat with the same ref_property,
        ref_house and ref_object can exist.
    """
    data = {
        "status": "pre",

        # unique for active flats (status in pre, pub, dis)
        "ref_property": "12",
        "ref_house": "23",
        "ref_object": "39",

        # required fields
        "street": "Uetlibergstrasse 129",
        "zipcode": "8045",
        "city": u"Zürich",

        # advertisers takes a list of objects with a pk
        "advertisers": [
            {"pk": advertiser_id}
        ],

        # optional fields
        # "year_built": 1995,
        # "floor": None,
        # "number_of_rooms": "3.0",
        # "rent_charges": 100,
        # "rent_gross": 2070
    }
    r = requests.post(MY_FLAT_URL, auth=(API_KEY, ''), json=data)
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

    # Default language is English, this example shows how to get the apply
    # card PDF in German
    headers = {"Accept-Language": "de"}
    r = requests.get(url, auth=(API_KEY, ''), headers=headers)
    content = base64.b64decode(r.json()['pdf'])

    filename = '{pk}_apply_form.pdf'.format(pk=flat_pk)
    with open(filename, 'wb') as out_file:
        out_file.write(content)
    del r


if __name__ == "__main__":
    # First we check if a preflat already exists
    flat = get_existing_pre_flat()

    # If not, we look up the employee ID and create a pre-flat
    if not flat:
        advertiser_id = get_advertiser_id(name="Silvan Spross")
        flat = create_pre_flat(advertiser_id=advertiser_id)

    # Then get the apply pdf
    get_apply_pdf(flat_pk=flat['pk'])

    # Now a file named ####_apply_form.pdf should be created
    # next to this script
