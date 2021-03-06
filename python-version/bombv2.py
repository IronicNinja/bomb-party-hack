from selenium import webdriver
from time import sleep
import random

my_list = []
startWordDict = {}
cnt = 0
with open("dict.txt") as f:
    for word in f:
        my_list.append(word)

        if word[0] not in startWordDict:
            startWordDict[word[0]] = cnt

        cnt += 1

print(startWordDict)
n = len(my_list)

optimal_letters = "QJKVBPGFMCULDHRSNIOATE"
completed_set = set()

class bombParty():
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(r'C:\Users\Evan Zhang\Desktop\chromedriver', options=chrome_options)

    def solve(self, tag, nickname, maxWordLength, realistic=False):
        fname = f"https://jklm.fun/{tag}"
        self.driver.get(fname)

        sleep(2)
        username = self.driver.find_element_by_xpath("/html/body/div[2]/div[3]/form/div[2]/input")
        username.clear()
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

        currIndex = 0
        while True:
            sleep(1)

            try:
                syllable = self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div[2]/div").text.upper()
                textInput = self.driver.find_element_by_xpath("/html/body/div[2]/div[3]/div[2]/div[2]/form/input")

                if syllable:
                    print(syllable)
                
                startIndex = startWordDict[optimal_letters[currIndex]]
                print(optimal_letters[currIndex])
                go = True
                for i in range(startIndex, n):
                    if not go:
                        break
                    
                    word = my_list[i].replace('\n', '')
                    try:
                        if syllable in word:
                            if len(word) <= maxWordLength:
                                rand_sleep = random.uniform(0.05, 0.25) if realistic else 0.05
                                sleep(rand_sleep)

                                if realistic:
                                    word_sleep = random.uniform(0.5, 1)
                                    if syllable != self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div[2]/div").text.upper():
                                        go = False
                                        textInput.send_keys("")
                                        break

                                    for c in word:
                                        sleep(word_sleep/len(word))
                                        textInput.send_keys(c)
                                else:
                                    textInput.send_keys(word)

                                sleep(0.1)
                                textInput.submit()
                                syllable = self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div[2]/div").text.upper()

                                for char in word:
                                    completed_set.add(char)

                                go = False
                                for j in range(currIndex, len(optimal_letters)):
                                    if optimal_letters[j] not in completed_set:
                                        currIndex = j
                                        go = True
                                        break
                                
                                if not go:
                                    currIndex = 0
                                    completed_set.clear()
                    except:
                        break
            except Exception as e:
                print(e)
                pass

            try:
                next = self.driver.get.find_element_by_xpath("/html/body/div[2]/div[3]/div[1]/div[1]/button")
                next.click()
            except:
                pass
        
bombBot = bombParty()

#easy - <6, medium - <8, hard - <10, impossible - <20
bombBot.solve("AAAA", "bot", 10, True)
