from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from pprint import pprint
# import 'creds.json' 

# ---------------------------------- Library --------------------------------- #
    #! - There should be a folder named as TestData in library for author automation user. 
    #           This folder should not have "Golf Explained - Sequencing Forced Order" published in it. 
    #! - Make sure that EndUserAutomation have the permission to access FolderD in library .
    #! - Make sure Project A in workspace and folderD in library are empty in Author Automation user.
    #! - There should be a folder named as Permanent Data in library for admin automation user. 
    #! - Make sure Regression category is present on the portal under user categories.
# ---------------------------------------------------------------------------- #

# ------------------------- Translation Dictionaries ------------------------ #
    #! - There should be a Memory Translation - SAP - Clone with language spanish, present on the  Memory Translation Dictionaries page (One time creation).
    #! - On the Memory Translation Dictionaries page there should be no dictionary present that is using a FireFox application.
    #! - There should be a dictionary "Memory Translation - Default - Clone (Microsoft - Internet Explorer (6/7/8/9/10/11))" with language German and spanish only(no other language should be there), present on the  Memory Translation Dictionaries page (One time creation).
# ---------------------------------------------------------------------------- #
creds = [
    "brant.jolly@assima.net",
    "Test!234"]

class checker:

    # Sets the Driver, load strategy, and implicit wait time (10)
    def __init__(self):
        options = Options()
        options.page_load_strategy = 'normal'
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)

    def login(self, url, creds):
        self.driver.get(url)
        loginBox = self.driver.find_element_by_id('Form1')
        userField = loginBox.find_element_by_id('Content_LogOn_UserName').send_keys(creds[0])
        passField = loginBox.find_element_by_id('Content_LogOn_Password').send_keys(creds[1])
        subButn = loginBox.find_element_by_id('Content_LogOn_LoginButton').click()

    # Search feature for repeated use, obj to be returned depends on xpath
    #! Work to find solution better than XPath bcs XPath no work inside folder
    def search(self, q):
        searchBox = self.driver.find_element_by_id('SearchBox')
        searchBox.find_element_by_id('SearchBox_TextBox').clear()
        searchBox.find_element_by_id('SearchBox_TextBox').send_keys(q)
        sleep(3)

        # XPath may not corrospond 
        obj = self.driver.find_element_by_xpath('//*[@id="Content_Content_FolderViewer_FolderViewer_TreeGridItems"]/div/ol/li/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr/td[3]/div/div/a[2]')
        print('Top result is: ', obj.text)
        
        if obj:
            return obj
        else:
            print('No obj to return')
            return 'NOTHINGGGGG'

# ------------------------------ Checking Users ------------------------------ #
    #// - UserA should be present on portal with Author Role(One time creation).
    #// - UserB should be present on portal with Author Role(One time creation).
    #// - Make sure that we have a Author Automation user on portal. (Password- Assima@1)
    #// -Make sure that we have a EndUser Automation user on portal. (Password-Assima@1)
    #! - Test User1 should be present on portal with age 25 (One time creation).
    #! - Test User2 should be present on portal with City Wonderland (One time creation). 
    #// - If userC doesn't exists on portal,create a User with first name UserC and last name Test. And it should not have the role of both an Author and an Admin. It's Unique Id and email should be set to userc.test@assima.net. (Harkinder will update this point)
# ---------------------------------------------------------------------------- #
    def check_users(self, userDict):
        url = 'https://community-725release.assima.dev/Community/Users/Default.aspx#search='
        user1_link = ''
        user2_link = ''
        for key in userDict.keys():
            self.driver.get(url + key)
            self.driver.fullscreen_window()
            searchBox = self.driver.find_element_by_id('SearchBox')
            searchBox.find_element_by_id('SearchBox_TextBox').clear()
            searchBox.find_element_by_id('SearchBox_TextBox').send_keys(key)
            sleep(3)
            if key == 'Test User1' or key == 'Test User2':
                topResult = self.driver.find_element_by_xpath('/html/body/form/section/section[2]/section[2]/div[2]/div[1]/ol/li[2]/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr/td[3]/div/a')
            else:
                topResult = self.driver.find_element_by_xpath('/html/body/form/section/section[2]/section[2]/div[2]/div[1]/ol/li[1]/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr/td[3]/div/a')
            print(topResult)
            if topResult.text == key:
                userDict[key] = True
            #! Search for user1 age and user2 city
        return userDict
    
    # Returns a dict of project name : url
    # Useful bcs workspace wont need to be opened before each test
    def get_projects(self):
        self.driver.get('https://725release.assima.dev/Workspace/Folder/Default.aspx')
        sleep(2)
        project_dict = {}
        projects = self.driver.find_elements_by_class_name('assima__treeNode')
        for project in projects:
            link = project.find_element_by_class_name('name')
            project_dict[link.text] = link.get_attribute('href')
        return project_dict

# --------------------------------- Checklist -------------------------------- #
    #// - There should be a project named as TestData in workspace and it should contain 
    #//     News Item,
    #//     vao1 lesson
    #//     a course named as “Course”
    #//     Golf explained - sequencing forced order
    #//     CollaborateAdminitration_CourseSlides
    #//     CollaborateAdminitration_ExerciseGuide
    #//     Web Content. 
    #//     This project should be created by admin and author should also have its access. 
    #// - In the TestData folder, confirm that the "Course" is named as "Course" instead of "Course Test".
# ---------------------------------------------------------------------------- #
       
# --------------------------------- Workspace -------------------------------- #
    #// - Project Global should exist in the workspace and have a web content item named Test and a va01 lesson.
    
    #? - Make sure that we have a Web Content in Global folder which is also published to Permanent folder in library. 
    #? - There should be a Global project in workspace which should have a Golf explained - sequencing forced order in unpublished form. Author should also have access for this global project. 
    #! - Project Golbal should have Golf Explained - Sequencing Forced Order lesson in it and it should also be published to permanent fodler in library. 
    #! - There should be 'ProjectC' folder in the workspace, with a 'News Item' and va01 lesson file inside it. Make sure that the va01 lesson is not localised to any language. 
    #! - There should be a project named as LocaliseTestData in workspace and should contain a VA01 lesson which should not be localised in any language. This project should be created by admin and author should also have access to it. 
    #// - Make sure that we have a va01 lesson in global project. 
    #! - A va01 lesson should be present inside the Global folder
# ---------------------------------------------------------------------------- #
    def check_global_existance(self, url):
        # Library Tab
        self.driver.get('https://725release.assima.dev/Library/Folder/Default.aspx?LocalizedItemId=20427&RootType=2#categories=')
        print('\nLibrary Tab-----------------------------------')
        if self.search('Golf Explained - Sequencing Forced Order') != 'Golf Explained - Sequencing Forced Order':
            globalDict['Golf Explained - Sequencing Forced Order'] = False
            print('Golf not published')
        if self.search('Web Content') != 'Web Content':
            globalDict['Web Content'] = False
            print('Web not published')

    def check_existance(self, dataDict, url):
        self.driver.get(url)
        self.driver.fullscreen_window()
        sleep(2)
        for key in dataDict.keys():
            topResult = self.search(key).text
            if topResult == key:
                dataDict[key] = True
        return dataDict

    def check_author(self, url):
        authorCreds = ['author.automation@assima.net', 'Assima@1']
        self.login(url, authorCreds)



    def stop(self):
        print("Closing Now")
        self.driver.close()
        self.driver.quit()

testDataDict = {
    'News Item' : False,
    'va01' : False,
    'Course' : False,
    'Golf Explained - Sequencing Forced Order' : False,
    'CollaborateAdministrator_CourseSlides' : False,
    'CollaborateAdministrator_ExerciseGuide' : False,
    'Web Content' : False}

globalDict = {
    'Test': False,
    'va01': False,
    'Golf Explained - Sequencing Forced Order': False,
    'Web Content' : False}

userDict = {
    'UserA Test': False,
    'UserB Test': False,
    'Author Automation': False,
    'Enduser Automation': False,
    'Test User1': False,
    'Test User2': False,
    'UserC Test' : False}

urlDict = {
    'global' : 'https://725release.assima.dev/Workspace/Project/Default.aspx?LocalizedItemId=17160&RootType=1',
    'users' : 'https://community-725release.assima.dev/Community/Users/Default.aspx',
    'testData': 'https://725release.assima.dev/Workspace/Project/Default.aspx?LocalizedItemId=25310&RootType=1',
    '725' : 'https://sts-727release.assima.dev/Pages/Email/Default.aspx',
    '727' : 'https://sts-725release.assima.dev/Pages/Email/Default.aspx'
}
global_Url = 'https://725release.assima.dev/Workspace/Project/Default.aspx?LocalizedItemId=17160&RootType=1'
users_Url = 'https://community-725release.assima.dev/Community/Users/Default.aspx'
testData_Url = 'https://725release.assima.dev/Workspace/Project/Default.aspx?LocalizedItemId=25310&RootType=1'
url727 = 'https://sts-727release.assima.dev/Pages/Email/Default.aspx'
url725 = 'https://sts-725release.assima.dev/Pages/Email/Default.aspx'

c = checker()
c.login(url725, creds)
# c.check_users()
#testDataDict = c.check_testData()
# project_list = c.get_projects()
# c.check_global(project_list.get('Global'))
dataDict = c.check_existance(testDataDict, testData_Url)
globDict = c.check_existance(globalDict, global_Url)
userDict = c.check_users(userDict)
pprint(dataDict)
pprint(globDict)
pprint(userDict)
if input('End (y/n)? ') == 'y':
    c.stop()
        
    

