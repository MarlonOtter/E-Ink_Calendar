# E-Ink_calendar

calendar that displays weather and upcoming events using google calendar's api

To use this a google project needs to be setup, using the calednar api.
then credentials and a token are needded to be fetched.
Put these 2 files in a folder: /Secrets
along with this add a json file called calendars.json with this format:

```
 {
    "calendars" : [
        {
            "name" : "CALENDAR_NAME" // only necesarry to make it easier to identify multiple calendars
            "id" : "CALENDAR_ID"
        }
    ]
 }

```
