# RPi_Selenium_Web_Cam
A Python class "RPi_Camera" using selenium to manage webpage controlled IP cameras.

A first attempt to create a public Github repository; so documentation and build files will improve over time

Purpose is to manage/set the settings on multiple cameras by script rather than manually by web.
For instance: enabling/disabling the alarm sound.
Doing so is via selenium screen scraping. The camera webinterface uses a couple of nasty gimmicks (eg mouse-over enabled menus) that had to be simulated by combining multiple selenium methods...

About the class and it's methods:
The Class can manage multiple cameras at the same time and allows to be extended for multiple brands although it currently only has one implemented (see below). Obviously the screen scraping (menus and their behaviour can/will be very different by make...) and involve some trial/error java code inspection. I plan to add at least one other brand (for inside use).
The methods are pretty self-explanatory...
Typical usage flow is: (see __main__ procedure as testing script)
- TestCam1 = RPi_Camera( <camera params> )    # Init the Camera object and it's settings 
- RPi_Camera.OpenCamera ( TestCam1 )          # Open the page, log on and set to main menu
- ... RPi_Camera.Set_Mail(TestCam1, True)...  # Do what you need to do ...
- RPi_Camera.CloseCamera ( TestCam1 )         # Log out and close the page/selenium session
- del TestCam1                                # Tidy up if you no longer need the camera object


Environment the Class was developed/tested on:
- RaspBerry Pi 4 (4GB)
- Python 3
- IP PTZ Webcam 5M pixels (Yuchen brand with Sony heart) for outside use.
- Selenium Chromedriver (not in the build files; must be added manually )

To improve:
make it more robust / exception handling is minimal.
