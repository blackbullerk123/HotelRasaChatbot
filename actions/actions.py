# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.types import DomainDict
from datetime import datetime
room_type = ['single_room', 'double_room']
room = [ { 'room_id' : 201, 'room_type' : 'single_room', 'status' : 'checkedin'} , 
         { 'room_id' : 202, 'room_type' : 'double_room', 'status' : 'booked'} , 
         { 'room_id' : 301, 'room_type' : 'single_room', 'status' : 'avail'} , 
         { 'room_id' : 302, 'room_type' : 'double_room', 'status' : 'checkedin'} , 
         { 'room_id' : 401, 'room_type' : 'double_room', 'status' : 'booked'} , 
         { 'room_id' : 402, 'room_type' : 'single_room', 'status' : 'avail'} , ]
room_price = {'single_room' : 100000, 'double_room' : 200000}
room_description = {'single_room' : 'good for one person or a couple 😉', 
                    'double_room' : 'good for a group of friends and okay for a couple but not exciting 🙄'}


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

class ActionSayName(Action):

    def name(self) -> Text:
        return "action_say_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("action_say_name")
        name = tracker.get_slot("name")
        if not name:
            dispatcher.utter_message(response="utter_cannot_say_name")
        else:
            dispatcher.utter_message(response="utter_say_name", name=name)
        return []

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
        for i in range(len(room)):
            if room[i]['status'] == 'avail' and room[i]['room_type'] == roomtype:
                avail_rooms.append(room[i]['room_id'])
        if (len(avail_rooms) > 0):
            dispatcher.utter_message(response="utter_avail_room", avail_room= ', '.join(map(str,avail_rooms)))
        else:
            dispatcher.utter_message(response="utter_cannot_book_room", room_type=roomtype)
        
        return [SlotSet("room_type", roomtype)]

class ActionBookingForm(Action):

    def name(self) -> Text:
        return "action_booking_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("action_booking_form")
        room_id = tracker.get_slot('room_id')
        roomtype = tracker.get_slot('room_type')
        print(room_id)
        print(room_type)
        dispatcher.utter_message(response="utter_booking_form", room_id=room_id, room_type=roomtype)
        
        return []

class ActionConfirmFormBooking(Action):

    def name(self) -> Text:
        return "action_confirm_form_booking"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[EventType]:
        
        print("action_confirm_form_booking")
        room_id = int(tracker.get_slot('room_id'))

        print(room_id)
        price = 0
        for i in range(len(room)):
            if room[i]['room_id'] == room_id:
                room[i]['status'] = 'booked'
                price = room_price[room[i]['room_type']]
                print("booking", room[i]['room_type'], room_id, "success!")
                print(room)
                dispatcher.utter_message(response="utter_booking_success", price=price)
                break
     
        return []

class ActionRoomTypeDetail(Action):

    def name(self) -> Text:
        return "action_room_type_detail"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("action_room_type_detail")
        roomtype = tracker.get_slot('room_type')
        print(room_type)
        for i in range(len(room)):
            if room[i]['room_type'] == roomtype:
                room[i]['status'] = 'booked'
                # print("booking", room[i]['room_type'], room_id, "success!")
                # print(room)
                dispatcher.utter_message(response="utter_room_type_detail", 
                                        room_type=roomtype, price=room_price[room[i]['room_type']], 
                                        description=room_description[room[i]['room_type']])
                break
        
        return []


class ActionFindPlace(Action):

    def name(self) -> Text:
        return "action_find_place"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("action_find_place")
        place_type = tracker.get_slot('place_type')
        print(place_type)
        address = tracker.get_slot('address')
        print(address)
        if (place_type and address): 
            
            dispatcher.utter_message(response="utter_find_place", place_type=place_type, address=address)
            return [SlotSet("place_type", None), SlotSet("address", None)]
        else:
            dispatcher.utter_message(response="utter_input_address")
        
        return []


class ActionAskTime(Action):

    def name(self) -> Text:
        return "action_ask_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("action_ask_time")
        dispatcher.utter_message(response="utter_ask_time", time=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        
        return []


