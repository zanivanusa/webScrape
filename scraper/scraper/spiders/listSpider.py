import scrapy
import psycopg2
from scrapy.signalmanager import dispatcher
from scrapy import signals


class ListspiderSpider(scrapy.Spider):
    name = "listSpider"
    allowed_domains = ["www.sreality.cz"]
    
    #the content is dynamically loaded so i need to access the api instead of scraping html
    #i got to this url by watching the netwrok activity when loading the site.
    start_urls = ["https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&per_page=500&tms=1697472040323"]
    
    
    #had to do this, for some reason open and close spider were not getting called
    def __init__(self, *args, **kwargs):
        super(ListspiderSpider, self).__init__(*args, **kwargs)
        
        dispatcher.connect(self.open_spider, signals.spider_opened)
        dispatcher.connect(self.close_spider, signals.spider_closed)
            
    def open_spider(self, spider):
        try:
            print("Opening spider with signals...")
            self.connection = psycopg2.connect(database="webScrapeListing", user="postgres", password="pass", host='db', port='5432')
            self.cursor = self.connection.cursor()

            # Create the listings table if it doesn't exist
            create_table_query = """
            CREATE TABLE IF NOT EXISTS listings (
                id SERIAL PRIMARY KEY,
                locality TEXT,
                name TEXT,
                price TEXT,
                image_urls TEXT
            );
            """
            self.cursor.execute(create_table_query)
            self.connection.commit()
            
            #lets also delet the previous data in the table to refresh it with new listings
            #there is probably a better way to do this maybe without using volumes. but for now i think this will do
            
            delete_all_records_query = "DELETE FROM listings;"
            self.cursor.execute(delete_all_records_query)
            self.connection.commit()

        except psycopg2.OperationalError as e:
            print(f"Error while connecting to PostgreSQL: {e}")
            raise e



    def close_spider(self, spider):
        print("closing spider using signals...")
        self.connection.commit()
        self.connection.close() 
    
    
    def parse(self, response):
        #the content is saved in the response and we store it as json
        json_data = response.json()
        
        #the listings are nested in here
        estates = json_data['_embedded']['estates']  # Extract the 'estates' list

        for estate in estates:  # Loop through each estate
            
            #locality is acting a bit weird. its not the same as in the api call
            locality = estate.get('locality', 'N/A')  # Extract the 'name', default to 'N/A' if not found
            #only th name for the title seemed too little so i also took localitgy and price
            size=estate.get('name','N/A')
            price=estate.get('price','N/A')
            
            # Extract the first image URL, default to 'N/A' if not found
            image_urls = estate['_links'].get('images', [{'href': 'N/A'}])[0]['href']
           
            #or get every image            
            #image_urls = estate['_links'].get('images', [{'href': 'N/A'}])


            #if we want all images of a listing: 
            all_images=[]

           # for img in image_urls:  # Loop through each image object in the list
            #    image_url = img.get('href', 'N/A')
             #   #and store all images in one place 
                #im guessing that from the api call we only get some pictures and the rest are loaded later
              #  all_images.append(image_url)
                
            # Insert data into PostgreSQL
            #print("locality is: ",locality)
            self.cursor.execute(
                "INSERT INTO listings (locality, name, price, image_urls) VALUES (%s, %s, %s, %s)",
                (locality, size, price, image_urls)
            )            
            self.connection.commit()

            #print(f"locality: {locality}")
            #print(f"name: {name}")
            #print(f"price: {price} Kč")
            #print(f"Image URL: {all_images}")
