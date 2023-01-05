import json
import logging
from concurrent.futures.thread import ThreadPoolExecutor
from threading import Event

from cognite.client import CogniteClient
from cognite.client.data_classes import Row
from cognite.extractorutils import Extractor
from cognite.extractorutils.statestore import AbstractStateStore
from cognite.extractorutils.uploader import RawUploadQueue

from simple_salesforce import Salesforce

from .config import SalesforceConfig

logger = logging.getLogger(__name__)


def get_contacts(config: SalesforceConfig, queue: RawUploadQueue) -> None:

    """
    SELECT SFDC Contacts

    Args:
        config: Extractor config
        queue:  Upload queue for batching RAW requests
    """
    logger.info(f"SELECT Contacts from SFDC to {config.destination.database}/{config.destination.table}")
    logger.info(f"Query string: {config.sfdc.query_string}")

    try:
        sf = Salesforce(username=config.sfdc.username, 
                        password=config.sfdc.password, 
                        security_token=config.sfdc.security_token)
        query_string = config.sfdc.query_string
        logger.info(query_string)
        contacts = sf.query_all_iter(query_string)
        count = 0
        for row in contacts:
            count = count + 1
            logger.debug(f"row #{count} : {json.dumps(row, indent=2)}")

            queue.add_to_upload_queue(
                database=config.destination.database,
                table=config.destination.table,
                raw_row=Row(key=row['Id'], columns=row),
            )

    except Exception as e:
        logger.info(f"Extraction failed : {e}")
        print(f"Extraction failed : {e}")


def run(cognite: CogniteClient, states: AbstractStateStore, config: SalesforceConfig, stop_event: Event) -> None:
    """
    Extract Contacts from Salesforce

    Args:
        cognite: Initialized cognite client object
        states: Initialized state store object
        config: Configuration parameters
        stop_event: Cancellation token, will be set when an interrupt signal is sent to the extractor process
    """
    with RawUploadQueue(
        cdf_client=cognite, max_upload_interval=30, max_queue_size=100_000
    ) as queue, ThreadPoolExecutor(
        max_workers=config.extractor.parallelism, thread_name_prefix="SalesforceExtractor"
    ) as executor:
        executor.submit(get_contacts, config, queue)


def main(config_file_path: str = "config.yaml") -> None:
    """
    Main entrypoint.

    Args:
        config_file_path: path to config file. Defaults to config.yaml
    """
    with Extractor(
        name="salesforce_extractor",
        description="An extractor that SELECT Contact from SFDC to CDF RAW",
        config_class=SalesforceConfig,
        run_handle=run,
        config_file_path=config_file_path,
        use_default_state_store=False
    ) as extractor:
        extractor.run()


if __name__ == "__main__":
    main()
