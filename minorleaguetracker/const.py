DOMAIN = "minorleaguetracker"

API_KEY = "123"  # TheSportsDB free API key

TEAM_SEARCH_API = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}/searchteams.php?t="
NEXT_EVENTS_API = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}/eventsnext.php?id="
LAST_EVENTS_API = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}/eventslast.php?id="
LOOKUP_TABLE_API = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}/lookuptable.php?l={{league_id}}&s={{season}}"
