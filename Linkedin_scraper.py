# -*- coding: utf-8 -*-
"""
Bingbo Chen
"""
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from datetime import date

# pass the actual page and all the pagebar in webelement and click on the next page 
def change_page (active, page_bar):
    
    for page in page_bar:
        # find the num of the actual page 
        num_page = page.find_element_by_tag_name("span").text
        print(num_page)
        if num_page == "…":
            page.click()
            return
        elif active < int(num_page) :
            page.click()
            return
    


def get_job_posts(email, password, keywords, location,num_dataset,chrome_driver_path):
    driver = webdriver.Chrome(executable_path=chrome_driver_path)
    driver.get('https://www.linkedin.com/login')
    driver.maximize_window()
    time.sleep(2)
    
    # Login 
    driver.find_element_by_id('username').send_keys(email)
    driver.find_element_by_id('password').send_keys(password)
    driver.find_element_by_id('password').send_keys(Keys.RETURN)
    time.sleep(2)
    
    
    driver.get("https://www.linkedin.com/jobs/")
    time.sleep(2)
    # find the keywords/location search bars:
    search_bars = driver.find_elements_by_class_name('jobs-search-box__text-input')
    
    #search keyword
    search_keywords = search_bars[0]
    search_keywords.send_keys(keywords)
    time.sleep(2)
    #search location
    search_location = search_bars[3]
    search_location.send_keys(location)
    enter = driver.find_element_by_class_name("jobs-search-box__submit-button")
    driver.execute_script("arguments[0].click();", enter)
    time.sleep(2)
    
    # get a list of all the listings elements's in the side bar
    
    
    dates = []
    positions = []
    companies = []
    locations = []
    descriptions = []
    pasts_time = []
    candidates = []
    work_times = []
    experience_needs = []
    employees = []
    job_categories = []
    
    
    j = 0
    
    #loop until we reach the num dataset 
    while j < num_dataset:
    # scrolls a single page:
        #select all job offer in the single page
        list_items = driver.find_elements_by_class_name("occludable-update")
        for job in list_items:
            
            # if reach the num_dataset then exit 
            if j >= num_dataset : 
                break
            
            
            try:
                lenght_link = len(job.find_element_by_class_name("job-card-container__company-name").text)
            except NoSuchElementException:
                lenght_link = 0
            
            #for lengh > 28 selenium will click on the link because inside the job
            #So we avoid it and skip the job offer if this parameter is >28
            if lenght_link < 28:
                
                j += 1
                print(f"Processing data: {j}/{num_dataset}")
                # executes JavaScript to scroll the div into view
                driver.execute_script("arguments[0].scrollIntoView();", job)
                job.click()
                time.sleep(5)
                
                # get info:
                [position, company, location] = job.text.split('\n')[:3]
                positions.append(position)
                companies.append(company)
                locations.append(location)
                
                
                past_time = driver.find_element_by_class_name("jobs-unified-top-card__posted-date").text
                pasts_time.append(past_time)
                
                try:
                    candidate = driver.find_element_by_class_name("jobs-unified-top-card__applicant-count").text
                    candidates.append(candidate)
                except NoSuchElementException:
                    candidate = driver.find_element_by_class_name("jobs-unified-top-card__bullet").text
                    candidates.append(candidate)
                
                try:
                    description = driver.find_element_by_id("job-details").text
                    descriptions.append(description)
                except NoSuchElementException:
                    description = "na"
                    descriptions.append(description)
                
                job_insight = driver.find_elements_by_class_name("jobs-unified-top-card__job-insight")
                
                if len(job_insight) == 0:
                    time.sleep(20)
                    job_insight = driver.find_elements_by_class_name("jobs-unified-top-card__job-insight")
                
                work_time = job_insight[0].text.split("·")[0]
                work_times.append(work_time)
                
                try:
                    experience_need = job_insight[0].text.split("·")[1][1:]
                    experience_needs.append(experience_need)
                except IndexError:
                    experience_need = "na"
                    experience_needs.append(experience_need)
                    
                employee = job_insight[1].text.split("·")[0]
                employees.append(employee)
                try:    
                    job_category = job_insight[1].text.split("·")[1][1:]
                    job_categories.append(job_category)
                except IndexError:
                    job_category = "na"
                    job_categories.append(job_category)
                
                dates.append(date.today())
                time.sleep(2)
        
        if j < num_dataset : 
            active = int(driver.find_element_by_class_name("active").find_element_by_tag_name("span").text)
            page_bar = driver.find_elements_by_class_name("artdeco-pagination__indicator--number")
            change_page(active, page_bar)
            time.sleep(2)
    
    print(dates)
    jobs = {
            "Date" : dates,
            "Companies name": companies,
            "Type of company": job_categories,
            "Description": descriptions,
            "N. employees": employees,
            "Experience need": experience_needs,
            "Post time": pasts_time,
            "Position" : positions,
            "Location": locations,
            "Full-time": work_times,
            }
    return pd.DataFrame(jobs)




