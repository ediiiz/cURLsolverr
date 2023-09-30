from typing import List, Optional, Tuple, Union
from pydantic import BaseModel, RootModel

class OpeningTimes(BaseModel):
    mo_fr: Optional[dict[str, Union[Tuple[str, str], str]]]
    sa: Optional[dict[str, str]]

class Store(BaseModel):
    can_use_shop: bool
    decentralized_shop: bool
    website: bool
    latitude: float
    longitude: float
    street: str
    zip: str
    city: str
    phone: str
    name: str
    id: str
    store_id: str

class ExpertStore(BaseModel):
    start_lat: float
    start_lng: float
    linear_distance: str
    opening_times: Optional[OpeningTimes]
    store: Store

class ExpertStores(RootModel):
    List[ExpertStore]
