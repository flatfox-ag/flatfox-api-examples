import threading
import requests
import json
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
WEBHOOK_URL = '{host}/api/v1/webhook/'.format(host=API_SERVER_URL)
EVENT_URL = '{host}/api/v1/webhook/event/'.format(host=API_SERVER_URL)


def register_webhook():
    """
    Example of how to register a webhook to receive events later. That needs to
    be done only once. You can choose between two delivery types:

    - 'push'
      If you register a 'push' webhook the 'push_url' attribute is required
      too. This url will be called with a POST request with a list of new events.

    - 'postbox' (polling)
      If you register a 'postbox' webhook, you have to pull pending events
      by yourself frequently. See example in get_events below.

    You can also change your webhook later.

    Example response for '/api/v1/webhook/':

        {
          "delivery_type": "push",
          "push_url": "https://yourwebhhok.com/endpoint?key=yourownsecret"
        }

    """
    # check if webhook exists already and delete it if so.
    r = requests.get(WEBHOOK_URL, auth=(API_KEY, ''))
    if r.status_code == 200:
        requests.delete(WEBHOOK_URL, auth=(API_KEY, ''))

    # create the webhook we want for this example
    r = requests.post(WEBHOOK_URL, auth=(API_KEY, ''),
                      data={'delivery_type': 'postbox'})
    utils.print_response(r)


def get_events():
    """
    The event api endpoint returns a list of events to work off. You also have
    to manually delete each event to remove them from this list later.

    Example response for '/api/v1/webhook/event/':

        [
          {
            "type": "push_dossier",
            "data": {
              "dossier": {
                "url": "/api/v1/application/51617/form/",
                "pk": 31777
              },
              "application": {
                "url": "/api/v1/application/51617/",
                "pk": 51617
              },
              "object": {
                "house": null,
                "property": null,
                "object": null,
                "pk": 8769
              }
            },
            "id": "e79b75c5-135e-44f3-95a2-304a661dac28"
          }
        ]

    """
    r = requests.get(EVENT_URL, auth=(API_KEY, ''))
    utils.print_response(r)

    return r.json()


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


def delete_event(event):
    url = '{event_url}{id}'.format(event_url=EVENT_URL, id=event['id'])
    r = requests.delete(url, auth=(API_KEY, ''))
    utils.print_response(r)


def check_for_new_events(interval):
    events = get_events()

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

            # Finally delete the event
            delete_event(event=event)

    # Start interval to check again for new events later
    # NB: You should consider to use a 'push' webhook instead of polling
    print "Checking again for new events in {} seconds...".format(interval)
    print "(Press CTRL+C to quit)"
    threading.Timer(interval, check_for_new_events, [interval]).start()


if __name__ == "__main__":
    # Register a postbox webhook
    register_webhook()

    # Start checking for new events
    check_for_new_events(interval=10)
