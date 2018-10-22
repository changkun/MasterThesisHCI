# Mortal

Mortal clickstream prediction service

## Architecture

```
    Browser (front)        Browser (background)        Server
        |                      |                         |
newpage |  message passing     |                         |
clicks  |--------------------->|             request     |
navigate|                      |------------------------>| recieved data
        |                      |             response    | make predictions
        |                      |                         | ...
        |                      |                         | ...
        |    notification      |<------------------------| response results
present |<---------------------|                         |
predicts|                      |                         |
        |                      |                         |
        |    notification      |                         |
        |<---------------------|selected tab changed     |
trigger |                      |                         |
fake    |                      |                         |
clicks  |--------------------->|             request     |
        |                      |------------------------>| recieved data
        |                      |             response    | make predictions
        |                      |                         | ...
        |                      |                         | ...
        |    notification      |<------------------------| response results
present |<---------------------|                         |
predicts|                      |                         |
```

## Protocol

Request

```
{
    "user_id": "f5ecf7d6-83af-93cc-6739-672d92fa8ad8",
    "current_url": https://www.youtube.com/watch?v=skrb2oKGbHE 
    "previous_url": https://www.youtube.com/ 
    "stay_seconds": 4.993 
    "time": 2018-10-21T14:07:39Z
}
```

Response

```
{
    "message": "OK",
    "next": [
        {
            "url": "https://www.youtube.com/",
            "confidence": 95,
        },
        {
            "url": "https://www.youtube.com/notification",
            "confidence": 80,
        },
    ],
    "destination": [
        {
            "url": "https://www.bilibili.com",
            "confidence": 95,
        }
    ],
    "productivity": 10
}
```