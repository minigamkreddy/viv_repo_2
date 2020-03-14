import httplib
import logging
import socket
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.command import Command
from time import gmtime, strftime

logging = logging.getLogger("__name__")


class Ap_Agent():
    """Contains all the functions related to AP configuration."""

    def __init__(self):
        options = Options()
        options.headless = False
        self.driver = webdriver.Firefox(firefox_options=options)
        self.driver.set_page_load_timeout(180)
        self.driver.delete_all_cookies()

    def Login(self, ip_addr, user_name, password):
        """ Login to AP using given IP address, User and Password

        Args:
          ip_addr (str): IP address of 3rd party AP	#TODO: changed here.
          user_name (str) : Username of 3rd party AP
          password (str) : Password of 3rd party AP

        Returns:
          bool: retVal. True for success, False otherwise.
        """
        try:
          logging.info("http://" + user_name + ":" + password + "@" +
                       ip_addr)
          self.driver.get("http://" + ip_addr)
          time.sleep(4)  # AP login page loading time
          self.driver.find_element_by_xpath('//*[@id="userName"]'
                                            ).send_keys(user_name)
          time.sleep(4)  # AP page loading time
          self.driver.find_element_by_xpath('//*[@id="pcPassword"]').send_keys(password)
          time.sleep(4)  # AP page loading time
          self.driver.find_element_by_xpath('//*[@id="loginBtn"]').click()
          time.sleep(18)  # AP page loading time
          self.driver.find_element_by_xpath('//*[@id="advanced"]').click()
          time.sleep(4)  # AP home page loading time
        except Exception as error_msg:
          logging.error('Exception in AP login : %s' % error_msg)
          return False
        return True

    def SetWireless(self, frequency, ssid, mode, channel, bandwidth):
        """ According to Frequency value, It configures SSID,CHANNEL,MODE and
        BANDWIDTH

        Args:
          frequency (str): freq of 3rd party AP
          ssid (str) : ssid of 3rd party AP
          mode (str) : mode of 3rd party AP
          channel (str) : Channel of 3rd party AP
          bandwidth (str) : Bandwidth of 3rd party AP

        Returns:
          bool: Tuple of True for success, False otherwise.
        """
        frequency = frequency.upper()
        mode = mode.upper()
        bandwidth = bandwidth.upper()
        ssid = ssid + strftime("_%Y%m%d_%H%M%S", gmtime())
        if(len(ssid) > 32):
          logging.error("Ssid should be less than 32 character")
          return False
        logging.info("FREQ- "+frequency + "\nSSID- " + ssid + "\nMODE- "
              + mode + "\nCHANNEL- " + channel + "\nBANDWIDTH- "
              + bandwidth)
        wireless_mode = {'N': '2', 'AC': '1', 'GN-MIXED': '2', 'BGN-MIXED': '3'}
        wireless_bandwidth = {'AUTO': '1', '20': '2', '40': '3'}
        if(frequency == '5GHZ'):
          channl = {"36": "1", '40': '2', '44': '3', '48': '4', '149': '5',
                    '153': '6', '157': '7', '161': '8', '165': '9'}
          channel = str(channl.get(channel))
          logging.info(channel)
        if(channel.upper() == "AUTO"):
            channel = "1"
        else:
          ch = int(channel)+1
          channel = str(ch)
        try:
          if (frequency == '24GHZ'):
            self.driver.find_element_by_xpath('//*[@name="wireless"]').click()
            time.sleep(1)  # AP page loading time
            self.driver.find_element_by_xpath('//*[@name="wireless-settings" and '
                                              '@class = "sec"]').click()
            time.sleep(2)  # AP page loading time
            self.driver.find_element_by_xpath('//*[@id="show_2g"]').click()
            time.sleep(1)  # AP page loading time
            self.driver.find_element_by_xpath('//*[@name="ssid"]').clear()
            self.driver.find_element_by_xpath('//*[@name="ssid"]').send_keys(
                ssid)
            self.driver.find_element_by_xpath('//*[@id="wireless-setting-2g"]'
                                              '/div[8]/div[2]/div[1]/a').click()
            self.driver.find_element_by_xpath("//*[@id='wireless-setting-2g']"
                                              "/div[8]/div[2]/div[1]/div/div[3]"
                                              "/div/div/ul/li[" + wireless_mode.
                                              get(mode) + "]/label").click()
            time.sleep(1)  # AP page loading time
            self.driver.find_element_by_xpath('//*[@id="wireless-setting-2g"]/'
                                              'div[9]/div/div[2]/div[1]/a').click()
            self.driver.find_element_by_xpath("//*[@id='wireless-setting-2g']/"
                                              "div[9]/div/div[2]/div[1]/div/div["
                                              "3]/div/div/ul/li[" + wireless_bandwidth.get(
                bandwidth) + "]/label"
                                                                  "").click()
            time.sleep(1)  # AP page loading time
            self.driver.find_element_by_xpath('//*[@id="wireless-setting-2g"]/'
                                              'div[10]/div[2]/div[1]/a').click()
            self.driver.find_element_by_xpath('//*[@id="wireless-setting-2g"]/'
                                              'div[10]/div[2]/div[1]/div/div[3]'
                                              '/div/div/ul/li[' + channel +
                                              ']/label').click()
            time.sleep(1)  # AP page loading time
            self.driver.find_element_by_xpath('//*[@id="wireless-setting-2g"] '
                                              '/div[12]/div/div/div/div[1]'
                                              '/button').click()
          elif(frequency == '5GHZ'):
            self.driver.find_element_by_xpath('//*[@id="wireless_5g_menu"]').click()
            time.sleep(1)  # AP page loading time
            self.driver.find_element_by_xpath('//*[@id="wireless_5g_menu0"]').click()
            time.sleep(2)  # AP page loading time
            #self.driver.find_element_by_xpath('//*[@id="show_5g"]').click()
            time.sleep(3)  # AP page loading time
            self.driver.switch_to_frame(self.driver.find_element_by_id('frame'))
            time.sleep(3)
            self.driver.find_element_by_id('ssid').clear()
            self.driver.find_element_by_id('ssid').send_keys(ssid)
            # self.driver.find_element_by_xpath('//*[@id="ssid"]'
            #                                  '').send_keys(ssid)
            self.driver.find_element_by_xpath('/html/body/div/center/form/table/tbody/tr[7]/td[2]/div/div/a').click()
            self.driver.find_element_by_xpath("/html/body/div/center/form/table/tbody/tr[7]/td[2]/div/div/div/ul/li[" + wireless_mode.get(mode) + "]/label").click()
                                              
            time.sleep(1)  # AP page loading time
            self.driver.find_element_by_xpath('/html/body/div/center/form/table/tbody/tr[8]/td[2]/div/div/a').click()
            self.driver.find_element_by_xpath('/html/body/div/center/form/table/tbody/tr[8]/td[2]/div/div/div/ul/li[" + wireless_bandwidth.get(bandwidth)"]/label/span[2]').click()
            time.sleep(1)  # AP page loading time
            self.driver.find_element_by_xpath('/html/body/div/center/form/table/tbody/tr[9]/td[2]/div/div/a').click()
            self.driver.find_element_by_xpath('/html/body/div/center/form/table/tbody/tr[9]/td[2]/div/div/div/ul/li[' + channel +']/label').click()
            time.sleep(1)  # AP page loading time
            self.driver.find_element_by_xpath('//*[@id="Save"]').click()
	    self.driver.switch_to.default_content()
          else:
            logging.error('This AP support only \"24GHZ\" , \"5GHZ\" frequency.')
            return (False, False)
        except Exception as error_msg:
          logging.error('Exception raised during third party AP Wireless configuration: %s' % error_msg)
          time.sleep(30)
          return (False, False)
        time.sleep(10)  # Wait time to save AP  configuration
        return (True, ssid)

    def SetSecurity(self, frequency, auth_type, encryption_type=None,
                    passphrase=None):
        """ Sets third party AP with the security configuration - freq, auth_type, encryption_type, passphrase.

        Args:
            frequency (str): frequency of 3rd party AP
            auth_type (str) : authentication type of 3rd party AP
            encp_type (str) : Encryption type of 3rd party AP
            passphrase (str) : Passphrase of 3rd party AP

        Returns:
            bool: retVal. True for success, False otherwise.
        """
        frequency = frequency.upper()
        auth_type = auth_type.upper()
        if (auth_type == "OPEN"):
          logging.info("FREQ- " + frequency + "\nAUTH- " + auth_type)
        else:
          if (len(passphrase) > 64):
            logging.error("Psk value should be less than 64 character")
            return False
          encryption_type = encryption_type.upper()
          logging.info("FREQ- " + frequency + "\nAUTH- " + auth_type +
                       "\nSHARED_KEY- " + passphrase + "\nENCRYPTION_TYPE- " +
                       encryption_type)
        sel_sec = {'OPEN': '1', 'WPA-WPA2-MIXED': '2', 'WPA-WPA2-ENT': '3',
                   'WEP': '4', 'WPA2': '2', 'WPA': '2'}
        time.sleep(3)  # AP page loading time
        try:
          if (frequency == '24GHZ'):
            self.driver.find_element_by_xpath('//*[@id="show_2g"]').click()
            time.sleep(1)  # AP page loading time
            self.driver.find_element_by_xpath('//*[@id="wireless-setting-2g"]'
                                              '/div[4]/div[2]/div[1]/a').click()
            self.driver.find_element_by_xpath('//*[@id="wireless-setting-2g"]'
                                              '/div[4]/div[2]/div[1]/div/div[3]'
                                              '/div/div/ul/li[' + sel_sec.get(
                                               auth_type) + ']/label').click()
            time.sleep(1)  # AP page loading time
            if (auth_type == 'OPEN'):
              pass
            else:
              if (auth_type == 'WPA'):
                self.driver.find_element_by_xpath('//*[@id="wireless-setting-2g'
                                                  '"]/div[5]/div[1]/div[2]/div['
                                                  '1]/ul[2]/li/div[1]/label/span['
                                                  '2]').click()
              elif (auth_type == 'WPA2'):
                self.driver.find_element_by_xpath('//*[@id="wireless-setting-2g'
                                                  '"]/div[5]/div[1]/div[2]/div['
                                                  '1]/ul[3]/li/div[1]/label/span['
                                                  '2]').click()
              self.driver.find_element_by_xpath('//*[@id="personal-password-2g'
                                                '"]').clear()
              self.driver.find_element_by_xpath('//*[@id="personal-password-2g'
                                                '"]').send_keys(passphrase)
            time.sleep(1)  # AP page loading time
            self.driver.find_element_by_xpath('//*[@id="wireless-setting-2g'
                                              '"]/div[12]/div/div/div/div[1]'
                                              '/button').click()
          elif (frequency == '5GHZ'):
            #self.driver.find_element_by_xpath('//*[@id="show_5g"]').click()
            self.driver.find_element_by_xpath('//*[@id="wireless_5g_menu2"]').click()
            
            self.driver.switch_to_frame(self.driver.find_element_by_id('frame'))
            time.sleep(1)  # AP page loading time
            self.driver.find_element_by_xpath('/html/body/div/center/form/table/tbody/tr[3]/td/div/div/ul/li[2]/div[2]/div/table/tbody/tr[1]/td[2]/div/div/a').click()
            print("manoj_1")
            self.driver.find_element_by_xpath('/html/body/div/center/form/table/tbody/tr[3]/td/div/div/ul/li[2]/div[2]/div/table/tbody/tr[1]/td[2]/div/div/div/ul/li[' + sel_sec.get(auth_type) + ']/label'
                                              ).click()
            time.sleep(1)  # AP page loading time
            if (auth_type == 'OPEN'):
              pass
            else:
              if (auth_type == 'WPA'):
                self.driver.find_element_by_xpath('/html/body/div/center/form/table/tbody/tr[3]/td/div/div/ul/li[2]/div[2]/div/table/tbody/tr[1]/td[2]/div/div/div/ul/li[1]/label').click()
                print("manoj_2")
              elif (auth_type == 'WPA2'):
                self.driver.find_element_by_xpath('/html/body/div/center/form/table/tbody/tr[3]/td/div/div/ul/li[2]/div[2]/div/table/tbody/tr[1]/td[2]/div/div/div/ul/li[2]/label').click()
              self.driver.find_element_by_xpath('//*[@id="personal-password-5g'
                                                '"]').clear()
              self.driver.find_element_by_xpath('//*[@id="personal-password-5g'
                                                '"]').send_keys(passphrase)
            time.sleep(1)  # AP page loading time
            self.driver.find_element_by_xpath('//*[@id="Save"]').click()
          else:
            logging.error('This AP support only \"24GHZ\" , \"5GHZ\" frequency.')
            return False
        except Exception as error_msg:
          logging.error('Exception raised during third party AP Security configuration: %s' % error_msg)
          return False
        time.sleep(10)  # Wait time to save AP  configuration
        return True

    def CloseWebDriver(self):
        """ Closes the webdriver

        Args:
            None

        Returns:
            bool: retVal. True for success, False otherwise.
        """
        self.driver.quit()
        try:
            self.driver.execute(Command.STATUS)
            logging.error('Webdriver not closed')
            return False
        except (socket.error, httplib.CannotSendRequest):
            return True
        return True

    def SetWps(self, frequency):
        """ According to Frequency value, configures WPS secuirity

        Args:
            frequency (str): frequency of 3rd party AP

        Returns:
          bool: retVal. True for success, False otherwise.
        """
        logging.info("FREQ- "+frequency)
        time.sleep(3)  # AP home page loading time
        try:
          enabled = self.driver.find_element_by_xpath('//*[@id="'
                                                      'wifisc_enable_select'
                                                      '"]').is_selected()
          if(not enabled):
            self.driver.find_element_by_xpath('//*[@id="wifisc_enable_select'
                                              '"]').click()
            self.driver.find_element_by_xpath('//*[@id="SaveSettings_Btm"'
                                              ']').click()
            try:
              alert = self.driver.switch_to_alert()
              alert.accept()
            except Exception as error_msg:
                logging.debug('%s exception is passed ' % error_msg)
            self.driver.find_element_by_xpath('//*[@id="RestartNow"]').click()
            time.sleep(27)  # Wait time to restart wps button

          self.driver.find_element_by_xpath('//*[@id="'
                                            'wifisc_add_sta_start_button"]'
                                            '').click()
          time.sleep(2)  # AP home page loading time
          self.driver.find_element_by_xpath('//*[@id="wz_next_b"]').click()
          self.driver.find_element_by_xpath('//*[@id="config_method_radio_1'
                                            '"]').click()
          self.driver.find_element_by_xpath('//*[@id="wz_save_b"]').click()
          time.sleep(2)  # Wait time to save AP  configuration
        except Exception as error_msg:
          logging.error('Exception in set wps : %s' % error_msg)
          return False
        return True
