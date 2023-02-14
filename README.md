# GRAPHEE Scrapy spiders

## requirements
The required libs to launch those spiders are listed in requirements.txt, to install requirements, type : 
- pip install -r requirements.txt


## Server configuration
The SCRAPY server configuration is explained in this online document : \
https://docs.google.com/document/d/1p-lruxefIVEnUJz8PBTf9trCgZZYr72Y/edit?usp=sharing&ouid=104509825818607965272&rtpof=true&sd=true

## Files tree
for each client (one or more bots) there is a dedicated project (folder) so that it is possible to configure behaviour, outputs ... for this specific client

├───project 1                                
│####├───project 1                      
│####│####├───items.py                    
│####│####├───middleware.py                    
│####│####├───pipelines.py                    
│####│####├───settings.py                    
│####│####└───spiders   
│####│####│####├───spider1.1.py                    
│####│####│####├───spider1.2.py   
│####└───scrapy.cfg  
├───project 2                                
│####├───project 2                      
│####│####├───items.py                    
│####│####├───middleware.py                    
│####│####├───pipelines.py                    
│####│####├───settings.py                    
│####│####└───spiders   
│####│####│####├───spider2.1.py                    
│####│####│####├───spider2.2.py   
│####└───scrapy.cfg  

## Creating a new project
To create a new project you can (and should) use existing template  
```scrapy startproject -s TEMPLATES_DIR=templates {project_name}```

## Creating a new spider
To create a new spider you can (and should) use existing template, inside project folder type :  
```scrapy genspider -t classic {spider_name} {domain}```  
or  
```scrapy genspider -t sitemap {spider_name} {domain}```


## todo
- create project and spider templates
- update scrapy server directly from git repo

