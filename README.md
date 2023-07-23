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
3. Configure AWS credentials (Need to do inspite of local stack to avoid connection issues) \
Run following commands
  ```
  aws configure set profile.default.aws_access_key_id temp_key
  aws configure set profile.default.aws_secret_access_key temp_secret_key
  aws configure set profile.default.region us-east-1
  ```
5. Run ```make``` commands from Makefile to install dependencies
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

### Steps to access Postgres Database and check results
1. Execute the following command
  ```
  psql -d postgres -U postgres -p 5432 -h localhost -W
  ```
Note: Credentials for postgres database are
* username=postgres
* password=postgres
2. Execute following query via postgres connection
  ```
  postgres=# select * from user_logins;
  ```
  
