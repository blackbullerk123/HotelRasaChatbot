# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

room_type = ['single_room', 'double_room']
room = [ { 'room_id' : 201, 'room_type' : 'single_room', 'status' : 'checkedin'} , 
         { 'room_id' : 202, 'room_type' : 'double_room', 'status' : 'booked'} , 
         { 'room_id' : 301, 'room_type' : 'single_room', 'status' : 'avail'} , 
         { 'room_id' : 302, 'room_type' : 'double_room', 'status' : 'checkedin'} , 
         { 'room_id' : 401, 'room_type' : 'double_room', 'status' : 'booked'} , 
         { 'room_id' : 402, 'room_type' : 'single_room', 'status' : 'avail'} , ]
room_price = {'single_room' : 100000, 'double_room' : 200000}


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []

class ActionAskAvailability(Action):

    def name(self) -> Text:
        return "action_ask_availability"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message["intent"].get("room_type")
        # shown_privacy = tracker.get_slot("shown_privacy")
        # name_entity = next(tracker.get_latest_entity_values("room_type"), None)
        # roomtype = tracker.get_slot("room_type")
        roomtype = tracker.latest_message['text']
        avail_rooms = []
        for i in range(len(room)):
            if room[i]['status'] == roomtype:
                avail_rooms.append(room[i]['room_id'])
        dispatcher.utter_message(text=avail_rooms)

        return avail_rooms

