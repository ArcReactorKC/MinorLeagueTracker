import requests
from datetime import datetime
from homeassistant.helpers.entity import Entity
from .const import API_URL

def setup_platform(hass, config, add_entities, discovery_info=None):
    add_entities([MavericksNextGameSensor()], True)

class MavericksNextGameSensor(Entity):
    def __init__(self):
        self._state = None
        self._attributes = {}
        self._name = "Mavericks Next Game"

    def update(self):
        try:
            response = requests.get(API_URL, timeout=10)
            data = response.json()

            if not data or "events" not in data or not data["events"]:
                self._state = "No upcoming games"
                self._attributes = {}
                return

            event = data["events"][0]
            self._state = event.get("strEvent")
            self._attributes = {
                "date": event.get("dateEvent"),
                "time": event.get("strTime"),
                "league": event.get("strLeague"),
                "home_team": event.get("strHomeTeam"),
                "away_team": event.get("strAwayTeam"),
                "venue": event.get("strVenue"),
                "season": event.get("strSeason"),
            }
        except Exception as e:
            self._state = "Error fetching data"
            self._attributes = {"error": str(e)}

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes
