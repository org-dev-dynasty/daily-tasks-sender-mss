import os
from shared.domain.enums.stage_enum import STAGE

from shared.domain.irepositories.user_repository_interface import IUserRepository
from shared.infra.repositories.user_repository_postgres import UserRepositoryPostgres


class Environments:
    """
    Defines the environment variables for the application. You should not instantiate this class directly. Please use Environments.get_envs() method instead.

    Usage:

    """
    stage: STAGE
    s3_bucket_name: str
    region: str
    endpoint_url: str = None
    dynamo_table_name: str
    dynamo_partition_key: str
    dynamo_sort_key: str
    cloud_frontget_user_presenter_distribution_domain: str
    mss_name: str 

    def _configure_local(self):
        os.environ["STAGE"] = os.environ.get("STAGE") or STAGE.TEST.value

    def load_envs(self):
        if "STAGE" not in os.environ or os.environ["STAGE"] == STAGE.TEST.value:
            self._configure_local()

        self.stage = STAGE[os.environ.get("STAGE")]
        self.mss_name = os.environ.get("MSS_NAME")
        
        if self.stage == STAGE.TEST:
            self.s3_bucket_name = "bucket-test"
            self.region = "sa-east-1"
            self.endpoint_url = "http://localhost:8000"
            self.dynamo_table_name = "user_mss_template-table"
            self.dynamo_partition_key = "PK"
            self.dynamo_sort_key = "SK"
            self.cloud_front_distribution_domain = "https://d3q9q9q9q9q9q9.cloudfront.net"

        else:
            self.s3_bucket_name = os.environ.get("S3_BUCKET_NAME")
            self.region = os.environ.get("REGION")
            self.endpoint_url = os.environ.get("ENDPOINT_URL")
            self.dynamo_table_name = os.environ.get("DYNAMO_TABLE_NAME")
            self.dynamo_partition_key = os.environ.get("DYNAMO_PARTITION_KEY")
            self.dynamo_sort_key = os.environ.get("DYNAMO_SORT_KEY")
            self.cloud_front_distribution_domain = os.environ.get("CLOUD_FRONT_DISTRIBUTION_DOMAIN")

    @staticmethod
    def get_user_repository() -> IUserRepository:
        if Environments.get_envs().stage == STAGE.TEST:
            return UserRepositoryPostgres()
        elif Environments.get_envs().stage in [STAGE.DEV, STAGE.HOMOLOG, STAGE.PROD]:
            from shared.infra.repositories.user_repository_cognito import UserRepositoryCognito
            return UserRepositoryCognito()
        else:
            raise Exception("No user repository class found for this stage")

    @staticmethod
    def get_envs() -> "Environments":
        """
        Returns the Environments object. This method should be used to get the Environments object instead of instantiating it directly.
        :return: Environments (stage={self.stage}, s3_bucket_name={self.s3_bucket_name}, region={self.region}, endpoint_url={self.endpoint_url})

        """
        envs = Environments()
        envs.load_envs()
        return envs

    def __repr__(self):
        return self.__dict__

