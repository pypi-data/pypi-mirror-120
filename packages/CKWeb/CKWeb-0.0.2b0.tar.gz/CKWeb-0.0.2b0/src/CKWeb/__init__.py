# encoding: utf-8
import os
import sys
import glob
import inspect
import keyboard
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options as GCOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from robot.api.deco import keyword
import logging
import time

dir_file = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')

class web(object):

    def __init__(self):
        logging.basicConfig()
        logging.getLogger().setLevel(logging.INFO)
        logger = logging.getLogger(__name__)

    def _logDebug(self, funcName, status):
        time_s = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print('[{}]{}: {}'.format(time_s, funcName, status))

    def _status(self, status='fail'):
        if status == 'pass':
            status = 'PASSED'
        else:
            status = 'FAILED'
        return status

    def _scrollIntoView(self, arguments):
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", arguments)
        driver.execute_script("arguments[0].style = 'border:2px solid red;background-color: #f4ff00;'", arguments)
        time.sleep(0.5)
        driver.execute_script("arguments[0].style = ''", arguments)

    def _driverDownload(self):
        while True:
            try:
                driver_path = ChromeDriverManager(path=dir_file).install()
                return driver_path
            except:
                driver_path = glob.glob("{}/drivers/chromedriver/win32/**/[!driver.zip]*".format(dir_file))
                return driver_path[0]
    
    def _verifyPlatform(self):
        platform = sys.platform
        if platform == 'linux':
            profile = r'{}/.config/google-chrome/default'.format(os.environ['USERPROFILE'])
        elif platform == 'win32':
            profile = r'{}/AppData/Local/Google/Chrome/User Data'.format(os.environ['USERPROFILE'])
        else:
            profile = r'{}/Library/Application Support/Google/Chrome/Default'.format(os.environ['USERPROFILE'])
        return profile

    def _browserMaximizewindow(self, Maximizewindow=True):
        if Maximizewindow:
            driver.maximize_window()

    @keyword('Browser Open')
    def browserOpen(self, headless=False, Maximizewindow=True, profile=False):
        """ 
        headless, Maximizewindow, profile
            |    = Options =    |
            | False             |
            | True              |

        Examples:
            | `Browser Open` | headless=False | Maximizewindow=True | profile=False |
        """
        status = self._status()
        funcName = inspect.stack()[0][3]
        try:
            driver_path = self._driverDownload()
            global driver
            global actions
            options = GCOptions()
            options.headless = headless
            if profile == True:
                profile = self._verifyPlatform()
                options.add_argument("user-data-dir={}".format(profile))
            driver = webdriver.Chrome(executable_path=driver_path, options=options)
            driver.implicitly_wait(15)
            actions = ActionChains(driver)
            if Maximizewindow == True:
                self._browserMaximizewindow(True)
            else:
                self._browserMaximizewindow(False)
            status = self._status('pass')
            self._logDebug(funcName, status)
        except KeyboardInterrupt:
            status = self._status()
            self._logDebug(funcName, status)

    @keyword('Browser Goto')
    def browserGoto(self, url):
        """ 
        Examples:
            | Browser Goto     | https://www.google.com/  |
        """
        status = self._status()
        funcName = inspect.stack()[0][3]
        try:
            driver.get(url)
            status = self._status('pass')
            self._logDebug(funcName, status)
        except KeyboardInterrupt:
            status = self._status()
            self._logDebug(funcName, status)

    @keyword('Browser Input')
    def browserInput(self, xPath, text):
        """ 
        Examples:
            | Browser Input     | //*[@name='q']  |  test     |
        """
        status = self._status()
        funcName = inspect.stack()[0][3]
        try:
            input_text = driver.find_element(By.XPATH, xPath)
            self._scrollIntoView(input_text)
            input_text.clear()
            input_text.send_keys(text)
            status = self._status('pass')
            self._logDebug(funcName, status)
        except KeyboardInterrupt:
            status = self._status()
            self._logDebug(funcName, status)
    @keyword('Browser Click')
    def browserClick(self, xPath):
        """ 
        Examples:
            | Browser Click     | //*[@name='q']  |
        """
        status = self._status()
        funcName = inspect.stack()[0][3]
        try:
            click_element = driver.find_element(By.XPATH, xPath)
            self._scrollIntoView(click_element)
            click_element.click()
            status = self._status('pass')
            self._logDebug(funcName, status)
        except KeyboardInterrupt:
            status = self._status()
            self._logDebug(funcName, status)

    @keyword('Browser Click Text')
    def browserClickText(self, message):
        """ 
        Examples:
            | Browser Click Text | testmesage  |
        """
        status = self._status()
        funcName = inspect.stack()[0][3]
        try:
            click_element = driver.find_element(By.XPATH, '//*[text()="{}"]'.format(message))
            self._scrollIntoView(click_element)
            click_element.click()
            status = self._status('pass')
            self._logDebug(funcName, status)
        except KeyboardInterrupt:
            status = self._status()
            self._logDebug(funcName, status)

    @keyword('Browser Get')
    def browserGet(self, xPath):
        """ 
        Examples:
            | ${value}   | Browser Get     | //*[@name='q']  |
        """
        status = self._status()
        funcName = inspect.stack()[0][3]
        try:
            get_element = driver.find_element(By.XPATH, xPath)
            self._scrollIntoView(get_element)
            get = get_element.text
            status = self._status('pass')
            self._logDebug(funcName, status)
            return get
        except KeyboardInterrupt:
            status = self._status()
            self._logDebug(funcName, status)

    @keyword('Browser Select Frame')
    def browseriFrame(self, xPath):
        """ 
        Examples:
            | Browser Select Frame     | //*[@name='q']  |
        """
        status = self._status()
        funcName = inspect.stack()[0][3]
        try:
            browseriframe = driver.find_element(By.XPATH, xPath)
            driver.switchTo.frame(browseriframe)
            status = self._status('pass')
            self._logDebug(funcName, status)
        except KeyboardInterrupt:
            status = self._status()
            self._logDebug(funcName, status)

    @keyword('Browser Unselect Frame')
    def browserUniFrame():
        """ 
        Examples:
            | Browser Unselect Frame     |
        """
        status = self._status()
        funcName = inspect.stack()[0][3]
        try:
            uniframe = driver.switchTo.default_content()
            actions.move_to_element(uniframe).perform()
            status = self._status('pass')
            self._logDebug(funcName, status)
        except KeyboardInterrupt:
            status = self._status()
            self._logDebug(funcName, status)

    @keyword('Browser Select Value')
    def browserSelectValue(self, xPath, value):
        """ 
        Examples:
            | Browser Select Value     | //*[@name='q']  |  test     |
        """
        status = self._status()
        funcName = inspect.stack()[0][3]
        try:
            selectValue = driver.find_element(By.XPATH, xPath)
            self._scrollIntoView(selectValue)
            dropdown = Select(selectValue)
            dropdown.select_by_value(value)
            status = self._status('pass')
            self._logDebug(funcName, status)
        except KeyboardInterrupt:
            status = self._status()
            self._logDebug(funcName, status)

    @keyword('Browser Select Index')
    def browserSelectIndex(self, xPath, index):
        """ 
        Examples:
            | Browser Select Index     | //*[@name='q']  |  test     |
        """
        status = self._status()
        funcName = inspect.stack()[0][3]
        try:
            selectIndex = driver.find_element(By.XPATH, xPath)
            self._scrollIntoView(selectIndex)
            dropdown = Select(selectIndex)
            dropdown.select_by_index(index)
            status = self._status('pass')
            self._logDebug(funcName, status)
        except KeyboardInterrupt:
            status = self._status()
            self._logDebug(funcName, status)

    @keyword('Browser Select Text')
    def browserSelectText(self, xPath, text):
        """ 
        Examples:
            | Browser Select Text     | //*[@name='q']  |  test     |
        """
        status = self._status()
        funcName = inspect.stack()[0][3]
        try:
            selectText = driver.find_element(By.XPATH, xPath)
            self._scrollIntoView(selectText)
            dropdown = Select(selectText)
            dropdown.select_by_visible_text(text)
            status = self._status('pass')
            self._logDebug(funcName, status)
        except KeyboardInterrupt:
            status = self._status()
            self._logDebug(funcName, status)

    @keyword('Browser Keyboard')
    def browserKeyboard(self, text):
        """ 
        Examples:
            | Browser Keyboard     | test  |
        """
        status = self._status()
        funcName = inspect.stack()[0][3]
        try:
            keyboard.write(text)
            status = self._status('pass')
            self._logDebug(funcName, status)
        except KeyboardInterrupt:
            status = self._status()
            self._logDebug(funcName, status)

    @keyword('Browser Alert')
    def browserAlert(self, accept=True):
        """ 
        Examples:
            | Browser Alert   | accept=True   |
            | Browser Alert   | accept=False  |
        """
        status = self._status()
        funcName = inspect.stack()[0][3]
        try:
            action = driver.switch_to.alert
            if accept:
                action.accept();
            else:
                action.dismiss();
            status = self._status('pass')
            self._logDebug(funcName, status)
        except KeyboardInterrupt:
            status = self._status()
            self._logDebug(funcName, status)

    @keyword('Browser Popup')
    def browserPopup(self, xPath):
        """ 
        Examples:
            | Browser Popup   | //*[@name='q']  |
        """
        status = self._status()
        funcName = inspect.stack()[0][3]
        try:
            time.sleep(5)
            page = driver.window_handles
            driver.switch_to.window(page[1])
            driver.find_element(By.XPATH, xPath)
            status = self._status('pass')
            self._logDebug(funcName, status)
        except KeyboardInterrupt:
            status = self._status()
            self._logDebug(funcName, status)

    @keyword('Browser Main Page')
    def browserMainPage(self):
        """ 
        Examples:
            | Browser Main Page   |
        """
        status = self._status()
        funcName = inspect.stack()[0][3]
        try:
            time.sleep(5)
            page = driver.current_window_handle
            driver.switch_to.window(page)
            status = self._status('pass')
            self._logDebug(funcName, status)
        except KeyboardInterrupt:
            status = self._status()
            self._logDebug(funcName, status)

    @keyword('Browser Close')
    def close(self):
        """ 
        Examples:
            | Browser Close     |
        """
        status = self._status()
        funcName = inspect.stack()[0][3]
        try:
            driver.quit()
            status = self._status('pass')
            self._logDebug(funcName, status)
        except KeyboardInterrupt:
            status = self._status()
            self._logDebug(funcName, status)