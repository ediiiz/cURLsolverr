from pydantic import BaseModel
from typing import List, Dict, Union, Optional

class EnumFeatureValue(BaseModel):
    value: str

class ColorFeatureValue(BaseModel):
    value: str

class FeatureClassificationValue(BaseModel):
    values: Dict[str, Union[EnumFeatureValue, ColorFeatureValue]]

class ArticleProperties(BaseModel):
    internationalArticleNumber: str
    manufacturerPartNumber: str
    itemTrackings: List[str]
    productType: str
    condition: str
    brand: str
    mainArticle: Optional[str]
    classification: FeatureClassificationValue
    visibility: str
    requiredParcelInformation: List[str]
    articleNumber: str
    featureLogos: List[str]
    showPriceInfo: bool
    newClassification: Optional[str]
    virtual: bool

class Price(BaseModel):
    net: float
    gross: float
    taxRate: int
    currency: str

class ContextValue(BaseModel):
    title: str
    name: str
    description: Optional[str]
    primaryImage: str
    gallery: List[str]
    downloadDocuments: List[str]
    primaryCategory: str
    categories: List[str]
    releaseDate: Optional[str]
    listedSince: Optional[str]
    active: bool
    shippingOptions: Dict[str, str]
    maximumOrderAmount: int
    testScores: List[str]
    shortName: str
    headline: str
    pageTitle: str
    seoTitle: str
    searchKeywords: Optional[str]
    formerPrice: Price
    formerPriceState: str
    expRichContent: bool
    additionalArticles: List[str]
    crossSaleArticles: Optional[List[str]]
    priceTagText: List[str]
    nameSubscript: str
    packageContents: str
    similarArticles: Optional[List[str]]
    extendedTeaser: List[str]

class Article(BaseModel):
    class_name: str
    articleProperties: ArticleProperties
    boosts: List[str]
    defaultContext: str
    contextSensitiveData: Dict[str, ContextValue]
    id: str
    expId: str
    revision: int
