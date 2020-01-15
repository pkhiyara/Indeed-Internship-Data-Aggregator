# Imported the following libraries: requests, BeautifulSoup from bs4, pandas, re and time

import requests
import time
import pandas
import re
from bs4 import BeautifulSoup

# Set a limit on the max number of results to return to reduce the script's run time
max_results_per_query = 100

# Created a list of columns to use
columns = ["Job Title", "Company", "City", "Description", "Days On Indeed", "URL"]

# Created a pandas dataframe that uses the columns present in the columns variable
indeedjobsdf = pandas.DataFrame(columns=columns)

# Created a list of strings for the query
query_set = ["data+scientist+internship", "data+analyst+internship", "data+scientist+intern", "data+analyst+intern", "data+science", "data+analyst"]

# Created a for loop to search Indeed for job listings based on each query within the query_set
for query in query_set:
    # Advanced through the results pages by starting at 0 up to the preset limit, and aggregating by the number of non-sponsored jobs displayed on each results page on the website
    for start in range(0, max_results_per_query, 10):
        # Created a GET HTTP request to the page using concatenation to incorporate varying components already saved as variables
        page = requests.get("http://www.indeed.com/jobs?q=" + str(query) + "&l=Washington+DC&sort=date&start=" + str(start))

        # Wait 1 second between each query to prevent being blocked for bot activity
        time.sleep(1)

        # Initiated the results page for aggregating through the BeautifulSoup package
        soup = BeautifulSoup(page.text, "html.parser")

        # Created another for loop iterating through divs with class attributes for each job post's details
        for div in soup.findAll("div", class_="jobsearch-SerpJobCard"):
            # Gave each row in the dataframe a unique identifying number
            num = (len(indeedjobsdf) + 1)
            # Initiated a list to assemble details for each job post
            job_post = []
            # Found the job title from the post for the Job Title column
            titletable = div.find("a", class_="turnstileLink")
            title = titletable.text
            title = title.strip()
            # Appended the job title to the job post listing
            job_post.append(title)
            # Found the company name for the Company column
            try:
                companylink = div.find("span", class_="company")
                companytext = companylink.text
                company = companytext.replace("\n", "")
                company = company.strip()
            except Exception:
                company = "Error"
            # Appended the company to the job post listing
            job_post.append(company)
            # Found the location of the job for the City column
            locationlong = soup.find("div", class_="location")
            location = locationlong.text
            # Appended the location to the job post listing
            job_post.append(location)
            # Found the job's description for the Description column
            summary = div.find("div", class_="summary").findAll("li")
            if summary:
                description = summary[0].text
                for line in summary[1:]:
                    description = description+ " "+line.text
                description = description.strip()
            else:
                description = "N/A"
            # Appended the description to the post
            job_post.append(description)
            # Found the number of days it has been since the listing was published onto Indeed for the Days On Indeed column
            days = div.find(name="span", class_="date")
            # Used regex to capture only the numeric element from the number of days it has been since the listing was published onto Indeed detail
            days = re.search("\d+\+?", days.text)
            if days:
                days = days.group()
            else:
                days = 0
            # Appended the number of days to the job post listing
            job_post.append(days)
            # Found a hyperlink for the job ad for URL column
            url = 'www.indeed.com' + div.find('a')['href']
            # Appended the hyperlink to the job post listing
            job_post.append(url)
            # Inserted the job_post list as a row into the indeed jobs dataframe at the unique row number defined above
            indeedjobsdf.loc[num] = job_post

# Saved the dataframe as a CSV file
indeedjobsdf.to_csv("/IndeedInternships.csv", encoding="utf-8")
