## Solutions to questions about the application:


**1. How would you deploy this application in production?**
  * Setup a cloud based infrastructure as production environment. AWS, GCP, Azure are the common ones
  * As done in this assignment, ensure containeriztion which provides consistency and portability across different environments
    
**2. What other components would you want to add to make this production ready?**
  * Ensure data quality checks to analyse data drift and for maintaining data schema
  * Use job scheduling tools such as Airflow to automate the ETL pipeline at regular intervals
  * If dataset table will be growing horizontally, partition and normalize database to improve query performance.
  * Conduct load testing to assess the application's performance under varying workloads and identify potential bottlenecks.
  * Use a secure key management system to manage encryption keys and other sensitive credentials.
        
**3. How can this application scale with a growing dataset?**
  * Horizontal scaling :
    * Deploy the application on multiple servers or virtual machines to distribute the data processing workload.
    * Use load balancers to distribute incoming requests across the application instances.
    * As the dataset grows, add more application instances to the cluster to handle increased data processing demands.
  * Vertical scaling :
    * Depending on the dataset's size and growth rate, consider using scalable storage solutions like Amazon RDS (for AWS) or Google Cloud SQL.  

**4. How can PII be recovered later on?**
  * Since we use base64 encryption which is recoverable, we can get the original PII from a masked PIIs.
  * Execute following command to get original PIIs from any masked PII
    ```
    echo -n "<sample_base64_encrypted_string>" | base64 --decrypt
    ```
    
**5. What are the assumptions you made?**
  * Encryption needed needs to be reversible therefore, ```base64``` encryption was used for masking PIIs
  * ```app_version``` field needs to be of type ```VARCHAR``` to ensure smooth loading of data. Converting it into type ```INTEGER``` is not possible as \
    versions cannot be typecasted into Integers. Therefore, Table needed to be altered.
  * If ```device_id``` or ```ip``` are absent from a message, ignore the message as it won't contribute to any information.
  * Data type and schema is consistent across messages.
