import random
import time
#from tweepy import Stream
#from tweepy import API
#from tweepy import OAuthHandler
from tweepy import *
import tweepy
from tweepy.streaming import StreamListener
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException        


ckey = 'x80PDCNGYHSqIZpZ6ZHGIOTdV'
csecret = 'tUgRWCg3ds2fCL6SgnJkdkDxdhHFbvAZLktsyEMM9tn6qG6W2i'
atoken = '721350692292702208-gcDLyUcGgxFaVPzhVDcg0lxoZWkYvg0'
asecret = 'VLG0Jk99dj28HbNJQqRKnFUOKezBQ169ztQLQe7UFHlXV'
hotword = "zagalskloud"
#driver = webdriver.Chrome(executable_path='C:\Program Files (x86)\ChromeDriver\chromedriver.exe')
driver = webdriver.PhantomJS(executable_path=r'C:\phantomjs\bin\phantomjs.exe')
driver.implicitly_wait(60)
driver.maximize_window()
userToRecommend = 'pavelzagalsky'
nothingText = "//h3[text() = 'Nothing to hear here']"
errorText = "//a[text() = 'I need help']"

class listener(StreamListener):

    def on_data(self, data):
        #print(data)
        api = API(auth)
        created_at = data.split(',"created_at":"')[1].split('","utc_offset')[0]
        name = (data.split(',"screen_name":"')[1].split('","location')[0]).lower()
        tweetText = data.split(',"text":"')[1].split('","source')[0]
        tweetID = data.split(',"id_str":"')[1].split('","text')[0]
        print('Request made at: ' + created_at)
        print('Request made by: ' + name)
        print('Tweet Content: ' + tweetText)
        
        recommendedURL = runSelenium.selenium(name)
        if(recommendedURL == 'none'):
            try:
                api.update_status('@' + name + " Error " + str(random.randrange(1000, 9999)) + " Your SoundCloud user does not exist in the system")
            except TweepError: 
                print(str(TweepError))
                pass
            return True
        print('The recommended URL is: ' + recommendedURL)
        # Deletes all the previous posts
        #for recommendedURL in tweepy.Cursor(api.user_timeline).items():
        #    try:
        #        api.destroy_status(recommendedURL.id)
        #    except:
        #        pass
        try:
            api.update_status('@' + runSelenium.userToReplyTo + " " + recommendedURL)
        except TweepError:
            print(str(TweepError))
            pass
        #driver.close()
        return True

    def on_error(self, status):
        print(status)

    
class runSelenium:
    userToReplyTo = 'none'
    userToRecommend = 'none'
    def isElementPresent(locator):
        try:
            driver.find_element_by_xpath(locator)
        except NoSuchElementException:
            #print ('No such thing')
            return False
        return True

    def getAmountOfFollowings(name):
        #Get amount of followers
        userToRecommend = name
        userURL = "https://soundcloud.com/" + userToRecommend
        driver.get(userURL)
        driver.save_screenshot('something.png')
        isSCUserExists = runSelenium.isElementPresent("//a[@href='/" + userToRecommend + "/following'][1]")
        if(isSCUserExists == False):
            #userToRecommend = 'pavelzagalsky'
            runSelenium.userToRecommend = 'pavelzagalsky'
            runSelenium.userToReplyTo = name
            userURL = "https://soundcloud.com/" + runSelenium.userToRecommend
            driver.get(userURL)
            #return 0
        else:
            runSelenium.userToRecommend = name
            runSelenium.userToReplyTo = name

        followersString = "//a[@href='/" + runSelenium.userToRecommend + "/following'][1]"
        elem = driver.find_element_by_xpath(followersString)
        text = elem.text
        followersNumber = int(text.split("\n")[1])
        return followersNumber

    def countArtists():
        elementsAmt = 1
        elementToFind = '//li[@class=\'badgeList__item\'][' + str(elementsAmt) + ']'
        isElement = runSelenium.isElementPresent(elementToFind)
        while (isElement == True):
            elementsAmt+=1
            elementToFind = '//li[@class=\'badgeList__item\'][' + str(elementsAmt) + ']'
            isElement = runSelenium.isElementPresent(elementToFind)
        return elementsAmt

    def countSongs():
        elementsAmt = 1
        elementToFind = '//div[@class=\'sound__body\'][' + str(elementsAmt) + ']'
        isElement = runSelenium.isElementPresent(elementToFind)
        while (isElement == True):
            elementsAmt+=1
            elementToFind = '//li[@class=\'soundList__item\'][' + str(elementsAmt) + ']'
            isElement = runSelenium.isElementPresent(elementToFind)
        return elementsAmt-1
    
    def getRandomFollowee(followeeNum):
        if(followeeNum <= 1):
            randomNum = 1
        else:
            randomNum =  random.randrange(1, followeeNum, 1)
        return randomNum

    def getRandomSong(songsNum):
        if(songsNum <= 1):
            randomNum = 1
        else:
            randomNum =  random.randrange(1, songsNum, 1)
        return randomNum

    def selectTheFollowee(followerid):
        followeeElement = '//li[@class=\'badgeList__item\'][' + str(followerid) + ']//div[@class=\'userBadgeListItem\']//div[@class=\'userBadgeListItem__title\']//a[@class=\'userBadgeListItem__heading sc-type-small sc-link-dark sc-truncate\']'
        elem = driver.find_element_by_xpath(followeeElement)
        artistLink = elem.get_attribute('href')
        print('The chosen artist is ' + artistLink)
        driver.get(artistLink)
        
    def isPageOK(nothingText, errorText):
        _nothingText = nothingText
        _errorText = errorText
        isPresent = runSelenium.isElementPresent(_nothingText)
        isPresent2 = runSelenium.isElementPresent(_errorText)
        if(isPresent == True or isPresent2 == True):
            return False
        return True

    def selenium(name):
        userToRecommend = name
        followersAmt = runSelenium.getAmountOfFollowings(userToRecommend)
        if(followersAmt <=0):
            return 'none'
        followingURL = "https://soundcloud.com/" + runSelenium.userToRecommend + "/following"
        driver.get(followingURL)
        elementsAmt = runSelenium.countArtists()
        while(elementsAmt<followersAmt):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            elementsAmt = runSelenium.countArtists()
        print('Number of followed artists: ' + str(elementsAmt))
        randomFollowee = runSelenium.getRandomFollowee(elementsAmt)
        runSelenium.selectTheFollowee(randomFollowee)
        #check if URL is valid
        isPageOK = runSelenium.isPageOK(nothingText, errorText)
        while(isPageOK == False):
            randomFollowee = runSelenium.getRandomFollowee(elementsAmt)
            driver.back()
            time.sleep(10) #find a better solution for artists loading
            runSelenium.selectTheFollowee(randomFollowee)
            isPageOK = runSelenium.isPageOK(nothingText, errorText)
        #count songs
        songsAmt = runSelenium.countSongs()
        songToClick = runSelenium.getRandomSong(songsAmt)
        elemString = '//a[@class=\'soundTitle__title sc-link-dark\']'
        driver.find_elements_by_xpath(elemString)[songToClick].click()
        #getURL
        return driver.current_url

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track=[hotword])


