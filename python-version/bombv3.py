from selenium import webdriver
from time import sleep
import random

class bombParty():
    def __init__(self, tag, nickname, maxWordLength, typingSpeed):
        # typingSpeed - wpm

        print("Initializing...")
        self.tag = tag
        self.nickname = nickname
        self.maxWordLength = maxWordLength
        self.typingSpeed = 60/typingSpeed

        self.myList = []
        self.startWordDict = {}
        self.endWordDict = {}
        cnt = 0

        with open("dict.txt") as f:
            for word in f:
                word = word.replace('\n', '')
                if len(word) > self.maxWordLength:
                    continue

                self.myList.append(word)

                if word[0] not in self.startWordDict:
                    self.startWordDict[word[0]] = cnt
                    self.endWordDict[chr(ord(word[0]) - 1)] = cnt - 1

                cnt += 1

        self.totalWords = len(self.myList)
        print(f"Total words: {self.totalWords}")
        print(f"Start word dict: {self.startWordDict}")

        self.n = len(self.myList)
        self.optimalLetters = "QJKVBPGFMCULDHRSNIOATE" # Ordered by commonality in english language
        self.optimalLettersLength = len(self.optimalLetters)
        self.completedSet = set()
        self.usedWords = set()

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(r'C:\Users\Evan Zhang\Desktop\chromedriver', options=chrome_options)

    def play(self):
        fname = f"https://jklm.fun/{self.tag}"
        self.driver.get(fname)

        sleep(2)
        username = self.driver.find_element_by_xpath("/html/body/div[2]/div[3]/form/div[2]/input")
        username.clear()
        sleep(0.5)
        username.send_keys(self.nickname)
        
        sleep(0.5)
        nextBtn = self.driver.find_element_by_xpath("/html/body/div[2]/div[3]/form/div[2]/button")
        nextBtn.click()

        sleep(2)
        self.driver.switch_to.frame(0)
        
        # Join game ASAP
        while True:
            try:
                joinBtn = self.driver.find_element_by_xpath("/html/body/div[2]/div[3]/div[1]/div[1]/button")
                joinBtn.click()
                break
            except: 
                sleep(0.5)
                pass

        self.currIndex = 0
        while True:
            try:
                textInput = self.driver.find_element_by_xpath("/html/body/div[2]/div[3]/div[2]/div[2]/form/input")
                textInput.send_keys("")
                syllable = self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div[2]/div").text.upper()

                optimalLetter = self.optimalLetters[self.currIndex]
                startIndex = self.startWordDict[optimalLetter]
                endIndex = self.endWordDict[optimalLetter]

                print(f"Syllable: {syllable}, starting search from: {self.optimalLetters[self.currIndex]} to %c" % ("Z" if self.currIndex > self.totalWords//2 else "A"))

                for i in range(startIndex, self.n) if self.currIndex > self.totalWords//2 else range(endIndex, 0, -1):   
                    word = self.myList[i].replace('\n', '')
                    if syllable in word:
                        if len(word) <= self.maxWordLength:
                            if word not in self.usedWords:
                                word_sleep = random.uniform(self.typingSpeed*0.67, self.typingSpeed*1.5)/len(word) #typing speed
                                for c in word:
                                    sleep(word_sleep)
                                    textInput.send_keys(c)

                                sleep(random.uniform(word_sleep*0.67, word_sleep*1.5))
                                textInput.submit()

                                for char in word:
                                    self.completedSet.add(char)

                                self.usedWords.add(word)

                                go = True
                                for j in range(self.currIndex, self.optimalLettersLength):
                                    if self.optimalLetters[j] not in self.completedSet:
                                        self.currIndex = j
                                        go = False
                                        break
                                
                                if go:
                                    self.currIndex = 0
                                    self.completedSet.clear()

                                break

                # Iterate the other way
                print(f"Syllable: {syllable}, starting search from: {self.optimalLetters[self.currIndex]} to %c" % ("A" if self.currIndex > self.totalWords//2 else "Z"))
                for i in range(startIndex, 0, -1) if self.currIndex > self.totalWords//2 else range(endIndex, self.n):   
                    if syllable in word:
                        if len(word) <= self.maxWordLength:
                            if word not in self.usedWords:
                                word_sleep = random.uniform(self.typingSpeed, self.typingSpeed*2) #typing speed
                                for c in word:
                                    sleep(word_sleep/len(word))
                                    textInput.send_keys(c)

                                sleep(word_sleep/len(word)*2)
                                textInput.submit()

                                for char in word:
                                    self.completedSet.add(char)

                                self.usedWords.add(word)

                                go = True
                                for j in range(self.currIndex, self.optimalLettersLength):
                                    if self.optimalLetters[j] not in self.completedSet:
                                        self.currIndex = j
                                        go = False
                                        break
                                
                                if go:
                                    self.currIndex = 0
                                    self.completedSet.clear()

                                break
            except Exception as e:
                sleep(random.uniform(0.5, 1))
                pass

#1 - baby (you have a chance), #2 - easy (pros have a chance), #3 - medium, #4 - hard (no one will beat it), #5 - impossible (basically flexing)
def create_bot(tag, nickname, difficulty=3):
    if difficulty == 1:
        bot = bombParty(tag, nickname, 4, 60)
    elif difficulty == 2:
        bot = bombParty(tag, nickname, 6, 80)
    elif difficulty == 3:
        bot = bombParty(tag, nickname, 8, 100)
    elif difficulty == 4:
        bot = bombParty(tag, nickname, 12, 140)
    elif difficulty == 5:
        bot = bombParty(tag, nickname, 100, 200)
    else:
        raise Exception("Invalid difficulty, bot not created.")
    
    return bot

# custom creation
#bombBot = bombParty("AAAA", "bot", 4, 60)

bot = create_bot("AAAA", "bot", difficulty=3)
bot.play()
