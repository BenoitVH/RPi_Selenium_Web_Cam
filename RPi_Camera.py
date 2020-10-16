from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

class RPi_Camera(object):
    'Controlling IP camera via through its webinterface using selenium scraping'
    __PATH = '/usr/lib/chromium-browser/chromedriver'
    __WINDOW_OFFSET      = 50   # for multiple cameras, offset each new window slightly
    __WINDOW_INIT_POS    = 100
    __WINDOW_INIT_WIDTH  = 1280 # as we use mouse moves, too small windows generate exceptions
    __WINDOW_INIT_HEIGHT = 720  # prefer 16*9 aspect ratio
    CameraCount = 0

    def __init__(self, CameraURL, CameraType, CameraUN='admin', CameraPW=''):
        self.Url      = "HTTP://"+CameraURL
        self.Type     = CameraType
        self.Username = CameraUN
        self.Password = CameraPW
        # self.driver = ""
        self.CameraID = RPi_Camera.CameraCount
        self.SettingsMode = False
        # self.driver = ""
        RPi_Camera.CameraCount += 1

    def __str__(self):
        TheStr = "URL: "+self.Url+"\nType: "+self.Type+"\nUN: "+self.Username+"\nPW: "+self.Password+"\ndriver: "+str(self.driver)+"\nID: "+str(self.CameraID)+"\nSettingmode: "+str(self.SettingsMode)
        return TheStr

    def OpenCamera (self):
        self.driver = webdriver.Chrome(RPi_Camera.__PATH)
        self.driver.get(self.Url)
        # just a basic test to see if correct page is loaded
        if not 'CAMERA' in self.driver.title: return False
        xyPos = RPi_Camera.__WINDOW_INIT_POS+(self.CameraID*RPi_Camera.__WINDOW_OFFSET)
        self.driver.set_window_rect(x=xyPos, y=xyPos, width=RPi_Camera.__WINDOW_INIT_WIDTH, height=RPi_Camera.__WINDOW_INIT_HEIGHT)
        # find the username field and set it right
        search_box = self.driver.find_element_by_id('username')
        search_box.clear()
        search_box.send_keys(self.Username)
        search_box = self.driver.find_element_by_id('password')
        search_box.clear()
        if self.Password != '' :
            search_box.send_keys(self.Password)
        # this one a bit tricky: selector tag not unique, be careful, first one is used.
        logon_box = self.driver.find_element_by_tag_name('button')
        # if this is the right button, the text = "Login"
        if logon_box.text == "Login": logon_box.click()
        try:
            # the main menu ("PlayBackMenu") is what we use to activate commands
            # as long as we're logged in, it should be at the top.
            # Main menu features 4 button id choices:
            # 1) main   = watch live video
            # 2) rsmain = remote camera settings
            # 3) lsmain = local app settings (not used)
            # 4) index  = logout
            MainMenu = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "PlayBackMenu"))
            )
            # All cameras capture in 16/9, let's watch it this way
            select_box = self.driver.find_element_by_id('scale_16_9')
            select_box.click()
            return True
        except:
            return False

    def Watch_Live(self):
        try:
            # "main" = button id for Live in main menu
            MainMenu = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "PlayBackMenu"))
            )
            select_box = self.driver.find_element_by_id('main')
            select_box.click()
            MainMenu = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'scale_16_9'))
            )
            select_box = self.driver.find_element_by_id('scale_16_9')
            select_box.click()
            self.SettingsMode = False
        except:
            pass

    def Open_Menu_Set_Item(self,
                           ConfigMenu='cfgMenu_1',
                           Menu_Name='',
                           Menu_Item=0,
                           Enable_Item='',
                           Save_Button='',
                           Set_ON=False
                           ):
        if not self.SettingsMode:  # no need to set remote config mode...
            try:
                # "index" = button id for logout in main menu
                MainMenu = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "PlayBackMenu"))
                )
                select_box = self.driver.find_element_by_id('rsmain')
                select_box.click()
                # Remote settings menu defaults to 'Camera Config'
                MainMenu = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'cfgMenu_1'))
                )
                self.SettingsMode = True
            except:
                self.SettingsMode = False
        MainMenu = WebDriverWait(self.driver, 2).until(
            EC.presence_of_element_located((By.ID, ConfigMenu))
        )
        select_box = self.driver.find_element_by_id(ConfigMenu)
        # First click on the Network menu (to set mouse position)
        select_box.click()
        # Then perform mouseover action relative to the Network menu
        # Any mouseclick event only works if the menuitem has been "enabled" via mouseover first
        webdriver.ActionChains(self.driver).move_to_element(select_box).move_by_offset(0,Menu_Item*28).perform()
        MainMenu = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, Menu_Name))
        )
        select_box = self.driver.find_element_by_id(Menu_Name)
        # print ( 'menu item: ', select_box.text )
        # Activate left hand menu
        select_box.click()
        MainMenu = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, Enable_Item))
        )
        select_box = self.driver.find_element_by_id(Enable_Item)
        # rest of code not yet implemented
        if Set_ON:    # enable is always top entry of select field
            select_box.send_keys(Keys.ARROW_UP)
            select_box.send_keys(Keys.ARROW_UP)
        else:
            select_box.send_keys(Keys.ARROW_DOWN)
            select_box.send_keys(Keys.ARROW_DOWN)
        select_box.send_keys(Keys.RETURN)
        select_box.click()
        # now apply save the change
        select_box = self.driver.find_element_by_id(Save_Button)
        select_box.click()
        # a confirmationbox will appear for 5 secs.
        try:
            MainMenu = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, Enable_Item))
            )
            select_box = self.driver.find_element_by_id(Enable_Item)
        except:
            self.driver.quit()



    def Set_Mail(self, Set_ON=False):
        RPi_Camera.Open_Menu_Set_Item(self, 'cfgMenu_2', 'net_email', 4, 'emailEnable', 'emailSave', Set_ON )

    def Set_FTP(self, Set_ON=False):
        RPi_Camera.Open_Menu_Set_Item(self, 'cfgMenu_2', 'net_ftp', 5, 'ftpEnable', 'ftpSave', Set_ON )

    def Set_Motion(self, Set_ON=False):
        RPi_Camera.Open_Menu_Set_Item(self, 'cfgMenu_4', 'arm_motion', 1 , 'motionEnable', 'motionSave', Set_ON )

    def Set_Detect(self, Set_ON=False):
        RPi_Camera.Open_Menu_Set_Item(self, 'cfgMenu_4', 'arm_detect', 2 , 'detectEnable', 'detectSave', Set_ON )

    def CloseCamera(self):
        try:
            # "index" = button id for logout in main menu
            MainMenu = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "PlayBackMenu"))
            )
            select_box = self.driver.find_element_by_id('index')
            select_box.click()
            self.driver.quit()
            RPi_Camera.CameraCount -= 1
        except:
            self.driver.quit()


if __name__ == "__main__":
    print("start test")
    TestCam1 = RPi_Camera("192.168.0.240", "Sony") # these test cameras use the default password
    TestCam2 = RPi_Camera(, "192.168.0.241", "Sony")
    if RPi_Camera.OpenCamera ( TestCam1 ):
        print ( "Camera 1 Open" )
    time.sleep(5) # Let the user actually see something!
    if RPi_Camera.OpenCamera ( TestCam2 ):
        print ( "Camera 2 Open" )
    time.sleep(5) # Let the user actually see something!
    RPi_Camera.Set_Mail(TestCam1, True)
    RPi_Camera.Watch_Live(TestCam2)
    print(str(TestCam1))
    print(str(TestCam2))
    time.sleep(5)
    RPi_Camera.Watch_Live(TestCam1)
    print(str(TestCam1))
    RPi_Camera.Set_Mail(TestCam2)
    RPi_Camera.Set_Detect(TestCam1, True)
    print(str(TestCam1))
    RPi_Camera.Set_FTP(TestCam1, False)
    RPi_Camera.Set_Motion(TestCam1, True)
    print(str(TestCam2))
    time.sleep(5)
    print("stop test")
    RPi_Camera.CloseCamera ( TestCam1 )
    RPi_Camera.CloseCamera ( TestCam2 )
    del TestCam1
    del TestCam2
