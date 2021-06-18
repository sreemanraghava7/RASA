# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.forms import FormAction
import requests
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


class ActionCapital(Action):

    

    def name(self) -> Text:
        return "action_tell_capital"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        knowledge = open("data/countrycap.txt","r")
        l = {}
        for line in knowledge:
            temp = line.lstrip().rstrip().split(':')
            l[temp[0]] = temp[1]
                
        x = l.keys()
        
        
        response = requests.get("https://restcountries.eu/rest/v2/all").json()
        
        

        entities = tracker.latest_message['entities']
        print('Last message Now ', entities)
        con = ""

        for e in entities:
            if e['entity'] == 'country':
                con = e['value'].lower().lstrip().rstrip()

        message = "Sorry! I cannot find what you are looking for."

        try:
            for data in response:
                if con in x:
                    message = "Capital : "+l[con]
                    break
                if data["name"].lower() == con:
                    message = "Capital : "+data["capital"]
                    break
                
        except Exception:
            message = "Sorry! I cannot find what you are looking for."

        dispatcher.utter_message(text=message)

        return []