from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.core import HomeAssistant
from datetime import datetime, timedelta, timezone
import requests
import asyncio
import logging
from .const import (
    NEXT_EVENTS_API,
    LAST_EVENTS_API,
    LOOKUP_TABLE_API,
)

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=30)

async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities):
    team_id = entry.data["team_id"]
    league_id = entry.data["league_id"]
    team_name = entry.data["team_name"]
    season = entry.data["season"]

    coordinator = MinorLeagueDataUpdateCoordinator(
        hass, team_id=team_id, league_id=league_id, season=season
    )
    await coordinator.async_config_entry_first_refresh()

    sensor = MinorLeagueTeamSensor(coordinator, team_name)
    async_add_entities([sensor], True)


class MinorLeagueDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, team_id, league_id, season):
        super().__init__(
            hass,
            _LOGGER,
            name="MinorLeagueTrackerDataCoordinator",
            update_interval=SCAN_INTERVAL,
        )
        self.team_id = team_id
        self.league_id = league_id
        self.season = season

    async def _async_update_data(self):
        try:
            next_game = await asyncio.get_event_loop().run_in_executor(
                None, self.fetch_next_game
            )
            last_game = await asyncio.get_event_loop().run_in_executor(
                None, self.fetch_last_game
            )
            standings = await asyncio.get_event_loop().run_in_executor(
                None, self.fetch_standings
            )
            return {
                "next_game": next_game,
                "last_game": last_game,
                "standings": standings,
            }
        except Exception as err:
            raise UpdateFailed(f"Error fetching data: {err}")

    def fetch_next_game(self):
        try:
            url = f"{NEXT_EVENTS_API}{self.team_id}"
            response = requests.get(url, timeout=10)
            data = response.json()
            if data and "events" in data and data["events"]:
                return data["events"][0]
        except Exception as err:
            _LOGGER.error(f"Error fetching next game: {err}")
        return None

    def fetch_last_game(self):
        try:
            url = f"{LAST_EVENTS_API}{self.team_id}"
            response = requests.get(url, timeout=10)
            data = response.json()
            if data and "results" in data and data["results"]:
                return data["results"][0]
        except Exception as err:
            _LOGGER.error(f"Error fetching last game: {err}")
        return None

    def fetch_standings(self):
        try:
            url = LOOKUP_TABLE_API.format(league_id=self.league_id, season=self.season)
            response = requests.get(url, timeout=10)
            data = response.json()
            if data and "table" in data:
                return data["table"]
        except Exception as err:
            _LOGGER.error(f"Error fetching standings: {err}")
        return None


class MinorLeagueTeamSensor(Entity):
    def __init__(self, coordinator, team_name):
        self.coordinator = coordinator
        self._name = f"{team_name} Overview"

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        """Returns one of: pre, in, post, idle"""
        next_game = self.coordinator.data.get("next_game")
        last_game = self.coordinator.data.get("last_game")
        now = datetime.utcnow().replace(tzinfo=timezone.utc)

        if next_game:
            date_str = next_game.get("dateEvent")
            time_str = next_game.get("strTime")
            if date_str and time_str:
                try:
                    dt_str = f"{date_str} {time_str}"
                    game_time = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
                    if game_time <= now < game_time + timedelta(hours=3):
                        return "in"
                    elif now < game_time:
                        return "pre"
                except Exception as e:
                    _LOGGER.warning(f"Could not parse next game time: {e}")

        if last_game:
            date_str = last_game.get("dateEvent")
            time_str = last_game.get("strTime")
            if date_str and time_str:
                try:
                    dt_str = f"{date_str} {time_str}"
                    game_time = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
                    if now < game_time + timedelta(hours=6):
                        return "post"
                except Exception as e:
                    _LOGGER.warning(f"Could not parse last game time: {e}")

        return "idle"

    @property
    def extra_state_attributes(self):
        data = self.coordinator.data
        attrs = {}

        # Next game
        next_game = data.get("next_game")
        if next_game:
            attrs.update({
                "next_game_event": next_game.get("strEvent"),
                "next_game_date": next_game.get("dateEvent"),
                "next_game_time": next_game.get("strTime"),
                "next_game_home_team": next_game.get("strHomeTeam"),
                "next_game_away_team": next_game.get("strAwayTeam"),
                "next_game_venue": next_game.get("strVenue"),
                "next_game_league": next_game.get("strLeague"),
                "next_game_season": next_game.get("strSeason"),
            })

            # Add time until next game
            try:
                date_str = next_game.get("dateEvent")
                time_str = next_game.get("strTime")
                if date_str and time_str:
                    dt_str = f"{date_str} {time_str}"
                    game_time = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
                    now = datetime.utcnow().replace(tzinfo=timezone.utc)
                    delta = game_time - now
                    if delta.total_seconds() > 0:
                        seconds = int(delta.total_seconds())
                        days = seconds // 86400

                        if days > 30:
                            months = days // 30
                            time_until = f"{months} month{'s' if months > 1 else ''}"
                        elif days > 6:
                            weeks = days // 7
                            time_until = f"{weeks} week{'s' if weeks > 1 else ''}"
                        elif days >= 1:
                            time_until = f"{days} day{'s' if days > 1 else ''}"
                        else:
                            hours = (seconds % 86400) // 3600
                            minutes = (seconds % 3600) // 60
                            if hours >= 1:
                                time_until = f"{hours} hour{'s' if hours > 1 else ''}, {minutes} minute{'s' if minutes != 1 else ''}"
                            else:
                                time_until = f"{minutes} minute{'s' if minutes != 1 else ''}"

                        attrs["time_until_next_game"] = time_until
            except Exception as e:
                _LOGGER.warning(f"Could not calculate time until next game: {e}")

        # Last game
        last_game = data.get("last_game")
        if last_game:
            attrs.update({
                "last_game_event": last_game.get("strEvent"),
                "last_game_date": last_game.get("dateEvent"),
                "last_game_time": last_game.get("strTime"),
                "last_game_home_team": last_game.get("strHomeTeam"),
                "last_game_away_team": last_game.get("strAwayTeam"),
                "last_game_home_score": last_game.get("intHomeScore"),
                "last_game_away_score": last_game.get("intAwayScore"),
                "last_game_venue": last_game.get("strVenue"),
                "last_game_league": last_game.get("strLeague"),
                "last_game_season": last_game.get("strSeason"),
            })
        
        # Standings
        standings = data.get("standings")
        if standings:
            attrs["standings"] = standings
        # team thesportsdb.com ID number
        attrs["team_id"] = self.coordinator.team_id

        return attrs

    async def async_update(self):
        await self.coordinator.async_request_refresh()
