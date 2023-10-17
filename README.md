# webScrape
 web scraping listings from a site with scrapy
## How to Run: 
``` bash
 docker-compose build
 docker-compose up
```
go to: 
http://localhost:8080/

IMPORTANT: Might still be some bugs, specifically with creating the database tables and the pipeline surounding it.
You might need to do 
``` bash
 docker-compose down
 docker-compose build
 docker-compose up
```
again for it to work.(using a .sql file with compose was troublesome so i just used the sql in the scraper to create the table if it doesnt exists, therefore at the first build the database will not have the table and the program will crash)
I will fix this
