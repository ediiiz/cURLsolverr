from pydantic import BaseModel
from typing import List, Optional

class Price(BaseModel):
    net: float
    gross: float
    taxRate: int
    currency: str

class Availability(BaseModel):
    color: str
    minLeadTimeDays: int
    maxLeadTimeDays: int

class Service(BaseModel):
    label: str
    price: Optional[float]
    icon: str
    wandaResourceId: Optional[str]
    bankFinanceId: Optional[str]
    id: str
    parentServiceId: Optional[str]
    tooltipText: str
    expId: str

class OnlineShipment(BaseModel):
    type: str
    price: Price
    hideVskText: bool

class ProductData(BaseModel):
    stock: int
    orderedStock: int
    price: Optional[Price]
    basicPrice: Optional[float]
    basicPriceQuantity: Optional[float]
    basicPriceUnit: Optional[str]
    score: int
    storeButtonAction: str
    storeAvailability: Availability
    onlineButtonAction: str
    onlineAvailability: Optional[Availability]
    onlineStock: int
    onlineOrderedStock: int
    onlineStore: str
    availableServices: Optional[List[Service]]
    itemOnDisplay: bool
    itemOnDisplayDescription: Optional[str]
    wandaData: Optional[dict]  # This can be further specified if the structure is known
    expertTags: Optional[List[str]]
    priceInclShipping: Optional[float]
    onlineShipment: List[OnlineShipment]
    showStoreName: Optional[str]
