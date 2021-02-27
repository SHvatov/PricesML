# PricesML
Basic course project, which consists of bot, WS and a neural network.

## WS 
### Specs
At the moment WS supports the following requests:
```http request
POST http://localhost:8080/data
Content-Type: application/json

{
  "requestedProduct": string, // defines the query itself
  "limit": int, optinal, // defines the max number of products to fetch 
  "requestFrom": string // ALL, OKEY, LENTA - shop to fetch data from
}
```

### Example
Request:
```http request
POST http://localhost:8080/data
Content-Type: application/json

{
  "requestedProduct": "сок яблочный",
  "limit": 3,
  "requestFrom": "ALL"
}
```

Response:
```http request
POST http://localhost:8080/data

HTTP/1.1 200 OK
Content-Type: application/json; charset=UTF-8
Connection: keep-alive
transfer-encoding: chunked

[
  {
    "regularPrice": 11.59,
    "discountPrice": 10.99,
    "title": "Нектар 365 ДНЕЙ Персиково-яблочный, 0.2л",
    "shop": "LENTA",
    "pathToPicture": "https://lenta.gcdn.co/globalassets/1/-/53/35/93/304079_3.png?preset=thumbnail"
  },
  {
    "regularPrice": 12.59,
    "discountPrice": 11.89,
    "title": "Нектар 365 ДНЕЙ Яблочный, 0.2л",
    "shop": "LENTA",
    "pathToPicture": "https://lenta.gcdn.co/globalassets/1/-/16/63/76/317039_3.png?preset=thumbnail"
  },
  {
    "regularPrice": 12.99,
    "discountPrice": 12.99,
    "title": "Нектар Фрутоняня Малышам яблочно-персиковый неосветленный с 5 мес  125мл",
    "shop": "OKEY",
    "pathToPicture": "/wcsstore/OKMarketCAS/cat_entries/755664/755664_thumbnail.jpg"
  }
]
```
