# Расширения файлов, с которыми работает система
true_ext = ['.xlsx', '.csv']

# Наименование бренда
brand = ['Hansa', 'HANSA', 'Ханса', 'ХАНСА']

# URL сайта бренда
brand_url = 'https://www.hansa.ru/'

# Словарь категории
category_dict = {
    'CBI': ['Духовой шкаф', 'Духовые шкафы', 'duchovki'],
    'HOB': ['Варочная поверхность', 'Варочные поверхности', 'varochnye_poverkhnosti'],
    'TGC': ['Варочная поверхность', 'Варочные поверхности', 'varochnye_poverkhnosti'],
    'CFS': ['Отдельностоящая плита', 'Отдельностоящие плиты', 'plity'],
    'MWS': ['Микроволновая печь', 'Микроволновые печи', 'cvch'],
    'CCI': ['Микроволновая печь', 'Микроволновые печи', 'cvch'],
    'REF': ['Холодильник', 'Холодильники', 'kholodilniki'],
    'DWS': ['Посудомоечная машина', 'Посудомоечные машины', 'posudomoechnye_mashiny'],
    'WMS': ['Стиральная машина', 'Стиральные машины', 'stiralnye_machiny'],
    'HOO': ['Вытяжка', 'Вытяжки', 'vytyazhki'],
    'RFW': ['Винный шкаф', 'Винные шкафы', 'vinnye_shkafy'],
}

# Колонки файла SAP_GOODS.xlsx для дальнейшего парсинга
product_code_col = 'HANSA_CODE'
product_index_col = 'GLC_MAT'
product_eancode_col = 'EAN_CODE'
product_description_col = 'FULL_DESCR'
product_category_col = 'ASSORTMENT'
product_status_col = 'SD_STAT'
product_brand_col = 'BRAND_TXT'

# HEADER для парсинга сайтов
HEADER = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/77.0.3865.120 Safari/537.36'}

