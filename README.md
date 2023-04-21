# pw_shop - Приложение взаимодействия с сайтом ПВ-магазина  

# Модули:  

- ## `db_utils` - модуль взаимодействия с БД
    - ## Классы:
      - ### `DbConnection` - Осуществляет подключение к БД
      - ### `DbSettingsData` - Дата-класс настроек БД
      - ### `QueryCondition` - Дата-класс условия отбора записи в БД
      - ### `SqlConstructor` - Конструктор SQL-запросов
      - ### `BaseDb` - Базовый класс взаимодействия с данными в БД (создание/удаление/обновление/выбор с условием записи)  

- ## `server_utils` - модуль поддержки взаимодействия с сервером
    - ## Классы:
      - ### `HttpException` - Класс взаимодействия с http исключениями  
      - ### `UrlConstructor` - Конструктор URL
      - ### `UrlData` - Данные URL
- ## `db_shop` - модуль работы с ПВ-магазином
- ## Подмодуль `user`:  
    - ## Классы:
      - ### `UserData` - Дата-класс данных пользователя
      - ### `UserDb` - Класс работы с таблицей пользователя (user_data)
      - ### `Token` - Класс работы с токеном
