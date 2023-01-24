# Airport Analysis: Time Series and Forecasting of future delays

## Content:
This dataset is a subset of a bigger one that contains daily airline information covering from flight information, carrier company, to taxing-in, taxing-out time, and generalized delay reason of exactly 10 years, from 2009 to 2019. Information was collected and managed by the DOT - Bureau of Transportation Statistics (https://www.bts.gov/). 

For the purposes of this project, the data was gathered from a Kaggle repository (https://www.kaggle.com/datasets/sherrytp/airline-delay-analysis) and limited to three years (2016, 2017, 2018) for the following  airports:
- Hartsfield-Jackson Atlanta International Airport - ATL
- Los Angeles International Airport - LAX
- John F. Kennedy International Airport - JFK

## Dataset overview: 
This dataset has a total of 2.080.873 entries and 12 columns. 
- FL_DATE: Flight date
- OP_CARRIER: Carrier code
- ORIGIN: Departing airport     
- DEST: Destination airport      
- CRS_DEP_TIME: Scheduled departure time       
- DEP_TIME: Actual departing time  
- DEP_DELAY: Difference between Scheduled and Actual departing time     
- CRS_ARR_TIME: Scheduled arrival time      
- ARR_TIME: Actual arrival time      
- AIR_TIME: Flight time    
- DISTANCE: Miles covered    
- AIRLINE: Airline commercial name
