# -*- coding: utf-8 -*-
import requests
import utils
import base64
import string
import random


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
MY_FLAT_APPLY_PDF_URL = MY_FLAT_DETAIL_URL + 'flyer/'


def get_listings(status, ref_property, ref_house, ref_object):
    """
    Example how to get an already existing listing.

    We add query parameters to the my-flat-list api to filter by ref and
    status like:

        /api/v1/my-flat/?ref_property=12&ref_house=23&ref_object=39&status=pre

    """
    params = {
        "status": status,
        "ref_property": ref_property,
        "ref_house": ref_house,
        "ref_object": ref_object,
    }
    r = requests.get(MY_FLAT_URL, auth=(API_KEY, ''), params=params)
    utils.print_response(r)

    return [listing['pk'] for listing in r.json()['results']]


def get_existing_listings(ref_property, ref_house, ref_object):
    return (
        get_listings("pre", ref_property, ref_house, ref_object) +
        get_listings("act", ref_property, ref_house, ref_object) +
        get_listings("dis", ref_property, ref_house, ref_object))


def create_pre_listing(ref_property, ref_house, ref_object):
    """
    Example of how to create a pre-flat.

    NB: Keep in mind: only one active flat with the same ref_property,
        ref_house and ref_object can exist.
    """
    data = {
        "status": "pre",

        # unique for active flats (status in pre, pub, dis)
        "ref_property": ref_property,
        "ref_house": ref_house,
        "ref_object": ref_object,

        # required fields
        "street": "Uetlibergstrasse 129",
        "zipcode": "8045",
        "city": u"Zürich",

        # the responsible role(s) / employee(s) within Flatfox:
        # role choices are:
        # - manager (Bewirtschafter)
        # - lessor (Vermieter)
        # - assistant (Assistent)
        # - field_representative (Aussendienstmitarbeiter)
        # - vacancy_manager (Leerstandsmanager)
        # - facility_manager (Hauswart)

        "roles": [{
            "role": "manager",
            "name": "Silvan Spross",
            "phone": "+41 44 111 22 34",
            "email": "silvan.spross@flatfox.ch"
        }],

        # Optional fields:
        #
        # "year_built": 1995,
        # "floor": None,
        # "number_of_rooms": "3.0",
        # "rent_charges": 100,
        # "rent_gross": 2070
        # "language": "fr",

        # Optional agency fields:
        # This fields are used for statistics and to control the contact
        # row information in the application form flyer. Usually the same public
        # information is used as in an IDX export.
        #
        # "agency_reference": "Silvan Spross",
        # "agency_phone": "+41 44 111 22 33",
        # "agency_name": 'Verwaltung AG',
        # "agency_name2": 'c/o',
        # "agency_street": 'Husacherstrasse 3',
        # "agency_zipcode": '8304',
        # "agency_city": 'Wallisellen',
        # "agency_country": 'ch',
        # "agency_email": "info@verwatung.ch",
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
    url = MY_FLAT_APPLY_PDF_URL.format(pk=flat_pk)

    # Default language is English, this example shows how to get the apply
    # card PDF in German
    headers = {"Accept-Language": "de"}
    r = requests.get(url, auth=(API_KEY, ''), headers=headers)
    pdfBase64 = r.json().get('pdf')
    if pdfBase64:
        content = base64.b64decode(pdfBase64)
        filename = '{pk}_apply_form.pdf'.format(pk=flat_pk)
        with open(filename, 'wb') as out_file:
            out_file.write(content)
        del r


if __name__ == "__main__":
    # Create random property, house and object references to hopefully not
    # clash with existing ones.
    ref_property = ''.join(random.sample(string.ascii_lowercase, 8))
    ref_house = ''.join(random.sample(string.ascii_lowercase, 8))
    ref_object = ''.join(random.sample(string.ascii_lowercase, 8))

    # If not, we create the listing
    flat = create_pre_listing(
        ref_property=ref_property,
        ref_house=ref_house,
        ref_object=ref_object)

    # Then get the apply pdf
    get_apply_pdf(flat_pk=flat['pk'])

    # Now a file named ####_apply_form.pdf should be created
    # next to this script
