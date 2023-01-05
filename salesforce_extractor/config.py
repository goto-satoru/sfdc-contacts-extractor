from dataclasses import dataclass
from cognite.extractorutils.configtools import BaseConfig, RawDestinationConfig


@dataclass
class ExtractorConfig:
    """
    Configuration for the running extractor, so any performance tuning parameters should go here
    """
    upload_queue_size: int = 50000
    parallelism: int = 10


@dataclass
class SfdcConfig:
    username: str
    password: str
    security_token: str
    query_string: str


@dataclass
class SalesforceConfig(BaseConfig):
    """
    Master configuration class, containing everything from the BaseConfig class, in addition to the custom building
    blocks defined above
    """
    sfdc: SfdcConfig
    destination: RawDestinationConfig
    extractor: ExtractorConfig = ExtractorConfig()
