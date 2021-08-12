# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 18:01:22 2021

@author: bingb
"""

import Linkedin_scraper as lk
import pandas as pd

chrome_driver_path = r"C:\Users\bingb\PycharmProjects\chromedriver.exe"


# Username, password, keywords of the job to search, location, num dataset

email = "bingbochen8@gmail.com"
password = "qeid6300bi"
keywords = "Data scientist"
location = "Italia"
num_dataset = 400


df = lk.get_job_posts(email, password, keywords, location, num_dataset, chrome_driver_path)

df.to_csv("linkedin_jobs.csv")