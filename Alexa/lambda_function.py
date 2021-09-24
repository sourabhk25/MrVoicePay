# -*- coding: utf-8 -*-

# This is a Color Picker Alexa Skill.
# The skill serves as a simple sample on how to use  
# session attributes.

import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard
import requests
import json
from decimal import Decimal

skill_name = "Voice pay"
# help_text = ("Please tell me your favorite color. You can say "
#              "my favorite color is red")

USERNAME = "nirbhay"
USERID = "5629290"
MAX_PAYMENT = 2000

# color_slot_key = "COLOR"
# color_slot = "Color"

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    """Handler for Skill Launch."""
    # type: (HandlerInput) -> Response
    speech = "Hello Nirbhay, Welcome to voice pay. You can check your balance, pay to other user and know last transactions"
    handler_input.response_builder.set_should_end_session(False)
    handler_input.response_builder.speak(speech)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input):
    """Handler for Help Intent."""
    # type: (HandlerInput) -> Response
    handler_input.response_builder.speak(help_text).ask(help_text)
    return handler_input.response_builder.response


@sb.request_handler(
    can_handle_func=lambda handler_input:
        is_intent_name("AMAZON.CancelIntent")(handler_input) or
        is_intent_name("AMAZON.StopIntent")(handler_input))
def cancel_and_stop_intent_handler(handler_input):
    """Single handler for Cancel and Stop Intent."""
    # type: (HandlerInput) -> Response
    speech_text = "Goodbye!"

    return handler_input.response_builder.speak(speech_text).response


@sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input):
    """Handler for Session End."""
    # type: (HandlerInput) -> Response
    return handler_input.response_builder.speak("Hasta lasagna, I got my eyes on ya").response


@sb.request_handler(can_handle_func=is_intent_name("Pay"))
def pay(handler_input):
    resetUsernameInSessionAttribute(handler_input)
    speech_text  =  "will update it later"
    display_text = ""
    slots = handler_input.request_envelope.request.intent.slots
    to_username = slots["username"].value
    to_username.lower()
    amount = slots["amount"].value
    URL = "http://35.240.203.4:5000/checkTransaction"
    r = requests.post(url=URL,json = json.loads(json.dumps({"USERID":USERID})))
    data = r.json()
    if (data["FLAG"]=="True"):
        debited_amount = data["BALANCE"]
        if (Decimal(amount)+Decimal(debited_amount)<=MAX_PAYMENT):
            URL = "http://35.240.203.4:5000/performTransaction"
            r = requests.post(url=URL,json = json.loads(json.dumps({"FROM_USERNAME":USERNAME,"TO_USERNAME":to_username,"AMOUNT":amount})))
            data = r.json()
            speech_text = data["MESSAGE"]
        else:
            handler_input.attributes_manager.session_attributes["FROM_USERNAME"] = to_username
            handler_input.attributes_manager.session_attributes["AMOUNT"] = amount
            speech_text = "Your last 24 hour transaction will be greater than decided limit. It will require passcode now for processing."
    else:
        speech_text = "Something is not right with checking transaction way. please try again later."
    return handler_input.response_builder.speak(speech_text).response




@sb.request_handler(can_handle_func=is_intent_name("checkBalance"))
def checkBalance(handler_input):
    resetUsernameInSessionAttribute(handler_input)
    speech_text  =  ""
    intent = handler_input.request_envelope.request.intent


    URL = "http://35.240.203.4:5000/checkBalance"
    r = requests.post(url=URL,json = json.loads(json.dumps({"USERNAME":USERNAME})))
    data = r.json()

    if ( data["FLAG"]=="True" ):
        balance = data["BALANCE"]
        balance = float("{0:.2f}".format(Decimal(balance)))
        speech_text = "your account balance is "+str(balance)
    else:
        message = data["MESSAGE"]
        speech_text = str(message)

    handler_input.response_builder.set_should_end_session(False)
    return handler_input.response_builder.speak(speech_text).response

def resetUsernameInSessionAttribute(handler_input):
    if "FROM_USERNAME" in handler_input.attributes_manager.session_attributes and handler_input.attributes_manager.session_attributes["FROM_USERNAME"] is not None:
        handler_input.attributes_manager.session_attributes["FROM_USERNAME"] = None
        handler_input.attributes_manager.session_attributes["AMOUNT"] = None


@sb.request_handler(can_handle_func=is_intent_name("passcode"))
def passcode(handler_input):

    slots = handler_input.request_envelope.request.intent.slots
    code = slots["numberCode"].value
    speech_text = ""

    if "FROM_USERNAME" in handler_input.attributes_manager.session_attributes and handler_input.attributes_manager.session_attributes["FROM_USERNAME"] is not None:
        to_username = handler_input.attributes_manager.session_attributes["FROM_USERNAME"]
        amount = handler_input.attributes_manager.session_attributes["AMOUNT"]
        
        URL = "http://35.240.203.4:5000/getpasscode"
        r = requests.post(url=URL,json = json.loads(json.dumps({"USERID":USERID})))
        data = r.json()
        logger.info("************")
        correct_passcode = data["PASSCODE"]
        if str(code)==str(correct_passcode):
            URL = "http://35.240.203.4:5000/performTransaction"
            r = requests.post(url=URL,json = json.loads(json.dumps({"FROM_USERNAME":USERNAME,"TO_USERNAME":to_username,"AMOUNT":amount})))
            data = r.json()
            logger.info("+++++++++++++")
            speech_text = data["MESSAGE"]
        else:
            speech_text = "Passcode dose not match, please try it once again."
    else:
        speech_text = "At present there is no requirement of passcode."

    return handler_input.response_builder.speak(speech_text).response

@sb.request_handler(can_handle_func=is_intent_name("transaction"))
def getTransaction(handler_input):
    resetUsernameInSessionAttribute(handler_input)
    speech_text  =  ""
    intent = handler_input.request_envelope.request.intent

    URL = "http://35.240.203.4:5000/transaction"
    r = requests.post(url=URL,json = json.loads(json.dumps({"USERID":USERID})))
    data = r.json()

    if ( data["FLAG"]=="True" ):
        logger.info("Flag is true **************************")
        trans = data["DATA"]
        speech_text = createSpeechForTransaction(trans)
    else:
        message = data["MESSAGE"]
        speech_text = str(message)

    handler_input.response_builder.set_should_end_session(False)
    return handler_input.response_builder.speak(speech_text).response

def createSpeechForTransaction(data):
    speech_text = ""
    for o in data:
        logger.info(str(o))
        speech_text = speech_text + (createSpeechForTransactionFromObject(o))
    return speech_text

def createSpeechForTransactionFromObject(o):
    username = o["USERNAME"]
    amount = o["AMOUNT"]
    timestamp = o["TIME"]
    logger.info(str(timestamp))
    speech_text = " "+str(amount)+" rupees to "+str(username)+", on "+str(timestamp)+". "
    return speech_text

month = {"1":"January","2":"February","3":"March","4":"April","5":"May","6":"June","7":"July","8":"August","9":"September","10":"October","11":"November","12":"December"}

def speakTime(time):
    ss = time.split("(")[1].split(")")[0].split(", ")
    spech_text = ss[2]+" "+month[ss[1]]+" "+ss[0]+" on "+ss[3]+" hours, "+ss[4]+" minutes and "+ss[5]+" second GMT."
    return spech_text

# @sb.request_handler(can_handle_func=is_intent_name("WhatsMyColorIntent"))
# def whats_my_color_handler(handler_input):
#     """Check if a favorite color has already been recorded in
#     session attributes. If yes, provide the color to the user.
#     If not, ask for favorite color.
#     """
#     # type: (HandlerInput) -> Response
#     if color_slot_key in handler_input.attributes_manager.session_attributes:
#         fav_color = handler_input.attributes_manager.session_attributes[
#             color_slot_key]
#         speech = "Your favorite color is {}. Goodbye!!".format(fav_color)
#         handler_input.response_builder.set_should_end_session(False)
#     else:
#         speech = "I don't think I know your favorite color. " + help_text
#         handler_input.response_builder.ask(help_text)

#     handler_input.response_builder.speak(speech)
#     return handler_input.response_builder.response


# @sb.request_handler(can_handle_func=is_intent_name("MyColorIsIntent"))
# def my_color_handler(handler_input):
#     """Check if color is provided in slot values. If provided, then
#     set your favorite color from slot value into session attributes.
#     If not, then it asks user to provide the color.
#     """
#     # type: (HandlerInput) -> Response
#     slots = handler_input.request_envelope.request.intent.slots

#     if color_slot in slots:
#         fav_color = slots[color_slot].value
#         handler_input.attributes_manager.session_attributes[
#             color_slot_key] = fav_color
#         speech = ("Now I know that your favorite color is {}. "
#                   "You can ask me your favorite color by saying, "
#                   "what's my favorite color ?".format(fav_color))
#         reprompt = ("You can ask me your favorite color by saying, "
#                     "what's my favorite color ?")
#     else:
#         speech = "I'm not sure what your favorite color is, please try again"
#         reprompt = ("I'm not sure what your favorite color is. "
#                     "You can tell me your favorite color by saying, "
#                     "my favorite color is red")

#     handler_input.response_builder.speak(speech).ask(reprompt)
#     return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.FallbackIntent"))
def fallback_handler(handler_input):
    """AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    # type: (HandlerInput) -> Response
    speech = (
        "The {} skill can't help you with that.").format(skill_name)
    handler_input.response_builder.speak(speech)
    return handler_input.response_builder.response


def convert_speech_to_text(ssml_speech):
    """convert ssml speech to text, by removing html tags."""
    # type: (str) -> str
    s = SSMLStripper()
    s.feed(ssml_speech)
    return s.get_data()


@sb.global_response_interceptor()
def add_card(handler_input, response):
    """Add a card by translating ssml text to card content."""
    # type: (HandlerInput, Response) -> None
    response.card = SimpleCard(
        title=skill_name,
        content=convert_speech_to_text(response.output_speech.ssml))


@sb.global_response_interceptor()
def log_response(handler_input, response):
    """Log response from alexa service."""
    # type: (HandlerInput, Response) -> None
    print("Alexa Response: {}\n".format(response))


@sb.global_request_interceptor()
def log_request(handler_input):
    """Log request to alexa service."""
    # type: (HandlerInput) -> None
    print("Alexa Request: {}\n".format(handler_input.request_envelope.request))


@sb.exception_handler(can_handle_func=lambda i, e: True)
def all_exception_handler(handler_input, exception):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    # type: (HandlerInput, Exception) -> None
    print("Encountered following exception: {}".format(exception))

    speech = "Sorry, there was some problem. Please try again!!"
    handler_input.response_builder.speak(speech).ask(speech)

    return handler_input.response_builder.response


######## Convert SSML to Card text ############
# This is for automatic conversion of ssml to text content on simple card
# You can create your own simple cards for each response, if this is not
# what you want to use.

from six import PY2
try:
    from HTMLParser import HTMLParser
except ImportError:
    from html.parser import HTMLParser


class SSMLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.full_str_list = []
        if not PY2:
            self.strict = False
            self.convert_charrefs = True

    def handle_data(self, d):
        self.full_str_list.append(d)

    def get_data(self):
        return ''.join(self.full_str_list)

################################################


# Handler to be provided in lambda console.
lambda_handler = sb.lambda_handler()
