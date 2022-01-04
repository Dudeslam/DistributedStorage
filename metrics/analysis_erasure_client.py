import csv
import json
import time

import requests

base_url = 'http://62.107.0.222:9000'
iterations = 5
files = ['100MB'] # ['10KB', '100KB', '1MB', '10MB', '100MB']
result_file = "results_erasure_client.csv"
fields = ['id',
          'file_size',
          'write_time',
          'write_status_code',
          'read_time',
          'read_status_code',
          'storage_mode',
          'max_erasures']

# Open csv file
with open(f'./logs/{result_file}', 'w') as csvfile:
    csv_writer = csv.writer(csvfile)

    # Write first row of csv
    csv_writer.writerow(fields)
    i = 0
    for storage_mode in ['erasure_coding_rs_random_worker', 'erasure_coding_rs']:
        for max_erasure in [2, 1]:
            # For each file size (10kB, 100kB, 1MB, 10MB and 100MB)
            for file in files:
                with open(f'./testfiles/{file}.txt', 'r') as f:
                    # Perform iterations
                    for i in range(iterations):
                        multipart_form_data = {
                            'file': f,
                            'storage': (None, storage_mode),
                            'max_erasures': (None, max_erasure),
                        }

                        # Upload file
                        start_time = time.time()
                        write_response = requests.post(f'{base_url}/exercise3/files_mp', files=multipart_form_data)
                        end_time = time.time()
                        write_total_time = end_time - start_time
                        id = json.loads(write_response.text)['id']

                        # Download file
                        time.sleep(30)
                        start_time = time.time()
                        read_response = requests.get(f'{base_url}/exercise3/files/{id}')
                        end_time = time.time()
                        read_total_time = end_time - start_time
                        print(i)
                        # Save entry in CSV
                        csv_writer.writerow([id,
                                             file,
                                             write_total_time,
                                             write_response.status_code,
                                             read_total_time,
                                             read_response.status_code,
                                             storage_mode,
                                             max_erasure
                                             ])
                        f.seek(0)

