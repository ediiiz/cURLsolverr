from curl_cffi import requests
from typing import Union, Dict, Any
from pydantic import BaseModel, ValidationError
from .models.article_models import Article
from .models.store_models import ExpertStores
from .models.price_models import ProductData

class ExpertAPIWrapper:
    _GET_ARTICLE_BY_EXP_NR_URL = "https://www.expert.de/shop/api/neo/article-service/getArticleByExpNr"
    _GET_ARTICLE_DATA_URL = 'https://www.expert.de/shop/api/neo/internal-pub-service/getArticleData'
    _STORE_FINDER_URL = "https://www.expert.de/shop/api/storeFinder?maxResults=1000"
    _HEADERS = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    def __init__(self):
        self.products = []

    from pydantic import ValidationError

    def fetch_product_information(self, store_id: str, store_name: str, article_id: str) -> Union[ProductData, str]:
        payload = {
            "articleId": article_id,
            "store": store_id,
            "cacheLevel": "MOST_RECENT"
        }

        try:
            response = requests.post(self._GET_ARTICLE_DATA_URL, headers=self._HEADERS, json=payload, impersonate="chrome100")
            response.raise_for_status()

            # Validate and parse raw data using Pydantic
            product_data = ProductData.model_validate_json(response.text)
            
            if product_data.price and product_data.onlineButtonAction == 'ORDER':
                product_data.showStoreName = store_name
                product_data.onlineStore = store_id
                if product_data.price.gross and product_data.onlineShipment[0].price.gross:
                    product_data.priceInclShipping = product_data.price.gross + product_data.onlineShipment[0].price.gross

                self.products.append(product_data)
                self.products.sort(key=lambda x: x.priceInclShipping if x.priceInclShipping else 0)

            return product_data

        except ValidationError as ve:
            return f"Validation error for product data from storeId {store_id}: {ve}"
        except requests.RequestException as e:
            return f"Error fetching product information for storeId {store_id}: {e}"


    def get_article_by_number(self, article_nr: int) -> Article:
        payload = {
          "articleNr": str(article_nr)
        }
        try:
            response = requests.post(self._GET_ARTICLE_BY_EXP_NR_URL, headers=self._HEADERS, json=payload, impersonate="chrome100")
            response.raise_for_status()
            
            # Use Pydantic model to parse and validate the response data
            article = Article.model_validate_json(response.text)
            return article

        except ValidationError as ve:
            raise ValueError(f"Error validating article data: {ve}")
        except requests.RequestException as e:
            raise ValueError(f"Error fetching article: {e}")


    def expert_stores(self) -> ExpertStores:
        """Fetches information about expert stores.

        Returns:
        - dict: The expert stores' information.
        """
        try:
            response = requests.get(self._STORE_FINDER_URL, headers=self._HEADERS, impersonate="chrome100")
            response.raise_for_status()
            stores = ExpertStores.model_validate_json(response.text)
            return stores
        except ValidationError as ve:
                raise ValueError(f"Error validating expert stores data: {ve}")
        except requests.RequestException as e:
            raise ValueError(f"Error fetching expert stores: {e}")
