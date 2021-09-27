from selenium import webdriver
from multiprocessing import Pool
import time,config,pickle,os.path,keyboard,datetime,random
from selenium.webdriver.chrome.options import Options

options = webdriver.ChromeOptions()
options.headless = config.silent
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
#mute
if config.mute_audio:
    options.add_argument("--mute-audio")

path_to_driver = r"chromedriver\chromedriver.exe"
def get_time():
    return str(str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute)+":"+str(datetime.datetime.now().second))

def log_to_terminal(text,nickname):
    print(text+" "+nickname+" "+get_time())

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
    log_to_terminal("Login successful",url)
    time.sleep(10)
    #18+ button
    try:
     driver.find_element_by_xpath("//button[@data-a-target='player-overlay-mature-accept']").click()
    except:
        pass
    time.sleep(5)
    #subtember
    try:
        driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[1]/main/div[2]/div[3]/div/div/div[1]/div[1]/div[2]/div/div[1]/div/div/div/div[2]/div[1]/div[2]/div[3]/div/div/div[2]/button").click()
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[1]/main/div[2]/div[3]/div/div/div[1]/div[1]/div[2]/div/div[1]/div/div/div/div[2]/div[1]/div[2]/div[2]/div[2]/div/div/div[1]/button").click()
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
        for i in a:
            if i.text == "160p":
                i.click()
    time.sleep(1)
    while keyboard.is_pressed(config.key_stop)==False:
     try:
            driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[1]/div[2]/div/div[1]/div/div/div/div/div/section/div/div[5]/div[2]/div[2]/div[1]/div/div/div/div[2]/div/div/div/button").click()
            time.sleep(1)
            log_to_terminal("The reward was collected",url)
            time.sleep(1)
            if config.send_mesages:
             chat = driver.find_element_by_xpath("//textarea[@data-a-target='chat-input']")
             chat.click()
             try:
                 driver.find_element_by_xpath("/html/body/div[5]/div/div/div/div/div/div/div[3]/button").click()   
             except:
                 pass     
             message = config.messages[random.randrange(0,len(config.messages))]
             chat.send_keys(message)
             time.sleep(5)
             driver.find_element_by_xpath("//button[@data-a-target='chat-send-button']").click()
             log_to_terminal("Message send: "+message,url) 
     except:
        pass
     if driver.current_url != ("https://www.twitch.tv/"+url):
             time.sleep(15)
             driver.get("https://www.twitch.tv/"+url)   
     else:
         continue
 except Exception:
    print(Exception)
 finally:
    log_to_terminal("End",url)
    driver.close()
    driver.quit()
if __name__ == '__main__':
    p=Pool(len(config.streamers))
    p.map(main,config.streamers)
