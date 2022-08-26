# False Friends 
This project is about distinguishing true and false friends between Spanish and Portuguese. 

## Install

```
sh docker-build.sh
```

## Execute
```
docker run --rm -p 0.0.0.0:8866:8866 --name falsefriends elg_falsefriends:1.0
```
## Use
```
 curl -X POST http://0.0.0.0:8866/class_falsefriends -H 'Content-Type: application/json' -d '{"type":"structuredText", "texts":[{"content":spanish word},{"content":portuguese word}]}'
```

## Example
```
 curl -X POST http://0.0.0.0:8866/class_falsefriends -H 'Content-Type: application/json' -d '{"type":"structuredText", "texts":[{"content":"barata"},{"content":"barata"}]}'
 curl -X POST http://0.0.0.0:8866/class_falsefriends -H 'Content-Type: application/json' -d '{"type":"structuredText", "texts":[{"content":"barato"},{"content":"barato"}]}'
```



# Test
In the folder `test` you have the files for testing the API according to the ELG specifications.
It uses an API that acts as a proxy with your dockerized API that checks both the requests and the responses.
For this follow the instructions:
1) Configure the .env file with the data of the image and your API
2) Launch the test: `docker-compose up`
3) Make the requests, instead of to your API's endpoint, to the test's endpoint:
   ```
   curl -X POST http://0.0.0.0:8866/class_falsefriends -H 'Content-Type: application/json' -d '{"type":"structuredText", "texts":[{"content":"salsa"},{"content":"salsa"}]}'
   ```
4) If your request and the API's response is compliance with the ELG API, you will receive the response.
   1) If the request is incorrect: Probably you will don't have a response and the test tool will not show any message in logs.
   2) If the response is incorrect: You will see in the logs that the request is proxied to your API, that it answers, but the test tool does not accept that response. You must analyze the logs.


    
## Citations:
The original work of this tool is:
- Castro, Santiago & Bonanata, Jairo & Ros{\'a}, Aiala (2018) A High Coverage Method for Automatic False Friends Detection for Spanish and Portuguese",
  booktitle = 	"Proceedings of the Fifth Workshop on NLP for Similar Languages, Varieties and Dialects (VarDial 2018).
- https://github.com/pln-fing-udelar/false-friends
