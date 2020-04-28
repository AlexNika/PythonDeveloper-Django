# HANSA FTPIM (FTP PIM - ftp product information system)

Система сбора, управления, распределения и дистрибуции рич-контента компаниии HANSA
Распределение рич-контента происходит с помощью внешнего FTP сервера.

Функционал бизнес-логики:
- API парсинг сайта медиа-контента digital content libraty (DCL - https://dcl.amica.pl/authorize) для наполнения базы данных сущностями рич-контента;
- Парсинг XLS/CSV файлов для наполнения базы данных характеристиками товаров и сущностями рич-контента, не присутствующими в медийной библиотеке;
- Парсинг директорий для наполнения базы данных и папок с конкретным товаром сущностями рич-контента;
- Парсинг директорий для проверки наличия сущностей рич-контента по конкретному товару;


Management commands:
- python manage.py fill_category - заполнение категориями товаров модели/таблицы Category
- python manage.py file_save param1 param2 - копирование на сервер файла param1 с описанием param2
	- param1 - путь к локальному файлу, который необходимо загрузить. Пример: с:/temp/upload_file.xlsx
	- param2 - описание загружаемого файла. Пример: Файл со списком загружаемых товаров
			   Описание должно быть бех кавычек, состоять из одного или нескольких слов через пробелы, длиной не более 256 символов.
	Команда save_file загружает файлы в директорию MEDIA_ROOT/uploads.
	
Формы:
1. Форма добавления категории http://127.0.0.1:8000/create_category/
2. Форма обратной связи - контакты http://127.0.0.1:8000/contacts/ - переписана на class Contacts(View).
3. Форма импорта/загрузки файла excel - http://127.0.0.1:8000/import_files/ - загружены базовые модели товаров.
4. Форма списка категорий - http://127.0.0.1:8000/categories/
5. Форма детального вида категории - например: http://127.0.0.1:8000/category_detail/5/
6. Форма списка товаров - http://127.0.0.1:8000/
7. Форма детального вида товара - например: http://127.0.0.1:8000/product_detail/1103064/
8. Форма добавления нового товара - http://127.0.0.1:8000/product_create/
9. Форма регистрации нового польщователя - http://127.0.0.1:8000/registration/ (* - доступ только для superuser)
10. Форма списка всех зарегистрированных пользователей - http://127.0.0.1:8000/users/ (* - доступ только для superuser)
11. Форма парсинга наличия URL адресов на родительском сайте hansa.ru - http://127.0.0.1:8000/product_filling/

Поиск:
Реализован поиск по товарам. Поиск возможен по полям Hansa_index, Hansa_code и Hansa_eancode
Поиск реализован как по точному соответствию, так и по любому вхождению.
Поиск совмещен с фильтрацией по 2-м полям типа select.

Пагинация:
Реализована пагинация на главной странице и на страице результатов поиска.

Система прав:
Незарегистрированным пользователям позволено только искать и просматривать информацию, а также 
форма обратной связи. Создание товаров, изменение, удаление, а также все действия с админ-панелью 
позволен только пользователям с правами superuser или staff. 