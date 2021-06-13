from selenium import webdriver
from time import sleep
import random

my_list = []
with open("dict.txt") as f:
    for word in f:
        my_list.append(word)

n = len(my_list)
    
class bombParty():
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(r'C:\Users\Evan Zhang\Desktop\chromedriver', options=chrome_options)

    def solve(self, tag, nickname, maxWordLength, MAX_RANDINT):
        fname = f"https://jklm.fun/{tag}"
        self.driver.get(fname)

        sleep(2)
        username = self.driver.find_element_by_xpath("/html/body/div[2]/div[3]/form/div[2]/input")
        username.send_keys("")
        sleep(1)
        username.send_keys(nickname)
        
        sleep(1)
        nextBtn = self.driver.find_element_by_xpath("/html/body/div[2]/div[3]/form/div[2]/button")
        nextBtn.click()

        sleep(2)
        self.driver.switch_to.frame(0)
        
        while True:
            sleep(1)

            try:
                joinBtn = self.driver.find_element_by_xpath("/html/body/div[2]/div[3]/div[1]/div[1]/button")
                joinBtn.click()
                break
            except:
                pass

        
        while True:
            sleep(1)

            try:
                syllable = self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div[2]/div").text.upper()
                textInput = self.driver.find_element_by_xpath("/html/body/div[2]/div[3]/div[2]/div[2]/form/input")
                print(syllable)
                
                rand_int = random.randint(0, MAX_RANDINT)
                for i in range(rand_int, n):
                    word = my_list[i]
                    try:
                        if syllable in word:
                            if len(word) <= maxWordLength:
                                sleep(0.05)
                                textInput.send_keys(word)
                                sleep(0.1)
                                textInput.submit()
                                syllable = self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div[2]/div").text.upper()
                    except:
                        break
            except Exception as e:
                pass
        
bombBot = bombParty()

#easy - <6, medium - <8, hard - <10, impossible - <20
bombBot.solve("AAAA", "bot", 20, n-100000)
