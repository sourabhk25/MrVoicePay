# import flask modules
from flask import Flask, make_response, request, jsonify
import api_calls
# build the flask app
app = Flask(__name__)

# definition of the results function
def results():
    req = request.get_json(force=True)
    action = req.get('queryResult').get('action')

    result = {}

    if action == "checkBalance":
        result = getObject(api_calls.checkBalance())
    elif action=="transaction":
        result = getObject(api_calls.checkTransaction())
    elif action=="pay":
        to_username = req.get('queryResult').get('parameters').get("username")
        amount = req.get('queryResult').get('parameters').get("amount")
        result = getObject(api_calls.payToOtherUser(to_username,amount))
    elif action=="passcode":
        numbercode = req.get('queryResult').get('parameters').get("numbercode")
        result = getObject(api_calls.verifyPasscode(numbercode))
    # return the result json
    result = jsonify(result)
    return make_response(result)

# default route for the webhook
# it accepts both the GET and POST methods
@app.route('/', methods=['GET', 'POST'])
def index():
    # calling the result function for response
    return results()

# call the main function to run the flask app
if __name__ == '__main__':
   app.run(debug=True,host="0.0.0.0")


def getObject(speech_text):
    # your action statements here
    # do whatever you want
    # return response in dialogflow response format
    # i am going to use Dialogflow JSON reponse format
    # first build result json

    result = {} # an empty dictionary

    # fulfillment text is the default response that is returned to the dialogflow request
    result["fulfillmentText"] = "Sourabh wants to check balance"

    # you can also make rich respones like basic card, simple responses, list, table card etc.
    # you can refer this for rich response formats
    # https://github.com/dialogflow/fulfillment-webhook-json

    # you can also use custom payloads for different services like messenger or google assistant
    # below is an example of google assistant payload
    # the following paylod contains a simple response, a basic card and some suggestion chips.

    result["payload"] = {
        "google": {
            "expectUserResponse": True,
            "richResponse": {
                "items": [
                    {
                        "simpleResponse": {
                            "displayText": str(speech_text),
                            "textToSpeech": str(speech_text)
                        }
                    },
                    {
                        "basicCard": {
                            "title": "",
                            "subtitle": "",
                            "imageDisplayOptions": ""
                        }
                    }
                ]
            }
        }
    }

    return result

# # -*- coding:utf8 -*-
# # !/usr/bin/env python
# # Copyright 2017 Google Inc. All Rights Reserved.
# #
# # Licensed under the Apache License, Version 2.0 (the "License");
# # you may not use this file except in compliance with the License.
# # You may obtain a copy of the License at
# #
# #     http://www.apache.org/licenses/LICENSE-2.0
# #
# # Unless required by applicable law or agreed to in writing, software
# # distributed under the License is distributed on an "AS IS" BASIS,
# # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# # See the License for the specific language governing permissions and
# # limitations under the License.

# """This is a sample for a weather fulfillment webhook for an Dialogflow agent
# This is meant to be used with the sample weather agent for Dialogflow, located at
# https://console.dialogflow.com/api-client/#/agent//prebuiltAgents/Weather
# This sample uses the WWO Weather Forecast API and requires an WWO API key
# Get a WWO API key here: https://developer.worldweatheronline.com/api/
# """

# import json

# from flask import Flask, request, make_response, jsonify

# from forecast import Forecast, validate_params

# app = Flask(__name__)
# log = app.logger


# @app.route('/', methods=['POST'])
# def webhook():
#     """This method handles the http requests for the Dialogflow webhook
#     This is meant to be used in conjunction with the weather Dialogflow agent
#     """
#     req = request.get_json(silent=True, force=True)
#     try:
#         action = req.get('queryResult').get('action')
#     except AttributeError:
#         return 'json error'

#     if action == 'weather':
#         res = weather(req)
#     elif action == 'weather.activity':
#         res = weather_activity(req)
#     elif action == 'weather.condition':
#         res = weather_condition(req)
#     elif action == 'weather.outfit':
#         res = weather_outfit(req)
#     elif action == 'weather.temperature':
#         res = weather_temperature(req)
#     else:
#         log.error('Unexpected action.')

#     # print('Action: ' + action)
#     # print('Response: ' + res)

#     return make_response(jsonify({'fulfillmentText': "Sourabh wants to pay"}))


# def weather(req):
#     """Returns a string containing text with a response to the user
#     with the weather forecast or a prompt for more information
#     Takes the city for the forecast and (optional) dates
#     uses the template responses found in weather_responses.py as templates
#     """
#     parameters = req['queryResult']['parameters']

#     print('Dialogflow Parameters:')
#     print(json.dumps(parameters, indent=4))

#     # validate request parameters, return an error if there are issues
#     error, forecast_params = validate_params(parameters)
#     if error:
#         return error

#     # create a forecast object which retrieves the forecast from a external API
#     try:
#         forecast = Forecast(forecast_params)
#     # return an error if there is an error getting the forecast
#     except (ValueError, IOError) as error:
#         return error

#     # If the user requests a datetime period (a date/time range), get the
#     # response
#     if forecast.datetime_start and forecast.datetime_end:
#         response = forecast.get_datetime_period_response()
#     # If the user requests a specific datetime, get the response
#     elif forecast.datetime_start:
#         response = forecast.get_datetime_response()
#     # If the user doesn't request a date in the request get current conditions
#     else:
#         response = forecast.get_current_response()

#     return response


# def weather_activity(req):
#     """Returns a string containing text with a response to the user
#     with a indication if the activity provided is appropriate for the
#     current weather or a prompt for more information
#     Takes a city, activity and (optional) dates
#     uses the template responses found in weather_responses.py as templates
#     and the activities listed in weather_entities.py
#     """

#     # validate request parameters, return an error if there are issues
#     error, forecast_params = validate_params(req['queryResult']['parameters'])
#     if error:
#         return error

#     # Check to make sure there is a activity, if not return an error
#     if not forecast_params['activity']:
#         return 'What activity were you thinking of doing?'

#     # create a forecast object which retrieves the forecast from a external API
#     try:
#         forecast = Forecast(forecast_params)
#     # return an error if there is an error getting the forecast
#     except (ValueError, IOError) as error:
#         return error

#     # get the response
#     return forecast.get_activity_response()


# def weather_condition(req):
#     """Returns a string containing a human-readable response to the user
#     with the probability of the provided weather condition occurring
#     or a prompt for more information
#     Takes a city, condition and (optional) dates
#     uses the template responses found in weather_responses.py as templates
#     and the conditions listed in weather_entities.py
#     """

#     # validate request parameters, return an error if there are issues
#     error, forecast_params = validate_params(req['queryResult']['parameters'])
#     if error:
#         return error

#     # Check to make sure there is a activity, if not return an error
#     if not forecast_params['condition']:
#         return 'What weather condition would you like to check?'

#     # create a forecast object which retrieves the forecast from a external API
#     try:
#         forecast = Forecast(forecast_params)
#     # return an error if there is an error getting the forecast
#     except (ValueError, IOError) as error:
#         return error

#     # get the response
#     return forecast.get_condition_response()


# def weather_outfit(req):
#     """Returns a string containing text with a response to the user
#     with a indication if the outfit provided is appropriate for the
#     current weather or a prompt for more information
#     Takes a city, outfit and (optional) dates
#     uses the template responses found in weather_responses.py as templates
#     and the outfits listed in weather_entities.py
#     """

#     # validate request parameters, return an error if there are issues
#     error, forecast_params = validate_params(req['queryResult']['parameters'])
#     if error:
#         return error

#     # Validate that there are the required parameters to retrieve a forecast
#     if not forecast_params['outfit']:
#         return 'What are you planning on wearing?'

#     # create a forecast object which retrieves the forecast from a external API
#     try:
#         forecast = Forecast(forecast_params)
#     # return an error if there is an error getting the forecast
#     except (ValueError, IOError) as error:
#         return error

#     return forecast.get_outfit_response()


# def weather_temperature(req):
#     """Returns a string containing text with a response to the user
#     with a indication if temperature provided is consisting with the
#     current weather or a prompt for more information
#     Takes a city, temperature and (optional) dates.  Temperature ranges for
#     hot, cold, chilly and warm can be configured in config.py
#     uses the template responses found in weather_responses.py as templates
#     """

#     parameters = req['queryResult']['parameters']

#     # validate request parameters, return an error if there are issues
#     error, forecast_params = validate_params(parameters)
#     if error:
#         return error

#     # If the user didn't specify a temperature, get the weather for them
#     if not forecast_params['temperature']:
#         return weather(req)

#     # create a forecast object which retrieves the forecast from a external API
#     try:
#         forecast = Forecast(forecast_params)
#     # return an error if there is an error getting the forecast
#     except (ValueError, IOError) as error:
#         return error

#     return forecast.get_temperature_response()


# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0')
