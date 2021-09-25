from selenium import webdriver
from multiprocessing import Pool
import time,config,pickle,os.path,keyboard
from selenium.webdriver.chrome.options import Options

options = webdriver.ChromeOptions()
options.headless = config.silent
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0")
#mute
if config.mute_audio:
    options.add_argument("--mute-audio")

path_to_driver = r"chromedriver\chromedriver.exe"
def log_to_terminal(text):
    print(text)
def main(url):
 try:
    driver = webdriver.Chrome(path_to_driver,chrome_options=options)
    time.sleep(1)
    driver.get("https://www.twitch.tv/"+url)
    time.sleep(2)
    #authorization
    if config.load_cookies == False:
        login_button = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/nav/div/div[3]/div[3]/div/div[1]/div[1]/button").click()
        time.sleep(5)
        login_input = driver.find_element_by_id("login-username")
        password_input = driver.find_element_by_id("password-input")
        login_input.send_keys(config.login)
        password_input.send_keys(config.password)
        login1_input = driver.find_element_by_xpath("/html/body/div[3]/div/div/div/div/div/div[1]/div/div/div[3]/form/div/div[3]/button").click()
        time.sleep(30)
        if os.path.isfile("cookies") == False:
            pickle.dump(driver.get_cookies(),open("cookies",'wb'))
        time.sleep(30)
    else:
        if os.path.isfile("cookies"):
            for cookies in pickle.load(open("cookies",'rb')):
                driver.add_cookie(cookies)
    time.sleep(5)
    driver.refresh()
    log_to_terminal("Login successful")
    time.sleep(10)
    #18+ button
    try:
     driver.find_element_by_xpath("//button[@data-a-target='player-overlay-mature-accept']").click()
    except:
        pass
    time.sleep(5)
    #160p quality
    if config.auto_160p:
        driver.find_element_by_xpath("//button[@data-a-target='player-settings-button']").click()
        time.sleep(1)
        driver.find_element_by_xpath("//button[@data-a-target='player-settings-menu-item-quality']").click()
        time.sleep(1)
        a = driver.find_elements_by_xpath("//div[@data-a-target='player-settings-submenu-quality-option']")
        #a[0].click() #is auto
        a[5].click()
    while keyboard.is_pressed(config.key_stop)==False:
     if driver.current_url != ("https://www.twitch.tv/"+url):
         driver.get("https://www.twitch.tv/"+url)
     try:
            driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[1]/div[2]/div/div[1]/div/div/div/div/div/section/div/div[5]/div[2]/div[2]/div[1]/div/div/div/div[2]/div/div/div/button").click()
            time.sleep(5)
            log_to_terminal("The reward was collected")
     except:
        pass
 except Exception:
    print(Exception)
 finally:
    driver.close()
    driver.quit()
if __name__ == '__main__':
    p=Pool(len(config.streamers))
    p.map(main,config.streamers)
