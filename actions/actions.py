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

room_type = ['single_room', 'double_room']
room = [ { 'room_id' : 201, 'room_type' : 'single_room', 'status' : 'checkedin'} , 
         { 'room_id' : 202, 'room_type' : 'double_room', 'status' : 'booked'} , 
         { 'room_id' : 301, 'room_type' : 'single_room', 'status' : 'avail'} , 
         { 'room_id' : 302, 'room_type' : 'double_room', 'status' : 'checkedin'} , 
         { 'room_id' : 401, 'room_type' : 'double_room', 'status' : 'booked'} , 
         { 'room_id' : 402, 'room_type' : 'single_room', 'status' : 'booked'} , ]
room_price = {'single_room' : 100000, 'double_room' : 200000}


class ActionGreet(Action):

    def name(self) -> Text:
        return "action_greet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = tracker.get_slot('name')
        if (name):
            dispatcher.utter_message(response="utter_greet_user", name=name)
        else:
            dispatcher.utter_message(response="utter_greet_guest", name=name)

        return [SlotSet("name", name)]

class ActionBookRoom(Action):

    def name(self) -> Text:
        return "action_book_room"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        avail_rooms = []
        if (True):
            for i in range(len(room)):
                if room[i]['status'] == 'avail':
                    avail_rooms.append(room[i]['room_id'])
            if (len(avail_rooms) > 0):
                dispatcher.utter_message(response="utter_can_book_room", avail_room=avail_rooms)
            else:
                dispatcher.utter_message(response="utter_cannot_book_room")
        # dispatcher.utter_message(text=avail_rooms)
        
        return []

class ActionAskAvailability(Action):

    def name(self) -> Text:
        return "action_ask_availability"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        avail_rooms = []
        roomtype = tracker.get_slot('room_type')
        print(roomtype)
        # if room_type is "Single room":
        #     room_type == 'single_room'
        # else:
        #     room_type == 'double_room'
        # name = tracker.get_slot('name')
        for i in range(len(room)):
            if room[i]['status'] == 'avail' and room[i]['room_type'] == roomtype:
                avail_rooms.append(room[i]['room_id'])
        if (len(avail_rooms) > 0):
            dispatcher.utter_message(response="utter_avail_room", avail_room=avail_rooms)
        else:
            dispatcher.utter_message(response="utter_cannot_book_room", room_type=roomtype)
        
        return [SlotSet("room_type", roomtype)]

class ActionBookingForm(Action):

    def name(self) -> Text:
        return "action_booking_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        room_id = tracker.get_slot('room_id')
        roomtype = tracker.get_slot('room_type')
        dispatcher.utter_message(response="utter_booking_form", room_id=room_id, room_type=roomtype)
        
        return []

class ActionConfirmBooking(Action):

    def name(self) -> Text:
        return "action_confirm_booking"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        print("booking")
        room_id = int(tracker.get_slot('room_id'))

        print(room_id)
        price = 0
        for i in range(len(room)):
            if room[i]['room_id'] == room_id:
                room[i]['status'] == 'booked'
                price = room_price[room[i]['room_type']]
                print("booking", room[i]['room_type'], room_id, "success!")
                dispatcher.utter_message(response="utter_booking_success", price=price)
                break

        
        
        return []