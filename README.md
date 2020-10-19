# stags

Stags is an HTML parser in progress. My initial goal was to make an Indeed.com scraper to commit new Python-related jobs to a database every hour or so, and display the newest job openings whenever I query it.

To do that I needed a web scraper, and rather than using Beautiful Soup I decided to try to implement one of my own.

In the process I decided I'd like to represent the HTML document as a tree, so I implemented a class that builds trees out of submitted objects.


