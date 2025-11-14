# E-Ink Calendar

Calendar that displays the weather and upcoming events on a waveshare 7x5in E-ink display. Initially started in mid-2023

## Example Output

![Example Output image](resources/Example_Combined_2024-12-24.png)

As the display is an e-ink display that can only display 2 colours, I have to generate the image to be displayed in 2 seperate colour channels (seperate images).
Each of these iamges are a black and white and the display combines both images into red, white and black

## Red Channel

![Red Channel output image](resources/Example_Red_2024-12-24.png)

## Black Channel

![Black Channel output image](resources/Example_Black_2024-12-24.png)

## Setup

All the Features of the Calendar are able to be enabled/disabled. By default all the features are disabled as they require API keys not part of the program by default.
In order to enable a feature the information needs to be set in the .env (.env.example is provided)
and then enabled in .env.features (.env.features.example is also provided).

### Google Calendar Setup

To use this feature, a Google project needs to be setup, using the developer dashboard. And the credentials stored
in the folder: `APIs/secrets/GoogleCalendar/`

### Weather Setup

To use this feature create an API key for the current weather by creating an account here: [https://home.openweathermap.org/users/sign_up](https://home.openweathermap.org/users/sign_up)

### Bins Setup

This is more complicated and can vary depending on location so should probably be disabled.

### Email on fail

To use this feature, the sender email needs to be stored in the .env (address that is sending the email). and the reciever (address that is recieving the email).

The App passord that allows the program to access the sender's google email (so it can send the message) can be retreived from here:
[https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)

`NOTE: REMOVE ANY SPACES FROM THE PASSWORD`

This should then send an email with any important information such as:

- error type,
- date (that is being ran)
- weather code
- important event information

---

## Running The Calendar

execute the run.py file:

```Bash
python3 run.py
```
