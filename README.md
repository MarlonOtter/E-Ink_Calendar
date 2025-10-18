# E-Ink Calendar

Calendar that displays the weather and upcoming events on a waveshare 7x5in E-ink display. Initially started in mid-2023

## Example Output

![Example Output image](https://github.com/MarlonOtter/E-Ink_Calendar/blob/main/Example_Combined_2024-12-24.png)

As the display is an e-ink display that can only display 2 colours, I have to generate the image to be displayed in 2 seperate colour channels (seperate images).
Each of these iamges are a black and white and the display combines both images into red, white and black

## Red Channel

![Red Channel output image](https://github.com/MarlonOtter/E-Ink_Calendar/blob/main/Example_Red_2024-12-24.png)

## Black Channel

![Black Channel output image](https://github.com/MarlonOtter/E-Ink_Calendar/blob/main/Example_Black_2024-12-24.png)

## Setup

To use this, a Google project needs to be setup, using the developer dashboard. And the credentials stored
in the folder: `APIs/secrets/GoogleCalendar/`

An access token needs to be retrieved by using the API, this should be stored with the credentials.

Along with this add a new json file called calendars.json with this format to the same directory:

```json
 {
    "calendars" : [
        {
            "name" : "Holidays",
            "id" : "CALENDAR_ID"
        },
        {
            "name" : "Personal",
            "id" : "CALENDAR_ID_2"
        }
    ]
 }
```

NOTE: The Calendar Name is only to make it easier for users to identify each calendar and is not used by the program

This tells the program what calendars it should make requests to, through the API.

To make use of the weather functionality the location and API key need to be provided in `APIs/secrets/OpenWeatherMap/key.json`
In the following format:

```json
 {
    "lat": 0,
    "lon": 0,
    "key": "API_KEY"
}
```

The latitude and longitude is your location and the key is the key that you get by setting up the openWeatherMap API

I have also included the ability for the program to display what bin needs to be put out for the next day. Inorder to use this `APIs/secrets/bins.json` needs to be created with this information:

NOTE: I have made this feature completely optional as different locations have different websites for bin schedule so it would be very unreliable. The website may also change format so would also cause issues.

```JSON
{
    "HouseURL" : "BIN_SCHEDULE_URL_FOR_HOUSE"
}
```


To send Error Emails create a `/APIs/email.json` file and enter the following information:

```json
{
  "senderAddr": "SENDER_EMAIL",
  "appPassword": "APP_PASSWORD",

  "debugAddr": "RECIEVER_EMAIL"
}
```

The App password can be retreived from (remove any spaces from the password):
[https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)

This should then send an email with any important information such as:

- error type,
- date
- weather code
- important event information

---

## Running The Calendar

execute the run.py file:

```Bash
python3 run.py
```
