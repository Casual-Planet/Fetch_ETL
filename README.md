<<<<<<< HEAD
<<<<<<< HEAD
# casual_planet
=======
=======
>>>>>>> 4fa0f32d51e8850a33c63dab8e2c751f27067932
## Fetch Rewards Data Engineering ETL Challenge 

Welcome! This repository contains the solution for the Fetch Rewards Data Engineering ETL Challenge. I've created a Python program to fetch data from an AWS Simple Queue Service (SQS), apply some essential transformations (including data masking), and then store the processed data into a PostgreSQL database.


### Setup:

#### Prerequisites

You need to have Docker, Docker Compose, AWS CLI, AWS CLI Local, PostgreSQL, and Python installed on your machine.

1. Install Docker: [Guide](https://docs.docker.com/engine/install/)

2. Docker Compose: It comes preinstalled with Docker on Windows and macOS. For Linux users : [ official Docker Compose installation guide.](https://docs.docker.com/compose/install/)

3. Install PostgreSQL: https://www.postgresql.org/download/

4. PyCharm or another Python IDE for editing and running Python scripts. https://www.jetbrains.com/pycharm/download/

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
   git clone <repository url>
   ```

    Navigate to the project's root directory by:
    ``` 
   cd /path/to/your/Fetch_ETL
   ```

    Replace /path/to/your/Fetch_ETL with the correct path to the Fetch_ETL directory on your system.

    
7. Once Python is installed, you need to create a virtual environment
    This will create and activate a virtual environment named venv.
    ```
   python -m venv venv
    source venv/bin/activate
   ```
    Next, you need to install the Python packages required for the project. These are specified in the requirements.txt file. Install them using the following command:
    ```
    pip install -r requirements.txt
    ```

## Starting the services

Start the Postgres and Localstack services using Docker Compose.

```
docker-compose up
```
You should see logs indicating that the services are starting. Once they are ready, you should see a line saying something like `localstack_main | Ready`. and `database system is ready to accept connections for Postgres`.


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
```
psql -d postgres -U postgres -p 5432 -h localhost -W
```
Running the Application
The main application script is located in the src directory and named main.py. This script reads data from the SQS queue, processes it, and then saves it into the PostgreSQL database.

To run the application, open a new terminal window (don't close the previous ones) in the PyCharm IDE and activate the virtual environment:
```
source venv/bin/activate
```

Then, navigate to the src directory from Fetch_ETL
```
cd src
```
Run the script with the following command:

```
python main.py
```
When you run this script, it will start processing data from the SQS queue, apply transformations, and write it to the Postgres database. You should see some output logs in your terminal indicating that the script is running.


### Verify PostgreSQL
Now we will be verifying if the data has been masked with respective fields and stored in PostgreSQL database

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

### Stopping Containers:
Executing the below command will halt and erase all the containers associated with the docker-compose.yml file.

```
docker-compose down
```


## Design Decisions and Additional Questions


### Design Decisions

#### Reading messages from the queue:
- We utilize the boto3 client to fetch messages from the AWS SQS Queue. Messages are read sequentially; once a message has been processed and transferred to the database, it's removed from the queue.

#### Data structures:
- The JSON data derived from SQS messages are managed using Python dictionaries. This approach facilitates easy access, transformation, and manipulation of the data.

#### Masking PII data:
- To mask the device_id and ip fields, a simple SHA256 hash function is employed. This method ensures uniqueness (identical input will yield identical hashed output). However, reverting to the original value is non-trivial, ensuring data protection.

#### Writing to Postgres:
- To establish a connection with the Postgres database and transfer data to it, we utilize the psycopg2 library. Each modified record is committed to the user_logins table in the database.

## Additional Questions
#### Deploying in production: 
- This application could be containerized using Docker and deployed on a cloud platform like AWS ECS or Kubernetes for scalability and easy management. Environment variables would be used to handle configuration and credentials. The application could be set up to automatically restart if it crashes.
#### Other components for production readiness:
- We would add error handling and logging to make the application more robust and easier to monitor. We would also add tests to ensure the correctness of the code.
#### Scaling with growing dataset
- The application can be scaled up by running multiple instances of it, either on multiple machines or in separate containers on the same machine. Each instance would read from the SQS queue independently, allowing the workload to be distributed.
#### Recovering PII: 
- As we are using a one-way hash function to mask the PII, it cannot be easily recovered. If we need to be able to recover the original PII data, we would need to use a different method of obfuscation that allows recovery, such as encryption with a secure key.
#### Assumptions:
- We assumed that the SQS queue always contains valid and well-formed JSON data. We also assumed that the database is always available and that the user_logins table exists with the correct schema.

## Additional Information
#### Unit Tests:
- Even though unit tests weren't explicitly mandated in the assignment, I deemed them necessary for a few reasons:

#### Quality Assurance:
- Unit tests act as the first line of defense against potential regressions, ensuring that as we build or modify the codebase, we don't inadvertently introduce defects.

#### Documentation:
- Well-constructed tests serve as a form of documentation. They provide insight into the expected behavior of the application, demonstrating the way functions or methods are supposed to operate.

#### Ease of Refactoring:
- With a robust suite of unit tests in place, refactoring or expanding the codebase becomes significantly safer. Tests provide the confidence to make changes without the fear of unknowingly disrupting existing functionality.

#### Enhanced Collaboration:
- If this project were to grow or if other developers were to collaborate, having unit tests ensures that new contributions don't negatively impact the existing code.

### Running Unit Tests
To ensure the integrity and functionality of the ETL process, we have included a suite of unit tests. Even though they weren't explicitly part of the original assessment, implementing these tests provides a safety net and helps ensure the application's robustness as we move forward with further development and improvements.

How to Run Tests:
Activate your virtual environment.

```
source venv/bin/activate
```
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








<<<<<<< HEAD
>>>>>>> 89be52a (Initial commit)
=======
>>>>>>> 4fa0f32d51e8850a33c63dab8e2c751f27067932
