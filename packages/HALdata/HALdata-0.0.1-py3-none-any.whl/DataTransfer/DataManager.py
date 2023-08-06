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

from decouple import config
import pandas as pd
import numpy as np
from botocore.exceptions import NoCredentialsError
from data_transfer import dataTransfer
import json

class DataManager():
    def __init__(self):
        self.domo_email_dict = {
            'Summary Table' : 'fe0077517d984a1da02e3fb614149cb0@sharkninja.mail.domo.com',
            'Unit Table' : '23c7265d50964aae818e7b444011bcc2@sharkninja.mail.domo.com',
            'Individual Unit' : '417a5a871efd4206afd06d29fa24ee29@sharkninja.mail.domo.com'
        }

        self.sql_query_dict = {
            'Summary Table' : 'SELECT A.TEST_ID, A.SKU_BUILD, A.SOFTWARE_VERSION, A.TOTAL_KCUP, A.TOTAL_COFFEE, A.TOTAL_HOT_WATER, A.LOAD_DATETIME, A.MAX_BOILER_TEMP_TEST, B.HUMAN_READABLE_DESC FROM NINJA_TESTING_BDP_DB_PROD.REPORTING.SUMMARY_TABLE AS A INNER JOIN NINJA_TESTING_BDP_DB_PROD.STAGE.TEST_ID_HASH AS B ON B.TEST_ID_HASH = A.TEST_ID ORDER BY TEST_ID;',
            'Unit Table' : 'SELECT A.LOAD_DATETIME, A.CYCLE_ID, A.TEST_ID, A.SKU_BUILD, A.SOFTWARE_VERSION, A.CURRENT_BREW, A.BREW_OUNCES, A.BREW_BASKET, A.MAX_BOILER_TEMP, A.MAX_WARM_PLATE_TEMP, A.ELAPSED_TIME, B.HUMAN_READABLE_DESC FROM NINJA_TESTING_BDP_DB_PROD.REPORTING.UNIT_TABLE AS A INNER JOIN NINJA_TESTING_BDP_DB_PROD.STAGE.TEST_ID_HASH AS B ON B.TEST_ID_HASH = A.TEST_ID ORDER BY TEST_ID, CYCLE_ID;',
            'Individual Unit' : 'SELECT * FROM NINJA_TESTING_BDP_DB_PROD.REPORTING.UNIT_TABLE WHERE TEST_ID = 91111002 ORDER BY CYCLE_ID;'
        }

        self.worker = dataTransfer()

    def get_data(self):
        """
        Get data from snowflake in for loop
        returns: dictionaru payload for call to api
        """
        
        lst = ["Summary Table", "Unit Table", "Individual Unit"]

        for i in lst:
            query = self.sql_query_dict[i]

            print(query)

            #Get data from snowflake 
            df = self.worker.sfQuery(query)

            file_name = f"{i}_DOMO.csv"

            path = "C:/Users/ccrescas/Downloads/"

            # Dump Pandas DataFrame to Excel sheet
            df.to_csv('%s%s' % (path, file_name), index=False)

            print(f'Created {file_name}')

            local_file = '%s%s' % (path, file_name)

            #calls upload to s3 function for snowflake sample data
            self.worker.upload_to_s3(file_name=file_name, local_file=local_file)

            dict = {"aws_bucket_name" : "sn-snowflake-ninja",
                "aws_access_key" : "AKIAUNSR4422MZHDIOEL",
                "aws_secret_key" : "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",
                "aws_filepath" : file_name,
                "aws_region" : "us-east-1",
                "aws_email_address" : self.domo_email_dict[i],
                "aws_send_file_name" : f"{i}.csv",
                "aws_delete_file" : "True"}

            DataManager.send_payload(self, dict)


    def send_payload(self, dict):
        """
        Send multiple payloads to API with correct address
        """
        
        payload = json.dumps(dict)

        #passes json payload to api for emailing to Domo
        self.worker.call_api(payload)