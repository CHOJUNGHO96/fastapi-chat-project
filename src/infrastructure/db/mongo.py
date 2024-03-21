from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine


class MongoDB:
    def __init__(self, config) -> None:
        self.mongo_url = config["MONGO_URL"]
        self.mongo_db_name = config["MONGO_DB_NAME"]
        self.mongo_max_connections = config["MONGO_MAX_CONNECTIONS"]
        self.mongo_min_connections = config["MONGO_MIN_CONNECTIONS"]
        self.__client: AsyncIOMotorClient = None
        self.__engine: AIOEngine | None = None

    @property
    def client(self) -> AsyncIOMotorClient:
        return self.__client

    @property
    def engine(self) -> AIOEngine:
        return self.__engine

    async def connect(self):
        """
        Connect to MongoDB
        """
        self.__client = AsyncIOMotorClient(
            self.mongo_url,
            maxPoolSize=self.mongo_max_connections,
            minPoolSize=self.mongo_min_connections,
            )
        self.__engine: AIOEngine = AIOEngine(
            client=self.__client, database=self.mongo_db_name
            )

    async def close(self):
        """
        Close MongoDB Connection
        """
        self.__client.close()

