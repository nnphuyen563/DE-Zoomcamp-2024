-- Create a non partitioned table from external table
CREATE OR REPLACE TABLE de-zoomcamp-411818.green_taxi_2022_hw_3.green_taxi_2022_no_partition AS
SELECT * 
FROM de-zoomcamp-411818.green_taxi_2022_hw_3.external_green_taxi_2022;


--Question 1. What is count of records for the 2022 Green Taxi Data?
SELECT * 
FROM de-zoomcamp-411818.green_taxi_2022_hw_3.green_taxi_2022_no_partition


--Question 2. What is the estimated amount of data in the tables?
--MATERIALIZED TABLE
SELECT COUNT(DISTINCT PULocationID)
FROM de-zoomcamp-411818.green_taxi_2022_hw_3.green_taxi_2022_no_partition


--EXTERNAL TABLE
SELECT COUNT(DISTINCT PULocationID)
FROM de-zoomcamp-411818.green_taxi_2022_hw_3.external_green_taxi_2022


--Question 3. How many records have a fare_amount of 0?
SELECT COUNT(*)
FROM de-zoomcamp-411818.green_taxi_2022_hw_3.green_taxi_2022_no_partition
WHERE fare_amount = 0


--CREATE A NEW TABLE WITH TIMESTAMP
CREATE TABLE IF NOT EXISTS de-zoomcamp-411818.green_taxi_2022_hw_3.green_taxi_2022
AS    
SELECT *, 
  TIMESTAMP_MICROS(lpep_pickup_datetime) as lpep_pickup_datetime_fmt,
  TIMESTAMP_MICROS(lpep_dropoff_datetime) as lpep_dropoff_datetime_fmt 
FROM de-zoomcamp-411818.green_taxi_2022_hw_3.green_taxi_2022_no_partition


-- Question 4. What is the best strategy to make an optimized table in Big Query?
CREATE OR REPLACE TABLE de-zoomcamp-411818.green_taxi_2022_hw_3.green_taxi_2022_partition_cluster
PARTITION BY DATE(lpep_pickup_datetime_fmt)
CLUSTER BY PUlocationID AS
SELECT * 
FROM de-zoomcamp-411818.green_taxi_2022_hw_3.green_taxi_2022;


--Question 5. What's the size of the tables?
--Non-partitioned
SELECT DISTINCT(PULocationID)
FROM de-zoomcamp-411818.green_taxi_2022_hw_3.green_taxi_2022
WHERE DATE(lpep_pickup_datetime_fmt) BETWEEN '2022-06-01' AND '2022-06-30';


--Partitioned and cluster
SELECT DISTINCT(PULocationID)
FROM de-zoomcamp-411818.green_taxi_2022_hw_3.green_taxi_2022_partition_cluster
WHERE DATE(lpep_pickup_datetime_fmt) BETWEEN '2022-06-01' AND '2022-06-30';

