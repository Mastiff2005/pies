# pies
Интернет-магазин кондитерских изделий (может быть использован для любых других товаров с минимальными доработками).
Данный проект позволяет создавать карточки товаров и изменять их через панель администратора, принимать и обрабатывать заказы, формировать накладные и выводить информацию по продажам.
### Основные модули (приложения):
* #### api
  API для вывода данных по товарам в корзине. Используется для динамического отображения корзины.
* #### users
  Управление регистрацией и авторизацией пользователей.
* #### homepage
  Отображение главной страницы, статических страниц с информацией и каталога товаров.
* #### cart
  Управление товарной корзиной.
* #### orders
  Управление заказами, товарными позициями в заказах.
* #### products
  Описывает модели карточек товаров.
* #### stats
  ##### Модуль выполняет следующие функции:
  * выгрузка товарных позиций и агрегация товарных наименований по названию с выводом количества каждого наименования для заданной последовательности заказов;
  * вывод статистики по продажам и основных операционных показателей за заданный период времени.
