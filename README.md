# E-Ink Calendar

Calendar that displays the weather and upcoming events on a waveshare 7x5in E-ink display. Initially started in mid-2023

To use this, a Google project needs to be setup, using the developer dashboard. And the credentials stored
in the folder: APIs/secrets/GoogleCalendar/

An access token needs to be retrieved by using the API, this should be stored with the credentials.

Along with this add a new json file called calendars.json with this format:
```
 {
    "calendars" : [
        {
            "name" : "Holidays"
            "id" : "CALENDAR_ID"
        },
        {
            "name" : "Personal"
            "id" : "CALENDAR_ID_2"
        }
    ]
 }
```
NOTE: The Calendar Name is only to make it easier for users to identify each calendar and is not used by the program

This tells the program what calendars it should make requests to, through the API.

To make use of the weather functionality the location and API key need to be provided in APIs/secrets/OpenWeatherMap/key.json
In the following format:
```
 {
    "lat": 0,
    "lon": 0,
    "key": "API_KEY"
}
```
The latitude and longitude is your location and the key is the key that you get by setting up the openWeatherMap API



___

