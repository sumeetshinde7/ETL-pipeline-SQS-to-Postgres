# Fetch-DataEngineer challenge

## ETL from a SQS queue to a Postgres Database

### Steps to run the code
1. Clone this repository
  ```
  git clone https://github.com/sumeetshinde7/Fetch-DataEngineer.git
  ```
2. Change directory
  ```
  cd Fetch-DataEngineer
  ```
3. Run ```make``` commands from Makefile to install dependencies
  ```
  make pip-install
  ```
4. Run ```make``` commands from Makefile to start docker and run images
  ```
  make start-docker
  ```  
5. Run ```make``` commands from Makefile for ETL process
  ```
  make perform-etl
  ```
