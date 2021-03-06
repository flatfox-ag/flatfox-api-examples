import requests
import json
import utils

from flask import Flask, request


# -----------------------------------------------------------------------------
# API CONFIG
# NB: Our API uses HTTP Basic Auth. You have to use the API key as username and
#     leave the password blank for each request.
# -----------------------------------------------------------------------------
API_SERVER_URL = 'https://flatfox.ch'
API_KEY = 'sk_xxxxxxxxxxxxxxxxxxxxxx'


# -----------------------------------------------------------------------------
# YOUR SERVER CONFIG
# NB: Keep in mind that your server, this url, has to be reachable from our
#     server flatfox.ch
# -----------------------------------------------------------------------------
YOUR_PUSH_SERVER_URL = 'http://127.0.0.1:5000'


# -----------------------------------------------------------------------------
# API ENDPOINTS
# -----------------------------------------------------------------------------
WEBHOOK_URL = '{host}/api/v1/webhook/'.format(host=API_SERVER_URL)


def register_webhook(webhook_name):
    """
    Example of how to register a webhook to receive events later. That needs to
    be done only once. You can choose between two delivery types:

    - 'push'
      If you register a 'push' webhook the 'push_url' attribute is required
      too. This url will be called with a POST request with a list of new events.

    - 'postbox' (polling)
      If you register a 'postbox' webhook, you have to pull pending events
      by yourself frequently. See example in get_events below.

    And you can subscribe your webhook for one or more event types:

    - 'push_dossier'
      Is created when a user wants to send a specific applicant/dossier from
      flatfox to another system for e.g. pre-filling a contract template.

    - 'application_chosen'
      Is created after an applicant was chosen as the new tenant for a listing.

    You can also change your webhook later.

    Example response for '/api/v1/webhook/':

        {
          "name": "rem",
          "delivery_type": "push",
          "event_types": ["push_dossier"],
          "push_url": "https://yourwebhhok.com/endpoint?key=yourownsecret"
        }

    """
    # check if webhook exists already and delete it if so.
    r = requests.get(WEBHOOK_URL, auth=(API_KEY, ''))
    if r.status_code == 200:
        requests.delete(WEBHOOK_URL, auth=(API_KEY, ''))

    # create the webhook we want for this example
    # NB: the url '/endpoint' has to be the same as in @app.route below.
    push_url = '{host}/endpoint'.format(host=YOUR_PUSH_SERVER_URL)
    r = requests.post(WEBHOOK_URL, auth=(API_KEY, ''),
                      json={'name': webhook_name,
                            'delivery_type': 'push',
                            'event_types': ['push_dossier'],
                            'push_url': push_url})

    utils.print_response(r)


def get_dossier_details(event):
    """
    This is an example of how to get dossier details of a 'push_dossier'
    type event. The api resource url is nested in 'data', 'dossier', 'url'.
    """
    url = '{host}{path}'.format(host=API_SERVER_URL,
                                path=event['data']['dossier']['url'])
    r = requests.get(url, auth=(API_KEY, ''))

    if r.status_code == 200:
        return r.json()

    return None


app = Flask(__name__)


@app.route('/endpoint', methods=['POST'])
def handle_events():
    events = request.json

    print '=' * 80
    print 'Received events: {}'.format(json.dumps(events, indent=2))
    print '=' * 80

    # Go through events
    for event in events:

        # Handle 'push_dossier' events
        if event['type'] == 'push_dossier':

            # Get application details
            dossier = get_dossier_details(event=event)

            # ... do something with this stuff ...
            print '=' * 80
            print 'Dossier details: {}'.format(json.dumps(dossier, indent=2))
            print '=' * 80

    return "OK"


if __name__ == "__main__":
    # You can name your own webhooks
    webhook_name = 'rem'

    # Register a push webhook
    register_webhook(webhook_name=webhook_name)

    # Start web server
    app.run(host="0.0.0.0", port=5000)
