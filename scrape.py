from stags import Stags

url = 'https://www.indeed.com/jobs?q=python&l=remote&fromage=1'
agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0'
stags = Stags(url, agent, 'get')

stags.filter_attributes('data-jk')
job_codes = [e.attributes['data-jk'] for e in stags.query()]
stags.descend()
stags.descend()
stags.filter_tags('a')

[print(e.get_attribute('href')) for e in stags.query()]
