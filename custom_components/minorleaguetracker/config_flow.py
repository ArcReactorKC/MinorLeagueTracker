import voluptuous as vol
from homeassistant import config_entries
import requests
from .const import DOMAIN, TEAM_SEARCH_API

class MinorLeagueTrackerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            team_name = user_input["team_name"]
            team_data = await self.hass.async_add_executor_job(self.search_team, team_name)
            if team_data:
                # Extract team and league info
                team = team_data[0]
                team_id = team.get("idTeam")
                league_id = team.get("idLeague")
                league = team.get("strLeague")
                team_name = team.get("strTeam")
                season = "2024-2025"  # You could make this configurable later

                return self.async_create_entry(
                    title=team_name,
                    data={
                        "team_id": team_id,
                        "league_id": league_id,
                        "league": league,
                        "team_name": team_name,
                        "season": season,
                    },
                )
            else:
                errors["base"] = "not_found"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required("team_name"): str}),
            errors=errors,
        )

    def search_team(self, team_name):
        try:
            url = f"{TEAM_SEARCH_API}{team_name.replace(' ', '%20')}"
            response = requests.get(url, timeout=10)
            data = response.json()
            return data.get("teams")
        except Exception:
            return None
