#!/usr/bin/python3.8
import json
import logging
import os

from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

#WEBHOOK_URL = os.environ.get('TeamsChannelWebhookUrl')

debug_mode = os.environ.get("debug_mode") #e.g "true/false"
# set up logging
logger = logging.getLogger()
if debug_mode:
    logger.setLevel(logging.INFO)
else:
    logger.setLevel(logging.ERROR)

def lambda_handler(event, context):
    
    if not WEBHOOK_URL:
        print("TeamsChannelWebhookUrl was not set: " + str(WEBHOOK_URL))
        raise KeyError

    logger.debug("Event: " + str(event))
    message = json.loads(event['Records'][0]['Sns']['Message'])
    logger.debug("Message: " + str(message))

    alarm_name = message['AlarmName']
    old_state = message['OldStateValue']
    new_state = message['NewStateValue']
    reason = message['NewStateReason']
    logger.info("Parser cloudwatch event for alarm: %s with state: %s" % (str(alarm_name), str(new_state)) )

    # select color schema depending on severity
    if '[high]' in alarm_name.lower():
        colour = "e83333" # red
    elif '[medium]' in alarm_name.lower():
        colour = "e89b2e" # orange
    elif '[low]' in alarm_name.lower():
        colour = "e3da2d" # yellow
    else:
        colour = "f21b5b" # pink

    data = {
        "colour": "64a837",
        "title": "%s - Resolved" % alarm_name,
        "text": "**%s** has changed from %s to %s - %s" % (alarm_name, old_state, new_state, reason)
    }

    if new_state.lower() == 'alarm':
        data = {
            "colour": colour,
            "title": "%s - Triggered" % alarm_name,
            "text": "**%s** has changed from %s to %s - %s" % (alarm_name, old_state, new_state, reason)
        }

    # generate final message
    message = {
      "@context": "https://schema.org/extensions",
      "@type": "MessageCard",
      "themeColor": data["colour"],
      "title": data["title"],
      "text": data["text"]
    }

    logger.debug(str(message))

    # send request to Teams
    req = Request(WEBHOOK_URL, json.dumps(message).encode('utf-8'))
    try:
        response = urlopen(req)
        response.read()
        logger.info("Message posted to Teams channel")
        return { "status": "200 OK"}
    except HTTPError as e:
        logger.error("Request failed: %d %s", e.code, e.reason)
    except URLError as e:
        logger.error("Server connection failed: %s", e.reason)
