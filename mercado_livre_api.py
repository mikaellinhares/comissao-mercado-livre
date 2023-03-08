import requests


class MercadoLivre:
    def __init__(self, token):
        self.token = token
        self.base_url = 'https://api.mercadolibre.com/'

    def get_product_info(self, product_id):
        url = self.base_url + f'items/{product_id}?access_token={self.token}'

        response = requests.get(url)

        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response

    def get_sales_fee_amount(self, site_id, price, category_id):
        url = self.base_url + f'sites/{site_id}/listing_prices' \
                              f'?price={price}&category_id={category_id}&access_token={self.token}'

        response = requests.get(url)

        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response
