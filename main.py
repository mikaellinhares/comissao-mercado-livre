from mercado_livre_api import MercadoLivre
import gspread
from time import sleep

ml_token = 'APP_USR-3697589497563412-030812-b3ebb8be45b4492e20913fc7cac57706-682469039'
mercado_livre = MercadoLivre(token=ml_token)


gc = gspread.oauth(
    credentials_filename='google-auth/credentials.json',
    authorized_user_filename='google-auth/authorized_user.json'
)
sh = gc.open("CUSTOS 2")

worksheet = sh.worksheet("ANÚNCIOS")

all_values = worksheet.get_all_values()

for i, row in enumerate(all_values):
    if i == 0:
        continue

    index = i + 1

    id_produto = row[0]
    product_info = mercado_livre.get_product_info(product_id=id_produto)

    if product_info[0]:
        produto_titulo = product_info[1]['title']
        produto_site_id = product_info[1]['site_id']
        produto_preco = row[1].replace(',', '.')
        produto_categoria_id = product_info[1]['category_id']

        sales_fee = mercado_livre.get_sales_fee_amount(
            site_id=produto_site_id, price=produto_preco, category_id=produto_categoria_id
        )

        if sales_fee[0]:
            produto_anuncio_tipo = row[2]
            comissao_anuncio = 'NÃO ENCONTRADO'
            for item in sales_fee[1]:
                if produto_anuncio_tipo == item['listing_type_name']:
                    comissao_anuncio = item['sale_fee_amount']
                    break

            print(f'Achado {id_produto} linha {index}')

            cell_list = worksheet.range(f'D{index}:F{index}')
            cell_values = [produto_categoria_id, comissao_anuncio, produto_titulo]

            for i_cell, val in enumerate(cell_values):
                cell_list[i_cell].value = val

            worksheet.update_cells(cell_list)
    else:
        print('Renovação do Token Mercado Livre necessária')
        break

    if i % 50 == 0:
        print('Sleep 10 segundos')
        sleep(10)
