from stags import Stags
import datetime
import time

INTERVAL = int(input('Search interval in seconds: '))
SEARCH = input('Search term: ')
LOCATION = input('Location, e.g. remote: ')

def querify(term):
    chars = []
    for c in term:
        if c == ' ':
            chars.append('+')
        elif c == ',':
            chars.append('%2C')
        else:
            chars.append(c)
    return ''.join(chars)

jobs = {}


def search(jobs, SEARCH, LOCATION):
    SITE =  'https://www.indeed.com'
    SEARCH = querify(SEARCH)
    LOCATION = querify(LOCATION)
    START = 0
    FROMAGE = 1
    agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0'
    new_jobs = {}
    searching = True
    while searching:
        previous_job_count = len(new_jobs)
        url = SITE + '/jobs?q={}&l={}&sort=date&filter=0&fromage={}&start={}'.format(
                SEARCH,LOCATION,FROMAGE,START)
        print(f'Requesting jobs from {url}.')
        stags = Stags(url, agent, 'get') 
        stags.filter_attributes('data-jk')
        job_codes = [e.attributes['data-jk'] for e in stags.query()]
        stags.descend()
        stags.descend()
        stags.filter_tags('a')
        job_titles = [e.contents for e in stags.query()]
        job_links = [e.get_attribute('href') for e in stags.query()]
        for i,v in enumerate(job_codes):
            if v not in jobs:
                job = {'title': job_titles[i].replace('\n',''), 'link': SITE + job_links[i]}
                new_jobs[v] = job
        START += 10
        if previous_job_count == len(new_jobs):
            searching = False

    print('----------------------------------------------------------------------------')
    if len(new_jobs) > 0:
        for job in new_jobs.items():
            print('{}: {}'.format(job[1]['title'],job[1]['link']))
            print('\n')
    job_term = 'jobs'
    if len(new_jobs) == 1:
        job_term = 'job'
    print(f'{len(new_jobs)} new {job_term} at {datetime.datetime.now()}.')
    print('----------------------------------------------------------------------------')
    jobs.update(new_jobs) 

while True:
    start_time = time.time()
    search(jobs,SEARCH,LOCATION)
    diff = round(time.time() - start_time)
    time.sleep(INTERVAL - diff)

