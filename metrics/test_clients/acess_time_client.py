import requests
import sys
import time
sys.path.insert(1, "../")
import metric_log as logger

start_id = 3000
url_stratAStore = f"http://62.107.0.222:9000/exercise2/files"


number_of_test_runs = 100

log = ""
with open("../../config.txt") as f:
    masterip = f.readline().split('=')[1].strip()
    pi1 =  f.readline().split('=')[1].strip()
    pi2 =  f.readline().split('=')[1].strip()
    pi3 =  f.readline().split('=')[1].strip()
    log =  f.readline().split('=')[1].strip()
    
metric_log = logger.MetricLog(f"../../metrics/logs/{log}.csv")

for i in range(number_of_test_runs):
    start_time = time.time()
    response = requests.get(f"{url_stratAStore}/{start_id}")
    end_time = time.time()
    retrieve_time = end_time - start_time
    metric_log.log_entry(str(retrieve_time))


