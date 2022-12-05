from datetime import datetime, tzinfo
from typing import Union, Dict, Any, TypedDict, Optional, Tuple
from elasticsearch import Elasticsearch
from elastic_transport import ObjectApiResponse

# es = Elasticsearch( #type:ignore
#     'http://localhost:9200',
#     basic_auth=("elastic","elastic-pasaword")
# )

# doc = {
#     'author': 'author_name',
#     'text': 'Interensting 213123...',
#     'timestamp': datetime.now(),
# }

# resp = es.index(index="test-index", id="GQ_2vIQB1D5s2btDFVSP", document=doc) #updated
# resp = es.index(index="test-index", document=doc) #created
# res = es.search(index="test-index",query={"match_all":{}})
# print(res["hits"]["hits"])


DocContent = Dict[str, Union[datetime,str]]


class ConnectConfigMap(TypedDict):
    indexName: str
    timezone: str
    author: str
    username: str
    password: str
    host: str

class ElasticClient(TypedDict):
    configMap: ConnectConfigMap
    client: Elasticsearch

class DbOPResponse(TypedDict):
    _index: str
    _type: str
    _id: str
    # _version: int
    result: str
    # _shards: Dict[str, int]
    # _seq_no: int
    # _primary_term: int

def initClient(configMap: ConnectConfigMap) -> ElasticClient:
    return {
        "configMap": configMap,
        "client": Elasticsearch( 
            configMap['host'],
            basic_auth=(configMap['username'], configMap['password'])
        )
    }
 
def close(ec: ElasticClient) -> None: 
    ec['client'].close()

def insert(ec: ElasticClient, doc: DocContent) -> DbOPResponse: 
    return ec['client'].index(index=ec['configMap']['indexName'], document=doc) # type:ignore

def update(cm: ElasticClient, id:str, doc: DocContent): ...
def delete(cm: ElasticClient, id:str): ...
def search(cm: ElasticClient, id:str, query: Dict[str,Dict[Any, Any]]): ...

client = initClient({
    "indexName": "test-index",
    "timezone": "Asia/Taipei",
    "author": "test.py",
    "username": "elastic",
    "password": "elastic-pasaword",
    "host": "http://127.0.0.1:9200"
})
data: DocContent = {
    'author': 'author_name',
    'text': 'Interensting 213123...',
    'timestamp': datetime.now().astimezone()
}
r = insert(client, data)
print(r)
print(type(r))
close(client)



