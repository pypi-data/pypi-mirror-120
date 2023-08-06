
from herre.wards.query import TypedQuery
from herre.access.object import GraphQLObject
from herre.config.model import BaseConfig
from herre.auth import HerreClient, get_current_herre
from herre.wards.graphql import ParsedQuery, GraphQLWard


class FlussConfig(BaseConfig):
    _group = "fluss"
    host: str
    port: int
    secure: bool



class FlussWard(GraphQLWard):

    class Meta:
        key = "fluss"

    def __init__(self, herre: HerreClient) -> None:
        self.config = FlussConfig.from_file(herre.config_path)
        self.transcript = None
        super().__init__(herre, f"http://{self.config.host}:{self.config.port}/graphql")



class playground():

    def __init__(self, width=900, height=700) -> None:
        herre = get_current_herre()
        self.config = FlussConfig.from_file(herre.config_path)
        self.width = width
        self.height = height

    def _repr_html_(self):
        return f"<iframe src='http://{self.config.host}:{self.config.port}/graphql' width={self.width} height={self.height}></iframe>"



class gql(TypedQuery):
    ward_key = "fluss"
    


