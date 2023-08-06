from typing import Any, Dict, List, Optional, Union

from pymongo import MongoClient
from pydantic import BaseModel
from dependency_injector import containers, providers
from applauncher.applauncher import Configuration


class BaseMongoURI(BaseModel):
    uri: str
    connect: bool = True


class NamedMongoURI(BaseMongoURI):
    name: str


class MongoDBConfig(BaseMongoURI):
    uris: Optional[List[NamedMongoURI]]


def get_default_database(client: MongoClient):
    return client.get_default_database()


class MongoClientsContainer:
    def __init__(self, named_uris: List[Dict[str, Any]]):
        self._uris = {u.name: {'uri': u.uri, 'connect': u.connect} for u in named_uris}

    def __getitem__(self, conn_name: str) -> MongoClient:
        uri = self._uris[conn_name]
        return MongoClient(host=uri['uri'], connect=uri['connect'])

    def get(self, conn_name: str, default: Any = None) -> Union[MongoClient, Any]:
        if conn_name not in self._uris:
            return default
        return self.__getitem__(conn_name)


class MongoDBContainer(containers.DeclarativeContainer):
    config = providers.Dependency(instance_of=MongoDBConfig)
    configuration = Configuration()
    mongo_client = providers.Singleton(
        MongoClient,
        host=configuration.provided.mongodb.uri,
        connect=configuration.provided.mongodb.connect
    )

    db = providers.Callable(
        get_default_database,
        mongo_client
    )

    clients = providers.Callable(
        MongoClientsContainer,
        named_uris=configuration.provided.mongodb.uris
    )


class MongoDBBundle:
    def __init__(self):
        self.config_mapping = {
            "mongodb": MongoDBConfig
        }

        self.injection_bindings = {"mongodb": MongoDBContainer}
