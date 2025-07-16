# 🏒 Minor League Tracker

**Minor League Tracker** custom Home Assistant integration that monitors upcoming, live, and past games for any team supported by [TheSportsDB](https://www.thesportsdb.com). Built with a focus on minor league teams (like the Kansas City Mavericks 🏒), it can be used for **any team-based sport** TheSportsDB supports.
This entire thing was built just so I could get ECHL minor league hockey data on the scrolling info display in my living room so let my hyperfixation help you as well!
---

##  Features

- Tracks previous, next, and live games
- Polls TheSportsDB API every 30 seconds for near real-time updates
- Sensor state indicates game status: `pre`, `in`, or `post`
- Time-until-next-game attribute (e.g., "2 hours", "3 days", "2 weeks")
- Attributes for opponent, venue, scores, and league
- Entity link from integration overview for quick access


## Installation

### Via HACS (Custom Repository)

1. Go to **HACS → Integrations → 3-dot menu → Custom repositories**
2. Add this repository:  
   ```
   https://github.com/ArcReactorKC/MinorLeagueTracker
   ```
   and select **Integration** as the category.
3. Click **Add**.
4. Return to **HACS → Integrations → Explore & Download Repositories**, search for **Minor League Tracker**, and install.

### Manual Installation

1. Clone this repo or download it as a ZIP.
2. Extract it into:  
   ```
   /config/custom_components/minorleaguetracker/
   ```
3. Restart Home Assistant.

---

## Configuration

1. Go to **Settings → Devices & Services → + Add Integration**
2. Search for **Minor League Tracker**
3. Enter your team’s **exact name** (as it appears in TheSportsDB)

✅ That’s it! A sensor will be created with game tracking attributes.

---

## Example Sensor Output

| Attribute              | Description                              |
|------------------------|------------------------------------------|
| `state`                | `pre`, `in`, or `post`                   |
| `next_game`            | ISO date/time of next scheduled game     |
| `last_game_score`      | Final score of the most recent game      |
| `opponent`             | Name of opponent team                    |
| `venue`                | Game venue name                          |
| `league`               | League name (e.g., ECHL)                 |
| `time_until_game`      | Human-friendly countdown (e.g. "3 days") |

---

## 🛠 Configuration Options (Coming Soon)

In a future release, you’ll be able to:
- Choose which attributes to track
- Enable/disable sensors per team
- Select from a dropdown list of available leagues and teams
- working on scores however the limited API does not include live scoring watch for a seperate integration with v2 API support

---

## 🧠 Notes

- Uses TheSportsDB **Free v1 API**
- Requires an active internet connection
- Ensure your team name is spelled exactly as it appears in TheSportsDB
 For reference if you wanted to see data for the KC Mavericks you would need to enter "kansas city mavericks" as the team name exactly.


---

## 🙏 Credits

- Built by [ArcReactorKC](https://github.com/ArcReactorKC)
- Inspired by [Team Tracker](https://github.com/vasqued2/ha-teamtracker)
- Powered by [TheSportsDB API](https://www.thesportsdb.com/api.php)

---

## 📃 License

MIT License — see [`LICENSE`](LICENSE)
