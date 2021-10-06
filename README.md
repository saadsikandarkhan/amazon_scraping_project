# Technical Challenge for the Global Overview

### Q1: Write a python selenium code that will extract the top 50 bestseller products.

1. Click on this [link](https://github.com/Saadkhansolo/amazon_scraping_project/blob/master/Use%20Cases.ipynb) which will take you to the use case demonstration of the amazon scraper.

2. Click on this [link](https://github.com/Saadkhansolo/amazon_scraping_project/blob/master/amazon_scraper.py) to look at the Amazon Web Scraper functions imported in the use case notebook.

### Q2: Steps to deploy and run code developed in quesition 1 on AWS lambda.

 All of these dependencies need to be packaged along with the function. We have few options to go about this, we can add custom lambda layers to include our selenium, boto3, pandas, bs4, and chrome headless dependencies or package all of this together using Serverless Framework. 

Once the dependencies are packages, we can get the data using the custom scrape function, add the date to the file name since this will run everyday and put it in S3 bucket using boto3:

 The lambda function would look like this:

 def handler(event, context):

    cur_dt = "{:%B %d, %Y}".format(datetime.datetime.now())

    ACCESS_KEY_ID = 'ENTER_KEY_HERE'
    ACCESS_SECRET_KEY = 'ENTER_SECRET_KEY_HERE'
    BUCKET_NAME = 'ENTER_DESTINATION_BUCKET_HERE'
    FILE_NAME = cur_dt + "ADD_LABEL_HERE.csv"

    links  = get_bestseller_links
    data = parsing_to_df_function(links[0])

    s3 = boto3.resource(
        's3',
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=ACCESS_SECRET_KEY,
        config=Config(signature_version='s3v4')
    )

    s3.Bucket(BUCKET_NAME).put_object(Key=FILE_NAME, Body=data)

### Q3: PostGres Task 

You can find the PostGres server notebook [here](https://github.com/Saadkhansolo/amazon_scraping_project/blob/master/PostGres%20Task.ipynb)
