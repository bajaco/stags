# scrape.py

scrape.py is a script that uses the Stags class to create a jobs feed in the terminal for Indeed job listings. Upon running you will be prompted to enter the search term, location, and time interval. At each interval it will list new jobs that have been added since the last interval. Intervals are not sychronized to time, so expect some drift. I have noticed some malformed titles- there is an error in the stags class that I need to investigate. The first request will get all matching listings, so make sure your search terms are specific. I recommend using specific search terms and a long interval time. If making a more general search edit the file and set FROMAGE to 0.

**Currently only accepts general search terms without special characters. A comma in the location is acceptable.**

#### Usage:

1. Install requests:
optionally make virtual environment:
- `python -m venv venv`
- `source venv/bin/activate`
Install requests: 
`pip install requests` or:
`pip install -r requirements.txt`
2. Run the script and follow prompts:
`python scrape.py`

# Stags

Stags is an in-progress HTML parser. It creates a tree representation of the document, and provides access to a list of all elements, which can be filtered and transformed.

## Usage

Example usage can be found in the scrape.py file.

To use:
1. Create necessary variables:
`url = 'https://www.indeed.com/jobs?q=python&l=remote&fromage=1'`
`agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0'`

2. Create a stags object
`stags = Stags(url, agent, 'get')`
Currently only 'get' is supported.

3. Transform list of tags. Examples:
- `stags.filter_attributes('href')`
Filters tags by those that have 'href' attribute.
- `stags.filter_tags('p')`
Filters tags by type 'p'
- `stags.ascend()`
Replaces tags with their parents, if a parent exists.
- `stags.descend()`
Gets all children of current tags.
- `stags.reset_query()`
Resets list to list of all elements in the document.
- `stags.query()`
Returns list of tags as filtered and modified by other operations

Each tag element has the following properties:

`tag.name`
`tag.contents`
`tag.attributes`
`tag.get_attribute(attribute)`, Which returns the value of an attribute, or None

Example:

    for t in stags.query():
        print(t.name)
        print('href={}'.format(t.get_attribute('href')
