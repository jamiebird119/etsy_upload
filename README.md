# Etsy Shop Upload script

Here is a script designed to upload multiple products to the Etsy shop. This file is designed to be run locally with the corresponding driver executable. 


## Installation 

+ First install dependencies from requirements file using command:

 py -m pip install -r requirements.txt

+ Now ensure that the chromedriver is correct for your OS and version of windows chrome. New versions can be found at:

https://chromedriver.chromium.org/downloads

NOTE: You can check your version of chrome by clicking the  3 dots in the top right and going to HELP > About Google Chrome 

+ Now enter your username on line 216 and password on line 224 where prompted.

+ Ensure that the product_info.csv is updated with files you wish to upload - see below for full details.

+ Ensure any image files are placed in the Images folder with names that match the .csv file.

+ Prices are currently added using the prices.csv file for easy changability. Ensure at least 1 set of values exists here. 

+ Once all files are correctly added run with command:

py -m upload

NOTE Commands set up for PyCharm, but may differ with different IDE's. See documentation for corresponding commands. 

## Product_info.csv management

This file can easily be exported from google sheets, however the format has to match the example and parameters set out below.

Fields are listed below with formats (if not stated then field is required for script to work). Line 1 in product_info.csv should contain headers with each product taking up one line and capitalised. Omit optional fields if not applicable (i.e. do not put blanks in).

+ Image - list
+ Title - string
+ Category - string
+ Description - string
+ Tags (opt) - list (will be appended to default values)
+ Quantity - int
+ SKU - string
+ Room (opt) - list (will replace defaults)
+ Subject (opt) - list (will replace defaults)

### Concerning lists

Where list formats can be used, the correct format for this is
"option1/option2/option3" with no spaces and only a '/' separating values. For image documents ensure filenames contain filetypes (.png, .jpg, etc)


### Google captcha

This script, is not set up to deal with google captchas. If one occurs (only happened once in testing after repeate logins) please wait 24 hours. An update to handle this may be added in later versions. 







 
