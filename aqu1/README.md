## Overview of Spring 2019 Project for CS504 Data Mechanics. Please click on poster.pdf for a complete visual outline of the project or report.pdf for a summary of the project 

## Note: Please remove the "templates" folder and "makemap.py" from the aqu1 folder before running execute.py

## Question: How does proximity of T-stops to public schools and colleges affect education attainment? How does education attainment affect poverty across different communities in Boston? How can the city of Boston optimize T-stops to provide residents with better access to education?

## Datasets

Colleges and Universities within the City of Boston
http://bostonopendata-boston.opendata.arcgis.com/datasets/cbf14bb032ef4bd38e20429f71acb61a_2.csv

Boston Public Schools for 2018-2019 
http://bostonopendata-boston.opendata.arcgis.com/datasets/1d9509a8b2fd485d9ad471ba2fdb1f90_0.csv

Educational Attainment Demographics by Neighborhood from 1950 to 2010
https://data.boston.gov/dataset/8202abf2-8434-4934-959b-94643c7dac18/resource/bb0f26f8-e472-483c-8f0c-e83048827673/download/educational-attainment-age-25.csv

Information on Vulnerable Populations Throughout Boston (Low Income, People With Disabilities, People of Color, etc) from 2008-2012
http://bostonopendata-boston.opendata.arcgis.com/datasets/34f2c48b670d4b43a617b1540f20efe3_0.csv

MBTA T-Stops 
http://maps-massgis.opendata.arcgis.com/datasets/a9e4d01cbfae407fbf5afe67c5382fde_2.csv

## Transformations

1. First a new income dataset was created containing the percent of people who were below the poverty line and fell into the low income group across each neighborhood in Boston. All of the data across the tract codes for each of the 23 neighborhoods (each neighborhood has multiple tract codes) were then aggregated. A projection was then applied to create a new column for the proportion of people who are low income (people who were 100% below the poverty level and those who were 100–149% of the poverty level).

2. A new dataset for educational attainment for people ages 25+ throughout the different neighborhoods of Boston was created by first filtering for data in the 2000s decade. Data from the 2010s decade was not used because there was no data in the 2010s decade. A projection was then applied to remove the ‘%’ at the end of the values in the percent of population column in order to make calculations easier in the future.

3. A new dataset containing all of the MBTA train stops was created to include the coordinates of all T-stops within Boston. T-stops that weren't in Boston, such as those in Cambridge, Brookline, and Newton, were filtered out. The latitude and longitude columns were selected for in the MBTA train dataset. There are a total of 119 T-stops within Boston.

4. A new dataset containing all of the public schools and colleges was created to include the coordinates of all Boston public schools and colleges, along with the neighborhoods each school belonged to. The college dataset was first cleaned to only include 2 year community colleges, traditional 4-year colleges, and graduate schools. Any schools outside of Boston or with 0 students were deleted from the data. English learning center schools were deleted from the public schools dataset. Both the college and public school dataset were cleaned to make sure that the neighborhoods of the schools belonged to one of the 23 neighborhoods of Boston. The latitude, longitude, and neighborhood columns were selected for in both the public schools and colleges datasets and aggregated into a single dataset. There are a total of 166 schools across 18 neighborhoods after the data cleaning and aggregation.

## Statistical Analysis and Optimization

1. There was an interest in how the distance from T-stops to schools throughout Boston affected the percent of people who obtained a bachelor's degree or higher. There was also an interest in the relationship between the percent of people who obtained a Bachelor's Degree and the percent of people who were low income throughout Boston. Thus, a script was created to find the correlation between the average distance from a T-stop to a shool in each Boston neighborhood and the percent of people with a bachelor's degree or higher, as well as the correlation between the percent of people with a bachelor's degree or higher and the percent of people who were low income. The distance from each of the 119 T-stops to each of the 166 schools was calculated using a distance function that calculated the distance between two locations in kilometers based on the coordinates of those locations, which was then converted to miles. The mean distance from a T-stop in Boston to a school in a particular neighborhood was then calculated by applying the built-in pandas mean function to each neighborhood. The mean distance from a T-stop to a school in a particular neighborhood is a metric for how easily accessible schools within certain neighborhoods are by the T. The data was then merged with the education attainment data to create a stop to school distance and education attainment dataset. The income dataset was also merged with the education dataset to create an education attainment and percent low income dataset. The correlation coefficients and p-values for the two correlations were than generated using scipy.stats.pearsonr(x, y). The option to generate two plots of these correlations was implemented, but is currently commented out because running the plots prevents the rest of the code from running. If interested in the plots, please uncomment lines 113 and 122 in cocrrelation.py and exit each plot to continue running the code.

2. The correlation between the average distance from a T-stop in Boston to a school and the percent of people with a bachelor's degree or higher was about -0.48 and the p-value was about 0.04. This showed that there is a moderate relationship between these two variables and that the results are statistically significant since p < 0.05. Based on the correlation and p-value generated from the correlation script, the next step was to optimize T-stops throughout Boston to provide easier access for students to get to school. The K-means algorithm was chosen to be used to optimized T-stops because it will return the means of the closest cluster of stops to each of the schools. The optimization was done by first calculating the mean latitude and longitude of all the schools in each of the 18 neighborhoods that has schools. These are the initial centroids in the K-means algorithm that was used to fit all of the 119 T-stops. The resulting 18 centroids (list of coordinates) from the K-means algorithm are the optimized T-stops that are the closest to the mean locations of schools in each of the 18 neighborhoods.  

## Visualization
An interactive web map was created with Python Flask and the JavaScript Leaflet library to showcase the 18 optimized T-stops from the K-means algorithm. Data is retrieved from a MongoDB database for the Flask web application with a RESTful web API. Each neighborhood is color coded with a specific shade of green representing the percent of people who have a bachelor’s degree or higher. In the actual web map, users are able to float over neighborhoods in Boston to get more information on the average distance from a T-stop to a school, percent of people with a bachelor’s degree or higher, and the percent of people who are low income.
