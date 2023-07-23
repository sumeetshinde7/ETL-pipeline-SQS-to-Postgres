import sys
import argparse
import boto3
import json
import configparser
import base64
import psycopg2
from datetime import datetime

class ETL_process():
    '''
    This class performs the entire ETL process through use of member functions    
    '''

    def __init__(self, endpoint_url, queue_name, wait_time, max_messages):
        '''Get postgres credentials using the constructor '''


        # argument values for ETL class
        self.__endpoint_url = endpoint_url
        self.__queue_name = queue_name
        self.__wait_time = wait_time
        self.__max_messages = max_messages


        # postgres credentials parser
        config = configparser.ConfigParser()
        config.read('postgres_creds.ini')

        self.__username = config.get('credentials', 'username')
        self.__password = config.get('credentials', 'password')
        self.__host = config.get('credentials', 'host')
        self.__database = config.get('credentials', 'database')
        self.__port = config.get('credentials', 'port')





    def poll_messages(self):
        '''reads messages from SQS queue
           returns a stack of messages
        '''

        sqs_client = boto3.client('sqs', 
                                  endpoint_url=self.__endpoint_url,
                                  region_name='us-east-1',
                                  aws_access_key_id='aaa', 
                                  aws_secret_access_key='aaa', 
                                  aws_session_token='aaa', 
                                  config=None)

        # check for response from SQS queue
        try:
            response = sqs_client.receive_message(QueueUrl= self.__endpoint_url + '/' + self.__queue_name,
                                                MaxNumberOfMessages=self.__max_messages,
                                                WaitTimeSeconds=self.__wait_time
                                            )
        except Exception as exceptions:
            # Print error while parsing parameters
            print("Error - " + str(exceptions))
            sys.exit()

         # fetch messages from SQS queue
        messages = response['Messages']
        
        return messages




    def mask(self, input_value, action = "encode"):
        """Function to encode or decode string using base64
            returns encoded or decoded values based on encode/decode action 
        """

        # Check if action is encoding or decoding
        if action == "encode":
            ascii_string = input_value.encode('ascii')
            encoded_string = base64.b64encode(ascii_string).decode('utf-8')

            return encoded_string

        elif action == "decode":
            decoded_string = base64.b64decode(input_value).decode('utf-8')

            return decoded_string



    def transform_messages(self, messages):
        '''Mask PII i.e. device_id and ip using base64 algorithm
           returns transformed messages with masked PIIs
        '''

        # Ensure message exists
        try:
            if len(messages) == 0:
                raise IndexError("Message list is empty")
        except IndexError as index_error:
            print("Error - " + str(index_error))
            sys.exit()

        transformed_messages = []

        # Traverse each message
        for mesg in messages:

            message_body = json.loads(mesg['Body'])

            # Check if PII fields exist in message
            try:
                ip = message_body['ip']
                device_id = message_body['device_id']

            except Exception as exception:
                print("Exception : " + str(exception) + " not found. Skipping this message from SQS")
                continue


            # Mask PII fields
            masked_ip = self.mask(ip)
            masked_device_id = self.mask(device_id)

            # Replace original values
            message_body['ip'] = masked_ip
            message_body['device_id'] = masked_device_id


            transformed_messages.append(message_body)


        return transformed_messages
    


    def load_messages(self,messages):
        '''
        Loads data to a Postgres Database
        '''

        # Ensure message exists
        try:
            if len(messages) == 0:
                raise IndexError("Message list is empty")
        except IndexError as index_error:
            print("Error - " + str(index_error))
            sys.exit()

   
        # Connect to Postgres
        pg_conn = psycopg2.connect(
                        host = self.__host,
                        database = self.__database,
                        user = self.__username,
                        password = self.__password,
                        port = self.__port
                        )


        # Create a database cursor
        cursor = pg_conn.cursor()

        # Traverse each message
        for mesg in messages:
            
            # create new fields for current datetime
            mesg['create_date'] = datetime.now().strftime("%Y-%m-%d")
            # locale returns nulls so replace with 'None'
            mesg['locale'] = 'None' if mesg['locale'] == None else mesg['locale']
            
            # Convert dictionary values to list
            values = list(mesg.values())

            # Update DDL for user_logins table to accomodate for storing app_version 
            # in non-integer format to avoid loss of information
            cursor.execute('''ALTER TABLE user_logins
                            ALTER COLUMN app_version TYPE varchar(32);
                           ''')



            # Execute the insert query
            cursor.execute('''INSERT INTO user_logins
                           (user_id, 
                           app_version, 
                           device_type, 
                           masked_ip, 
                           locale, 
                           masked_device_id, 
                           create_date)
                           VALUES (%s, %s, %s, %s, %s, %s, %s)''', values)

            # Commit data to Database
            pg_conn.commit()

        pg_conn.close()

        return
