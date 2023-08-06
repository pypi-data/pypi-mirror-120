from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import undetected_chromedriver.v2 as uc
import random as rd
import time
import ctypes

class WindowSort:
    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.__user32 = ctypes.windll.user32

        self.__user32.SetProcessDPIAware()

    @property
    def chrome_width(self):
        return self.__width

    @chrome_width.setter
    def chrome_width(self, value):
        self.__width = value

    @property
    def chrome_height(self):
        return self.__height

    @chrome_height.setter
    def chrome_height(self, value):
        self.__height = value

    def __call__(self, drivers):
        x, y = 1, 1
        window_width = self.__user32.GetSystemMetrics(0)

        for driver in drivers:
            driver.set_window_size(self.chrome_width, self.chrome_height)
            time.sleep(.5)

            driver.set_window_position(x, y)

            x += self.chrome_width + 105
            window_width -= x
            
            if not window_width < self.chrome_width: continue

            x = 1
            y += self.chrome_height
            window_width = self.__user32.GetSystemMetrics(0)

class ChromePlus(uc.Chrome):
    _timeout = 30
    _script_timeout = 9999
    _page_load_timeout = 60
    _scripts = {
        'get_user_agent': 'return navigator.userAgent',
    }

    def __init__(self, options=None, user_agent=None, profile_dir=None, **kwargs):
        self._delay_per_command = rd.randint(int(.5), 1)

        if user_agent or profile_dir:
            if not options: options = uc.ChromeOptions()
            if user_agent: options.add_argument(f'--user-agent={user_agent}')
                
            if profile_dir:
                options.user_data_dir = profile_dir
                options.add_argument(f'--user-data-dir={profile_dir}')
        
        super().__init__(options=options, **kwargs)
        
        self.set_script_timeout(self._script_timeout)
        self.set_page_load_timeout(self._page_load_timeout)

    def wait_for_new_title(self, current_title=None):
        current_title = self.title if not current_title else current_title
        while current_title == self.title:
            time.sleep(4)

    def send_keys(self, element, value, interval=.08):
        for char in value:
            element.send_keys(char)
            time.sleep(interval)

    def execute_elements(self, commands):
        commands = dict(sorted(commands.items()))

        for _, dict_value in commands.items():
            by, index, name = dict_value[:3]
            value = dict_value[-1]

            elements = WebDriverWait(self, self._timeout).until(
                EC.presence_of_all_elements_located((
                    by, name
                ))
            )
            self.send_keys(elements[index], value, .05)
            time.sleep(self._delay_per_command)
    
    def get_cookie_string(self):
        cookies = self.get_cookies()
        result = ''

        for cookie in cookies:
            result += f'{cookie["name"]}={cookie["value"]};'

        return result

    def get_user_agent(self):
        result = self.execute_script(self._scripts['get_user_agent'])
        return result

    def add_cookie_string(self, value):
        cookies = value.split(';')

        for cookie in cookies:
            item = cookie.split('=')

            if len(item) > 1:
                name, cookie_value = item
                self.add_cookie({'name': name, 'value': cookie_value})

        time.sleep(.5)
        self.refresh()