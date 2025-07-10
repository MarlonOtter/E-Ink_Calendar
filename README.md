# E-Ink_calendar

calendar that displays weather and upcoming events using google calendar's api

To use this a google project needs to be setup, using the calendar api.
then credentials and a token are needded to be fetched.
Put these 2 files in a folder: APIs/secrets/GoogleCalendar/
along with these add a json file called calendars.json with this format:

The Calendar Name is only to make it easier for users to identify each calendar and is not used by the program

```
 {
    "calendars" : [
        {
            "name" : "Holidays"
            "id" : "CALENDAR_ID"
        }
    ]
 }

```

To make use of the weather functionality the location and API key need to be provided in APIs/secrets/OpenWeatherMap/key.json

```
 {
    "lat": 0,
    "lon": 0,
    "key": "API_KEY"
}
```

The latitude and longitude is your location and the key is the key that you get by setting up openWeatherMap
