#!/usr/bin/env python

'''
MIT License
Copyright (c) 2021 Mikhail Hyde & Cole Crescas
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import snowflake.connector
import pandas as pd
import json
import requests
import boto3
from botocore.exceptions import NoCredentialsError


class dataTransfer():
    def __init__(self):
        """Saves AWS credentials for boto3 client
        """
        filename = "aws_credentials.json"

        with open(filename, 'r') as f:
            aws_credentials = json.load(f)

        self.ACCESS_KEY = aws_credentials['ACCESS_KEY']
        self.SECRET_KEY = aws_credentials['SECRET_KEY']
        self.bucket = aws_credentials['bucket']

        self.s3 = boto3.client('s3', aws_access_key_id=self.ACCESS_KEY,
                            aws_secret_access_key=self.SECRET_KEY)




    def sfQuery(self, query=None):
        '''Basic Query Function: Provided a query and username, it will create an output dataframe of the queried data.
        '''

        print('Connecting to Snowflake\n')


        sql = query


        # Connection string
        con = snowflake.connector.connect(
                    user='CCRESCAS@SHARKNINJA.COM',
                    authenticator='externalbrowser',
                    account='sharkninja.us-east-1',
                    warehouse='NINJA_BDP_SMALL',
                    database='NINJA_TESTING_BDP_DB_PROD',
                    #schema='REPORTING'
        )
                    
    

        print('Performing Query\n')

    

        cur = con.cursor()
        
        cur=cur.execute(sql)

    

        print('Writing to Dataframe\n')
        
        df = cur.fetch_pandas_all()
        
        print('Closing Cursor and Connection\n')
        cur.close()
        con.close()
        
        print(df.info())
        return df.copy(deep=True)


    def upload_to_s3(self, file_name, local_file):
        '''
        Uploads a single file to the AWS s3 bucket.
        '''

        try:
            self.s3.upload_file(Filename=local_file, Bucket=self.bucket, Key=file_name) # (local_file, bucket, s3_file)
            print("Upload Successful")
            return True
        except FileNotFoundError:
            print("The file was not found")
            return False
        except NoCredentialsError:
            print("Credentials not available")
            return False

    def call_api(self, payload):
        """
        Function to send csv file into Domo from API
        """
        try:
            headers = {'content-type':'application/json'}
            response = requests.post('https://snapp.euro-pro.local:8080/aws_access//sendAWSFileAsEmail', data=payload, timeout=5, headers=headers, verify=False)
            response.raise_for_status()
            print("Connected to API successfully")

           
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

    