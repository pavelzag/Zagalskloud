import random
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException        


class runSelenium(object):
    def __init__(self):
        # define a class attribute
        self.driver = webdriver.Chrome(executable_path='C:\Program Files (x86)\ChromeDriver\chromedriver.exe')
        self.driver.maximize_window()
        self.userToRecommend = 'pavelzagalsky'
        self.nothingText = "//h3[text() = 'Nothing to hear here']"
        self.errorText = "//a[text() = 'I need help']"

    def isElementPresent(self, locator):
        try:
            self.driver.find_element_by_xpath(locator)
        except NoSuchElementException:
            #print ('No such thing')
            return False
        return True

    def getAmountOfFollowings(self):
        #Get amount of followers
        userURL = "https://soundcloud.com/" + self.userToRecommend
        self.driver.get(userURL)
        followersString = "//a[@href='/" + self.userToRecommend + "/following'][1]"
        elem = self.driver.find_element_by_xpath(followersString)
        text = elem.text
        followersNumber = int(text.split("\n")[1])
        return followersNumber

    def countArtists(self):
        elementsAmt = 1
        elementToFind = '//li[@class=\'badgeList__item\'][' + str(elementsAmt) + ']'
        isElement = self.isElementPresent(elementToFind)
        print('The element is ' + str(isElement))
        while (isElement == True):
            elementsAmt+=1
            elementToFind = '//li[@class=\'badgeList__item\'][' + str(elementsAmt) + ']'
            isElement = self.isElementPresent(elementToFind)
        print('The last element is ' + str(elementsAmt))
        return elementsAmt

    def countSongs(self):
        elementsAmt = 1
        elementToFind = '//div[@class=\'sound__body\'][' + str(elementsAmt) + ']'
        isElement = self.isElementPresent(elementToFind)
        print('The element is ' + str(isElement))
        while (isElement == True):
            elementsAmt+=1
            elementToFind = '//li[@class=\'soundList__item\'][' + str(elementsAmt) + ']'
            isElement = self.isElementPresent(elementToFind)
        print('The last element is ' + str(elementsAmt))
        return elementsAmt-1
    
    def getRandomFollowee(self, followeeNum):
        if(followeeNum <= 1):
            randomNum = 1
        else:
            randomNum =  random.randrange(1, followeeNum, 1)
        print(randomNum)
        return randomNum

    def getRandomSong(self, songsNum):
        if(songsNum <= 1):
            randomNum = 1
        else:
            randomNum =  random.randrange(1, songsNum, 1)
        print(randomNum)
        return randomNum

    def selectTheFollowee(self, followerid):
        followeeElement = '//li[@class=\'badgeList__item\'][' + str(followerid) + ']//div[@class=\'userBadgeListItem\']//div[@class=\'userBadgeListItem__title\']//a[@class=\'userBadgeListItem__heading sc-type-small sc-link-dark sc-truncate\']'
        elem = self.driver.find_element_by_xpath(followeeElement)
        artistLink = elem.get_attribute('href')
        print('The link is ' + artistLink)
        self.driver.get(artistLink)
        
    def isPageOK(self, nothingText, errorText):
        _nothingText = nothingText
        _errorText = errorText

        #nothingText = "//h3[text() = 'Nothing to hear here']"
        #errorText = "//a[text() = 'I need help']"
        
        isPresent = self.isElementPresent(_nothingText)
        isPresent2 = self.isElementPresent(_errorText)
        if(isPresent == True or isPresent2 == True):
            return False
        return True

    def selenium(self):
        followersAmt = self.getAmountOfFollowings()
        followingURL = "https://soundcloud.com/" + self.userToRecommend + "/following"
        self.driver.get(followingURL)
        elementsAmt = self.countArtists()
        while(elementsAmt<followersAmt):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            elementsAmt = self.countArtists()
        print(str(elementsAmt))
        randomFollowee = self.getRandomFollowee(elementsAmt)
        self.selectTheFollowee(randomFollowee)
        #check if URL is valid
        isPageOK = self.isPageOK(self.nothingText, self.errorText)
        while(isPageOK == False):
            randomFollowee = self.getRandomFollowee(elementsAmt)
            self.driver.back()
            time.sleep(10) #find a better solution for artists loading
            self.selectTheFollowee(randomFollowee)
            isPageOK = self.isPageOK(self.nothingText, self.errorText)
        #count songs
        songsAmt = self.countSongs()
        songToClick = self.getRandomSong(songsAmt)
        elemString = '//a[@class=\'soundTitle__title sc-link-dark\']'
        self.driver.find_elements_by_xpath(elemString)[songToClick].click()
        #getURL
        currentURL = self.driver.current_url


        #self.driver.close()

if __name__ == '__main__':
    # create an instance of class runSelenium
    run = runSelenium()
    # call function
    run.selenium()

