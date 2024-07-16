import logging
import os
from src.shared.domain.enums.stage_enum import STAGE
from src.shared.domain.irepositories.user_repository_interface import IUserRepository
from src.shared.domain.irepositories.task_repository_interface import ITaskRepository


class Environments:
    """
    Defines the environment variables for the application. You should not instantiate this class directly.
    Please use Environments.get_envs() method instead.
    """

    stage: STAGE
    s3_bucket_name: str
    region: str
    endpoint_url: str = None
    user_pool_id: str
    client_id: str
    client_secret: str
    mongo_url: str
    base_pwd_cognito: str

    def _configure_local(self):
        os.environ["STAGE"] = os.environ.get("STAGE") or STAGE.TEST.value

    def load_envs(self):
        print(f'os.environ {os.environ} DENTRO DE LOAD ENVS!!!!!!!!!')
        if "STAGE" not in os.environ or os.environ["STAGE"] == STAGE.TEST.value:
            self._configure_local()

        self.stage = STAGE(os.environ.get("STAGE"))
        self.mongo_url = os.environ.get("MONGODB_URL")
        print(f'self.db_url {self.mongo_url}')

        if self.stage == STAGE.TEST:
            self.s3_bucket_name = "bucket-test"
            self.region = "sa-east-1"
            self.endpoint_url = "http://localhost:8000"
            self.user_pool_id = os.environ.get("USER_POOL_ID")
            self.client_id = os.environ.get("CLIENT_ID")

        else:
            self.s3_bucket_name = os.environ.get("S3_BUCKET_NAME")
            self.region = os.environ.get("REGION")
            self.endpoint_url = os.environ.get("ENDPOINT_URL")
            self.user_pool_id = os.environ.get("USER_POOL_ID")
            self.client_id = os.environ.get("CLIENT_ID")
            self.base_pwd_cognito = os.environ.get("BASE_PWD_COGNITO")

    @staticmethod
    def get_user_repo() -> IUserRepository:
        logging.info('chegou no get user repo ENVIRONMENTS')
        print('AQUI CACETEEEEEEEE')

        envs = Environments.get_envs()
        print(f'envsSSSSSSSSSSS!!!! {envs}')
        logging.info(f'envs.get_envs() {envs}')
        if envs.stage == STAGE.TEST:
            print(f'get_user_repo, envs.db_url: {envs.mongo_url}')
            from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
            return UserRepositoryMock()
        elif envs.stage in [STAGE.DEV, STAGE.HOMOLOG, STAGE.PROD]:
            from src.shared.infra.repositories.user_repository_cognito import UserRepositoryCognito
            return UserRepositoryCognito()
        else:
            raise Exception("No user repository class found for this stage")

    @staticmethod
    def get_task_repo() -> ITaskRepository:
        envs = Environments.get_envs()
        if envs.stage == STAGE.TEST:
            # from src.shared.infra.repositories.task_repository_mock import TaskRepositoryMock
            from src.shared.infra.repositories.task_repository_mongo import TaskRepositoryMongo
            print("OI MOCK")
            return TaskRepositoryMongo(envs.mongo_url)
        elif envs.stage in [STAGE.DEV, STAGE.HOMOLOG, STAGE.PROD]:
            from src.shared.infra.repositories.task_repository_mongo import TaskRepositoryMongo
            print("OI MONGOLLLL")
            return TaskRepositoryMongo(envs.mongo_url)
        else:
            raise Exception("No task repository class found for this stage")

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
        return str(self.__dict__)
