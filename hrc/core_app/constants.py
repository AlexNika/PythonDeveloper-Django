# Расширения файлов, с которыми работает система
true_ext = ['.xlsx', '.csv']

# Наименование бренда
brand = ['Hansa', 'HANSA', 'Ханса', 'ХАНСА']

# URL сайта бренда
brand_url = 'https://www.hansa.ru/'

# External server name ( FTP URL HCL бренда)
ext_server_name = 'ftp://ftp.selcdn.ru'

# Internal server name
int_server_name = 'ru15d001.amica.com.pl'

# Local file dir
local_file_dir = 'Site-HANSA.RU\\RICH_CONTENT'

# Словарь категории
category_dict = {
    'CBI': ['Духовой шкаф', 'Духовые шкафы', 'duchovki'],
    'HOB': ['Варочная поверхность', 'Варочные поверхности', 'varochnye_poverkhnosti'],
    'TGC': ['Варочная поверхность', 'Варочные поверхности', 'varochnye_poverkhnosti'],
    'CFS': ['Отдельностоящая плита', 'Плиты', 'plity'],
    'MWS': ['Микроволновая печь', 'Микроволновые печи', 'cvch'],
    'CCI': ['Микроволновая печь', 'Микроволновые печи', 'cvch'],
    'REF': ['Холодильник', 'Холодильники', 'kholodilniki'],
    'DWS': ['Посудомоечная машина', 'Посудомоечные машины', 'posudomoechnye_mashiny'],
    'WMS': ['Стиральная машина', 'Стиральные машины', 'stiralnye_machiny'],
    'HOO': ['Вытяжка', 'Вытяжки', 'vytyazhki'],
    'RFW': ['Винный шкаф', 'Винные шкафы', 'vinnye_shkafy'],
}

# Имена Excel файлов для загрузки
BASE_GOODS_FILE_NAME = 'SAP_GOODS'
BASE_PRICE_FILE_NAME = 'ZMASTERPL'
BASE_MRKTD_FILE_NAME = 'MARKETING_DESCRIPTIONS'

# Колонки файлов xlsx для дальнейшего парсинга
product_code_col = 'HANSA_CODE'
product_index_col = 'GLC_MAT'
product_eancode_col = 'EAN_CODE'
product_description_col = 'FULL_DESCR'
marketing_description_col = 'MARKET_DESCR'
product_category_col = 'ASSORTMENT'
product_status_col = 'SD_STAT'
product_brand_col = 'BRAND_TXT'

# HEADER для парсинга сайтов
HEADER = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/77.0.3865.120 Safari/537.36'}

TEST_IMAGE_PATH = '/temp/test_image.jpg'
