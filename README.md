# Fetch Rewards Data Engineering ETL Challenge 

Welcome! This repository contains the solution for the Fetch Rewards Data Engineering ETL Challenge. I've created a Python program to fetch data from an AWS Simple Queue Service (SQS), apply some essential transformations (including data masking), and then store the processed data into a PostgreSQL database.


### Setup:

#### Prerequisites

You need to have Docker, Docker Compose, AWS CLI, AWS CLI Local, PostgreSQL, and Python installed on your machine.

1. [Python 3.7.9](https://www.python.org/downloads/release/python-379/): Ensure that you have this version of Python installed for compatibility.


2. Docker: [Install Docker for Mac OS, Windows, Linux](https://docs.docker.com/get-docker/ )
Follow the installation guide provided in the link above for your respective operating system.

3. Docker Compose:
    - Windows and macOS: Comes pre-installed with Docker.
    - Linux: Follow the official Docker Compose installation [guide](https://docs.docker.com/compose/install/).

4. AWS CLI: [Install AWS CLI](https://aws.amazon.com/cli/)

    
5. AWS CLI Local –- This can be installed using pip (Python package installer) run in your terminal. 
    ```
    pip install awscli-local
    ```
    After installing AWS CLI, you are required to configure it with your AWS credentials. Since you are using LocalStack, the access key and secret key don't have to be real. You can configure them with dummy values. Here's how you can configure it:

    ```
    aws configure
    ```
    And then enter dummy credentials as:
    
    ```
    AWS Access Key ID [None]: test
    AWS Secret Access Key [None]: test
    Default region name [None]: us-east-1
    Default output format [None]: json
    ```
    

6. Clone the Repository, 
    In your terminal, clone the repository by running:
    ```
   git clone https://github.com/Casual-Planet/Fetch_ETL.git
   ```

    Navigate to the project's root directory by:
    ``` 
   cd /path/to/your/Fetch_ETL
   ```

    Replace /path/to/your/Fetch_ETL with the correct path to the Fetch_ETL directory on your system.

    
7.  Next, you need to install the Python packages required for the project. These are specified in the requirements.txt file. Install them using the following command:
    ```
    pip install -r requirements.txt
    ```

## Starting the services

Start the Postgres and Localstack services using Docker Compose.

```
docker-compose up
```
You should see logs indicating that the services are starting. 


### Verify AWS Localstack
Open a new terminal window to leave the Docker Compose logs visible in the previous one. Check the Localstack service using AWS CLI Local. Run the following command in the terminal:

```
awslocal sqs receive-message --queue-url http://localhost:4566/000000000000/login-queue
```
You should see a JSON response representing a message from the queue, something like this:

```
{
    "Messages": [
        {
            "MessageId": "3c007da8-3ca5-4df6-8a78-9b0162d7db3b",
            "ReceiptHandle": "ODkxNmU3MmYtYzA1YS00NTk0LThkMDMtNGVlYjc3ZDdjMTA0IGFybjphd3M6c3FzOnVzLWVhc3QtMTowMDAwMDAwMDAwMDA6bG9naW4tcXVldWUgM2MwMDdkYTgtM2NhNS00ZGY2LThhNzgtOWIwMTYyZDdkYjNiIDE2OTEyNzE3NTQuOTc1NDQ2Nw==",
            "MD5OfBody": "e4f1de8c099c0acd7cb05ba9e790ac02",
            "Body": "{\"user_id\": \"424cdd21-063a-43a7-b91b-7ca1a833afae\", \"app_version\": \"2.3.0\", \"device_type\": \"android\", \"ip\": \"199.172.111.135\", \"locale\": \"RU\", \"device_id\": \"593-47-5928\"}"
        }
    ]
}

```

## Running the Application
The main application script is located in the `src` directory and named `main.py`. The `main.py` script is designed to process data from an Amazon Simple Queue Service (SQS) queue, apply transformations, and store it in a PostgreSQL database. The script performs data masking to protect sensitive information before storing it in the database.


To run the application, open a new terminal tab window (don't close the previous ones) 

Then, navigate to the src directory from Fetch_ETL
```
cd /path/to/your/Fetch_ETL/src
```
Run the script with the following command:

```
python main.py
```
When you run this script, it will start processing data from the SQS queue, apply transformations, and write it to the Postgres database. 


## Verify PostgreSQL

After the script successfully stores the data in the PostgreSQL database, you can verify the results. By connecting to the PostgreSQL database using the psql command, you can run the SQL query `SELECT * FROM user_logins;` to retrieve and view the records in the user_logins table. This verification step ensures that the processed and masked data is correctly stored in the database.

Connect to the PostgreSQL database and check the user_logins table
```
psql -d postgres -U postgres -p 5432 -h localhost -W

```

#### After entering the password  (postgres), run the following SQL command:

```
SELECT * FROM user_logins;
```
You should see the records of the user_logins table, something like this:
```
               user_id                | device_type |            masked_ip             |         masked_device_id         | locale | app_version | create_date 
--------------------------------------+-------------+----------------------------------+----------------------------------+--------+-------------+-------------
 424cdd21-063a-43a7-b91b-7ca1a833afae | android     | a56e7589b4b780605f7c614d13df6696 | 1237b6b78f6293ce2714d52b209eb3b4 | RU     |         230 | 
(1 row)

```
#### To exit the PostgreSQL prompt, type ```\q``` and press enter.

 
## Running Unit Tests

To ensure the integrity and functionality of the ETL process, we have included a suite of unit tests. Even though they weren't explicitly part of the original assessment, implementing these tests provides a safety net and helps ensure the application's robustness as we move forward with further development and improvements.


Navigate to the project's root directory by:
    
``` 
   cd /path/to/your/Fetch_ETL
   ```
   
Use the nosetests command followed by the directory containing the tests. In our case, this directory is named tests.

```
nosetests tests

```
You should expect an output similar to:

```
----------------------------------------------------------------------
Ran 5 tests in 0.231s

OK
```
This indicates that all 5 tests passed successfully. If there are any issues or failed tests, they will be highlighted in the output.



### Stopping Containers:
Executing the below command will halt and erase all the containers associated with the docker-compose.yml file.

```
docker-compose down
```


## Design Decisions


#### How will you read messages from the queue?

- The boto3 client, a well-documented and efficient AWS SDK for Python, is utilized to read messages from the AWS SQS Queue. To guarantee data integrity and avoid redundant processing, we follow a sequential approach. After the successful processing and storage of a message in the database, we ensure its removal from the queue to prevent reprocessing.
#### What type of data structures should be used?

- For managing the JSON data from the SQS messages, Python dictionaries have been chosen. Their key-value pair nature aligns perfectly with the structure of JSON data. Dictionaries offer simple, direct, and efficient methods to access, transform, and manipulate JSON-like structures.
#### How will you mask the PII data so that duplicate values can be identified?

- To ensure the confidentiality of PII (Personally Identifiable Information), we use Fernet symmetric encryption from the cryptography library. This method masks the ip and device_id fields, making the original data unreadable. However, one of the critical properties we maintain with this encryption method is consistency. This means that for a given input, the encrypted output will always be the same. This deterministic behavior ensures that even after masking, we can identify records with duplicate values.

- For instance, if two users have the same device_id, after encryption, their masked device_id fields will also be identical, enabling us to detect such duplicates.

- It's important to note that while this approach masks the data effectively, it retains the ability to decrypt it back to its original form if necessary, offering flexibility without compromising data privacy.
#### What will be your strategy for connecting and writing to Postgres?

- The psycopg2 library is our tool of choice to connect to the PostgreSQL database. This library is popular in the Python community for its capabilities and robust performance when interfacing with PostgreSQL. After the data undergoes all necessary transformations, each record is diligently committed to the user_logins table in the database to ensure data integrity and consistency.
#### Where and how will your application run?

- The application is designed to run on any machine with the necessary dependencies installed (Python, required libraries, and PostgreSQL). For easy deployment and scalability, one can also consider containerizing the application using Docker, enabling it to run in diverse environments consistently.

## Additional Questions
### Deploying in Production:

- Containerization and Cloud Deployment: Our application is container-ready, making use of Docker for containerization. This enables seamless deployments on cloud orchestration platforms like AWS ECS or Kubernetes, offering automated scaling and failover capabilities.
- Configuration Management: To protect sensitive data, we use environment variables to handle configurations, including database connections and encryption secrets. This not only ensures security but promotes easier configuration updates without direct code modifications.

### Production-Readiness:

- Robustness: We've incorporated advanced error-handling mechanisms to address unexpected issues, ensuring the system runs smoothly. Every exception or irregularity is meticulously logged, aiding diagnostics and troubleshooting.
-Testing: A suite of unit tests has been added even though it wasn't a requirement for the assessment. This underscores our commitment to best practices in software engineering. Through these tests, we can ensure code integrity, and any future enhancements or changes won't introduce unforeseen issues.
### Scaling Strategy:

- Parallel Processing: The application's architecture allows for concurrent processing. By deploying multiple instances—either distributed across machines or within separate containers—we achieve rapid, parallel data processing from the SQS queue.
### Data Privacy and Recovery:

- PII Handling: The privacy of Personally Identifiable Information (PII) is paramount. We mask PII using Fernet symmetric encryption. This approach not only protects the data but also allows for potential data recovery, provided the encryption key is available.
### Assumptions:

 - Data Integrity: We operate on the assumption that SQS messages adhere to the expected JSON format.
 - Database Infrastructure: A continuous, uninterrupted database connection is assumed, along with the presence of a correctly structured user_logins table.

## Additional Information
#### Unit Tests:
- Even though unit tests weren't explicitly mandated in the assignment, I deemed them necessary for a few reasons:
- Unit tests act as the first line of defense against potential regressions, ensuring that as we build or modify the codebase, we don't inadvertently introduce defects.
- Well-constructed tests serve as a form of documentation. They provide insight into the expected behavior of the application, demonstrating the way functions or methods are supposed to operate.
- With a robust suite of unit tests in place, refactoring or expanding the codebase becomes significantly safer. Tests provide the confidence to make changes without the fear of unknowingly disrupting existing functionality.








