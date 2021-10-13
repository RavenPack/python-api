import logging
import time

from ravenpackapi import RPApi, ApiConnectionError
from ravenpackapi.utils.retry_logic import incremental_backoff

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# initialize the API (here we use the RP_API_KEY in os.environ)
api = RPApi()

# query the realtime feed
ds = api.get_dataset(dataset_id='us500')

wait_time = incremental_backoff()
while True:
    try:
        for record in ds.request_realtime():
            print(record)
            print(record.timestamp_utc, record.entity_name,
                  record['event_relevance'])
    except (KeyboardInterrupt, SystemExit):
        break
    except ApiConnectionError as e:
        logger.error("Connection error %s: reconnecting..." % e)
        time.sleep(next(wait_time))
