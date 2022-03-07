from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
import json

class EasyApplyLinkedin:

    def __init__(self, data):
        """Parameter initialization"""

        self.email = data['email']
        self.password = data['password']
        self.keywords = data['keywords']
        self.location = data['location']
        self.driver = webdriver.Chrome(data['driver_path'])

    def clr(self,rate):
        time.sleep(rate)
        os.system("clear")

    def login_linkedin(self):
        self.clr(0)
        print("LOGGING IN TO LINKEDIN with " + self.email + "\n\n")
        #This function logs into your personal LinkedIn profile
        # go to the LinkedIn login url
        self.driver.get("https://www.linkedin.com/login")
        # introduce email and password and hit enter
        login_email = self.driver.find_element_by_name('session_key')
        login_email.clear()
        login_email.send_keys(self.email)
        login_pass = self.driver.find_element_by_name('session_password')
        login_pass.clear()
        login_pass.send_keys(self.password)
        login_pass.send_keys(Keys.RETURN)
        self.clr(0)
        print("LOGIN COMPLETE\n\n")






    
    def job_search(self):
        self.clr(0)
        print("SEARCHING FOR " + self.keywords + " positions in " + self.location)
        #This function goes to the 'Jobs' section a looks for all the jobs that matches the keywords and location
        # go to Jobs
        jobs_link = self.driver.find_element_by_link_text('Jobs')
        jobs_link.click()
        self.clr(2)
        # search based on keywords and location and hit enter
        #search_keywords = self.driver.find_element_by_tag_name("input")
        search_keywords = self.driver.find_element_by_css_selector("[aria-label='Search by title, skill, or company']")
        search_keywords.clear()
        search_keywords.send_keys(self.keywords)
        self.clr(2)
        search_location = self.driver.find_element_by_css_selector("[aria-label='City, state, or zip code']")
        search_location.clear()
        search_location.send_keys(self.location)
        self.clr(2)
        search_location.send_keys(Keys.RETURN)
        self.clr(0)
        print("JOB SEARCH COMPLETE\n\n")










    def filter(self):
        self.clr(0)
        print("APPLYING EASY APPLY FILTER\n\n")
        self.clr(5)
        easy_apply_button = self.driver.find_element_by_css_selector("[aria-label='Easy Apply filter.']")
        easy_apply_button.click()
        self.clr(2)
        print("EASY APPLY FILTER COMPLETE\n\n")










    def find_offers(self):
        self.clr(2)
        print("FINDIN OFFERS")
        """This function finds all the offers through all the pages result of the search and filter"""
        # find the total amount of results (if the results are above 24-more than one page-, we will scroll trhough all available pages)
        total_results = self.driver.find_element_by_class_name("display-flex.t-12.t-black--light.t-normal")
        
        total_results_int = int(total_results.text.split(' ',1)[0].replace(",",""))
        print(total_results_int)

        time.sleep(2)
        # get results for the first page
        current_page = self.driver.current_url
        results = self.driver.find_elements_by_class_name("occludable-update.artdeco-list__item--offset-4.artdeco-list__item.p0.ember-view")

        # for each job add, submits application if no questions asked
        for result in results:
            hover = ActionChains(self.driver).move_to_element(result)
            hover.perform()
            titles = result.find_elements_by_class_name('job-card-search__title.artdeco-entity-lockup__title.ember-view')
            print(titles)
            for title in titles:
                self.submit_apply(title)

        # if there is more than one page, find the pages and apply to the results of each page
        if total_results_int > 24:
            time.sleep(2)

            # find the last page and construct url of each page based on the total amount of pages
            find_pages = self.driver.find_elements_by_class_name("artdeco-pagination__indicator.artdeco-pagination__indicator--number")
            total_pages = find_pages[len(find_pages)-1].text
            total_pages_int = int(re.sub(r"[^\d.]", "", total_pages))
            get_last_page = self.driver.find_element_by_xpath("//button[@aria-label='Page "+str(total_pages_int)+"']")
            get_last_page.send_keys(Keys.RETURN)
            time.sleep(2)
            last_page = self.driver.current_url
            total_jobs = int(last_page.split('start=',1)[1])

            # go through all available pages and job offers and apply
            for page_number in range(25,total_jobs+25,25):
                self.driver.get(current_page+'&start='+str(page_number))
                time.sleep(2)
                results_ext = self.driver.find_elements_by_class_name("disabled.ember-view.job-card-container__link.job-card-list__title")###############HERRE
                print(page_number,"out of",total_jobs) 
                
                for result_ext in results_ext:
                    hover_ext = ActionChains(self.driver).move_to_element(result_ext)
                    hover_ext.perform()
                    titles_ext = result_ext.find_elements_by_class_name('job-full-width artdeco-entity-lockup__title.ember-view')
                    for title_ext in titles_ext:
                        self.submit_apply(title_ext)
                        print("App submitted.")
        else:
            self.close_session()
        








    def submit_apply(self,job_add):
        """This function submits the application for the job add found"""
        self.clr(2)
        print('You are applying to the position of: ', job_add.text)
        job_add.click()
        time.sleep(5)
        
        # click on the easy apply button, skip if already applied to the position
        try:
            in_apply = self.driver.find_element_by_xpath("//button[@data-control-name='jobdetails_topcard_inapply']")
            in_apply.click()
        except NoSuchElementException:
            print('You already applied to this job, go to next...')
            pass
        time.sleep(1)

        # try to submit if submit application is available...
        try:
            submit = self.driver.find_element_by_xpath("//button[@data-control-name='submit_unify']")
            submit.send_keys(Keys.RETURN)
        
        # ... if not available, discard application and go to next
        except NoSuchElementException:
            print('Not direct application, going to next...')
            try:
                discard = self.driver.find_element_by_xpath("//button[@data-test-modal-close-btn]")
                discard.send_keys(Keys.RETURN)
                time.sleep(1)
                discard_confirm = self.driver.find_element_by_xpath("//button[@data-test-dialog-primary-btn]")
                discard_confirm.send_keys(Keys.RETURN)
                time.sleep(1)
            except NoSuchElementException:
                pass

        time.sleep(1)

    def close_session(self):
        """This function closes the actual session"""
        
        print('End of the session, see you later!')
        self.driver.close()

    def apply(self):
        """Apply to job offers"""
        self.driver.maximize_window()
        self.login_linkedin()
        self.job_search()
        self.filter()
        self.find_offers()
        self.close_session()


if __name__ == '__main__':
    import os
    os.system("clear")
    with open('/Users/Yousefmacer/github/automation/EasyApply-Linkedin/config.json') as config_file:
        data = json.load(config_file)

    bot = EasyApplyLinkedin(data)
    bot.apply() 