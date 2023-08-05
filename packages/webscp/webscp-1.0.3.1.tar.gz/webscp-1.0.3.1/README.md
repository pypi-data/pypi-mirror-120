# Python Image Scraper

## Introduction

Python Image scrapper can help in gathering huge dataset of images for any custom keyword. This helps save time and gather unique images for any keyword. Gathered images will be uploaded to [anonfiles.com](https://anonfiles.com) and the link will be emailed to the user.

## Demo
![](static/images/demo.gif)

## Features

- Scraping Data in Multiple Threads 
- Auto Execute Project Anytime
- Uploads files to [anonfiles.com](https://anonfiles.com)
- Emails link after scraping images
- logs every action performed by scrapper

## Installation

### Using Docker
1\.  Clone the project using 
```sh
git clone https://github.com/govind2220000/image_scraper.git
``` 
2\.  Rename `example.config.ini` to `config.ini`. Fill it with appropriate values.

3\.  Build the project using Docker
```sh  
cd image_scraper
sudo docker-compose build
```   
4\.  Deploy the project
```sh 
sudo docker-compose up
```


### Using Python
1\. Clone the project using 
```sh
git clone https://github.com/govind2220000/image_scraper.git
```
2\. Install dependencies
```sh
cd image_scraper
pip install -r requirements.txt
```
3\. Run application
```sh
python3 -m src
```    
    

## Documentation Links
High Level Design Document : [View / Download](https://drive.google.com/file/d/1xWUd1qql4b25_gpqhOVHEoX8_NvHJaic/view?usp=sharing)

Low Level Design Document  : [View / Download](https://drive.google.com/file/d/1BO-RErAp7n9-cYCCm36wpSba0sOug4pd/view?usp=sharing)

Project Report             : [View / Download](https://drive.google.com/file/d/1YDMSYhX_ldxOHqkgJtY31nyVLZivBVWL/view?usp=sharing)

WireFrame Document         : [View / Download](https://drive.google.com/file/d/1IIiREJi5Jaa4wPbiQ2gAZkvDBF1q5PQ2/view)


## Authors
- [Govind Choudhary](https://github.com/govind2220000)
- [Sreejith Subhash](https://github.com/sjith7)
