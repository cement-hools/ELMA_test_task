# ELMA Тестовое Задание

<!---
https://github.com/cement-hools/ELMA_test_task/badge.svg
--->
![example workflow](https://github.com/cement-hools/ELMA_test_task/actions/workflows/project_test.yml/badge.svg)
### Используется GitHub Actions для автоматического тестирования при изменении кода в репозитории

## Технологии
    Python 3.8, FastApi, PyTest, httpx, pydantic

## Задача

Написать http сервис на языке python с одним endpoint /counts, принимающий POST запрос вида 

```json
{"urls": [
  {"url": "https://python.org", "query": "python"},    
  {"url": "https://www.djangoproject.com", "query": "django"},
  {"url": "https://python.org", "query": "python"} 
  ],  
  "max_timeout": 3000
} 
``` 
- Максимальное время ответа не должно превышать указанный maxTimeout.  
- На каждый url нужно отправить HTTP-запрос методом GET и посчитать кол-во вхождений строки query в теле ответа.
- Если запрос http запрос завершился с ошибкой, вернул http статус !=200 или был превышен maxTimeout, 
то для данного url вернуть status=error и не возвращать count.  

Пример ответа 

HTTP 200 
```json
{"urls": [
  {"url": "https://python.org", "count": 10, "status": "ok"},
  {"url": "https://www.djangoproject.com", "status": "error"},
  {"url": "https://sanic.dev/en/", "count": 20, "status": "ok"}
]
}  
```

## endpoint
- [**POST**]```/counts``` отправить запрос на сервер.  

#### Параметры запроса
- urls*: list - список url ресурсов и строка для поиска
    - url*: str - адрес ресурса
    - query*: str - строка для поиска
- max_timeout: int (default=3000) - Максимальный таймаут на запрос ресурса в миллисекундах.
#### Тело запроса
```json
{
  "urls": [
      {
        "url": "https://python.org", 
        "query": "python"
      },    
      {
        "url": "https://www.djangoproject.com", 
        "query": "django"
      },
      {
        "url": "https://pythonist.ru",
        "query": ","
      },
      {
        "url": "https://ww@.-5644.com", 
        "query": "Test"
      } 
  ],  
  "max_timeout": 2000
} 
``` 
#### Пример ответа
```json
{
    "urls": [
        {
            "url": "https://python.org",
            "status": "error"
        },
        {
            "url": "https://www.djangoproject.com",
            "status": "ok",
            "count": 85
        },
        {
            "url": "https://pythonist.ru",
            "status": "ok",
            "count": 348
        },
        {
            "url": "https://ww@.-5644.com",
            "status": "error"
        }
    ]
}
```

## Установка и запуск

1. Клонировать репозиторий
    ```
    git clone https://github.com/cement-hools/ELMA_test_task
    ```
2. Перейдите в директорию ELMA_test_task
    ```
   cd ELMA_test_task
    ```
3. Создать виртуальное окружение, активировать и установить зависимости
    ``` 
   python -m venv venv
    ```
   Варианты активации окружения:
   - windows ``` venv/Scripts/activate ```
   - linux ``` venv/bin/activate ```
     <br><br>
   ```
   python -m pip install -U pip
   ```
   ```
   pip install -r requirements.txt
   ```

4. Запустить приложение на сервере
   ```
   python main.py
   ```
5. Проект доступен 
   ```
   http://127.0.0.1:8000
   http://localhost:8000
   ```

## Swaggerr
```
/docs
```

## Тесты
Запустить тесты
```
pytest
```

## Запуск в Docker контейнере

1. Клонировать репозиторий
    ```
    git clone https://github.com/cement-hools/ELMA_test_task
    ```
2. Перейдите в директорию ELMA_test_task
    ```
   cd ELMA_test_task
    ```
3. Запустить docker-compose
    ```
    docker-compose up --build
    ```
4. Проект доступен 
   ```
   http://127.0.0.1:8000/
   http://localhost:8000/
   ```
