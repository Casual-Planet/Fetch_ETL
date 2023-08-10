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
### Verify to check if the Postgres table is empty 

```
psql -d postgres -U postgres -p 5432 -h localhost -W
```
After entering the password  (postgres), run the following SQL command:

```
SELECT * FROM user_logins;
```
You should see the records of the user_logins table, something like this:

```
 user_id | device_type | masked_ip | masked_device_id | locale | app_version | create_date 
---------+-------------+-----------+------------------+--------+-------------+-------------
(0 rows)


```
#### To exit the PostgreSQL prompt, type ```\q``` and press enter.

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




### Stopping Containers:
Executing the below command will halt and erase all the containers associated with the docker-compose.yml file.

```
docker-compose down
```


## Design Decisions
#### How will you read messages from the queue?
- To interact with AWS SQS, we utilize the boto3 client in our sqs_client.py script. Messages are read in batches of up to 10, as specified by the MaxNumberOfMessages parameter in the get_messages_from_queue function. This ensures efficient processing while reducing the number of API calls. The sequence we follow ensures that a message is processed and inserted into the database successfully before it's deleted from the queue, which avoids potential data loss or redundant processing.
#### What type of data structures should be used?
- The system uses Python dictionaries to manage JSON data fetched from the SQS messages, as seen in functions such as mask_data and flatten_json in the data_processing.py script. Dictionaries were chosen due to their inherent alignment with JSON data structures and the ease of manipulating key-value pairs.
#### How will you mask the PII data so that duplicate values can be identified?
- To address data privacy, we're employing Fernet symmetric encryption (from the cryptography library) within the data_processing.py script. Specifically, the ip and device_id fields are encrypted using the encrypt_data function. This method ensures that the original data becomes unreadable while retaining a consistent encrypted output for identical inputs. This determinism is crucial to identify duplicate records, even after masking.
#### What will be your strategy for connecting and writing to Postgres?
- To interact with the PostgreSQL database, the psycopg2 library is employed in the database.py script. Connections are established using the connect_to_db function, and data is inserted using prepared statements in the insert_into_db function. The use of DictCursor simplifies parameter binding, and the commit ensures transaction durability. In case of any exceptions during insertion, they are caught and logged for troubleshooting.
#### Where and how will your application run?
- The application, as it stands, is a set of Python scripts designed to run on a local machine or server where Python, required libraries, and PostgreSQL are installed. While it's not currently containerized, this system can be easily wrapped in a Docker container to ensure consistent deployments across different environments.
## Additional Questions
#### Deploying in Production:
- Containerization and Cloud Deployment: Though our current application isn't containerized, wrapping it in Docker can ensure reproducible deployments across various environments, be it local machines or cloud platforms like AWS ECS or Kubernetes.

- Configuration Management: Database and encryption configuration is hard coded for simplicity. However, in a production environment, these would ideally be stored in environment variables or secret management tools to ensure security and ease of configuration management.

#### Production-Readiness:
- Robustness: Error handling mechanisms, such as exceptions within the insert_into_db function in the database.py script or the get_messages_from_queue function in the sqs_client.py script, ensure resilience against unforeseen issues.
- Scaling Strategy:
Parallel Processing: The architecture can handle parallel processing. By launching multiple instances or distributing the workload across different machines or containers, the application can concurrently process data from the SQS queue, leading to enhanced throughput.
- Data Privacy and Recovery:
PII Handling: PII, such as ip and device_id, is encrypted using Fernet symmetric encryption. This approach ensures the masked data's confidentiality while preserving the capability to decrypt it if required.
#### Assumptions:
- Data Integrity: The system assumes that SQS messages are in a consistent JSON format. If a string that isn't in valid JSON format is passed, the system provides a user-friendly error message.

- Database Infrastructure: The system anticipates a consistent and uninterrupted connection to the database, along with the pre-existence of a user_logins table structured to accommodate the processed data.
## Additional Information
#### Unit Tests:
- Even though unit tests weren't explicitly mandated in the assignment, I deemed them necessary for a few reasons:
- Unit tests act as the first line of defense against potential regressions, ensuring that as we build or modify the codebase, we don't inadvertently introduce defects.
- Well-constructed tests serve as a form of documentation. They provide insight into the expected behavior of the application, demonstrating the way functions or methods are supposed to operate.
- With a robust suite of unit tests in place, refactoring or expanding the codebase becomes significantly safer. Tests provide the confidence to make changes without the fear of unknowingly disrupting existing functionality.








