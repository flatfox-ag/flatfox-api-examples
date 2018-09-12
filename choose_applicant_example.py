# -*- coding: utf-8 -*-
import requests
import utils


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
APPLICATION_API_URL = '{host}/api/v1/application/{pk}/'


def choose_specific_applicant(pk):
    """
    Example how to choose an applicant for a flat. All you need is
    an application pk.
    """
    data = {
        "status": "chos",

        # Meta data is optional. You can store additional, structured
        # information on this application and we will provide it to every other
        # webhook event where this application is involved. E.g. the
        # `applicant_chosen` event, which is often consumed by central storage
        # systems.
        "metadata": {
            "mykey": "my value",
            "anotherkey": "another value",
        },
    }
    url = APPLICATION_API_URL.format(host=API_SERVER_URL, pk=pk)
    r = requests.patch(url, auth=(API_KEY, ''), json=data)
    utils.print_response(r)
    return r.json()


if __name__ == "__main__":
    # To choose an applicant, you need the pk from his application.
    # The push_dossier event from the event examples (webhook push/postbox)
    # contains the application with the pk and an endpoint url for more details:
    #
    # {
    #   "type": "push_dossier",
    #   "data": {
    #     "dossier": {
    #       "url": "/api/v1/application/51617/form/",
    #       "pk": 31777
    #     },
    #     "application": {
    #       "url": "/api/v1/application/51617/",
    #       "pk": 51617
    #     },
    #     "object": {
    #       "house": null,
    #       "property": null,
    #       "object": null,
    #       "pk": 8769
    #     }
    #   },
    #   "id": "e79b75c5-135e-44f3-95a2-304a661dac28"
    # }
    choose_specific_applicant(pk=51617)
