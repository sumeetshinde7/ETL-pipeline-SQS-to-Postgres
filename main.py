import sys
import argparse

from ETL import ETL_process


def main():
    """The Main Function"""

    # setup argparser to parse args using CLI
    parser = argparse.ArgumentParser(
                    prog = "SQS ETL pipeline",
                    description = '''This python script extracts data from an SQS queue, 
                                    transforms PIIs in the data and loads the processed data into a Postgres database
                                    '''
                    )

    # Add arguments for argparser
    parser.add_argument('-e', '--endpoint-url', required = True ,help = "endpoint URL for SQS data source")
    parser.add_argument('-q', '--queue-name', required = True ,help = "exact queue name of the SQS queue")
    parser.add_argument('-t', '--wait-time', type = int, default = 10, help = "wait time")
    parser.add_argument('-m', '--max-messages', type = int, default = 10, help = "maximum numebr messages to be pulled")

    # parse the argumenets
    args = vars(parser.parse_args())

    # read value for each parsed argument
    endpoint_url = args['endpoint_url']
    wait_time = args['wait_time']
    max_messages = args['max_messages']
    queue_name = args['queue_name']
 
    # instantiate ETL class object
    etl_process_object = ETL_process(endpoint_url, 
                                     queue_name, 
                                     wait_time,
                                     max_messages)

    # Extract messages from SQS Queue
    print("Fetching messages from SQS Queue...")
    messages = etl_process_object.poll_messages()

    # Transform the messages
    print("Transforming messages...")
    transformed_messages = etl_process_object.transform_messages(messages)

    # Load transformed data to Postgres database
    print("Loading messages to Postgres DB...")
    etl_process_object.load_messages(transformed_messages)

    print("ETL process completed")

    return


if __name__ == "__main__":
    main()