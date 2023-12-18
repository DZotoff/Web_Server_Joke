## Joke
This is our first joke API.
Api provides you to retrieve all jokes which are located in our database, vote for jokes and add new jokes. Enjoy!

### Retrieve all jokes
Returns all existing jokes.
```endpoint
GET /api/jokes
```
#### Example request

```curl
curl http://195.148.217.81:8080/api/jokes
```

#### Example response
```json
[
  {
    "_id": 1,
    "created": "2023-04-14 15:24:40",
    "downvotes": 0,
    "text": "Where did Joe go after getting lost on a minefield? Everywhere.",
    "upvotes": 0
  },
  {
    "_id": 2,
    "created": "2023-04-14 15:24:40",
    "downvotes": 0,
    "text": "I threw a boomerang a few years ago. I now live in constant fear.",
    "upvotes": 0
  },
  {
    "_id": 3,
    "created": "2023-04-14 15:24:40",
    "downvotes": 0,
    "text": "I made a graph of all my past relationships... It has an \"ex\" axis and a \"why\" axis.",
    "upvotes": 0
  }
]
```
### Add a new joke without category
Creates a new absolutely perfect joke.
Please fill the current form to add the new one joke.
```endpoint
POST /api/jokes
```
Property | Description
---|---
`text` | (mandatory) a content of the joke

#### Example request
```curl
$ curl --header "Content-Type: application/json" --request POST --data "{\"text\":\"Good joke!\"}" http://195.148.217.81:8080/api/jokes
```

#### Example response
```json
{"_id":6,
"created":"2023-04-17 11:21:53",
"downvotes":0,
"text":"Good joke!",
"upvotes":0}
```
### Retrieve a joke by id
Search the joke by joke id.
```endpoint
GET /api/jokes/{n}
```

#### Example request
```curl
curl http://195.148.217.81:8080/api/jokes/1
```

#### Example response
```json
{
  "_id":1,
  "created":"2023-04-17 11:21:38",
  "downvotes":0,
  "text":"Where did Joe go after getting lost on a minefield? Everywhere.",
  "upvotes":0
}
``` 
### Retrieve a random joke 
Retrieves a random joke from all jokes in the database

```endpoint
GET /api/jokes/random
```

#### Example request

```curl
curl http://195.148.217.81:8080/api/jokes/random
```

#### Example response

```json
{"_id":1,
"created":"2023-04-17 11:21:38",
"downvotes":0,
"text":"Where did Joe go after getting lost on a minefield? Everywhere.","upvotes":0}
``` 

### Vote of like

Gives a joke (by id) a vote of like

```endpoint
GET /api/jokes/{n}/upvote
```

#### Example request

```curl
curl --request POST 195.148.217.81:8080/api/jokes/3/upvote
```

#### Example response
```json
{"_id":3,
"created":"2023-04-17 11:21:38",
"downvotes":0,
"text":"I made a graph of all my past relationships... It has an \"ex\" axis and a \"why\" axis.",
"upvotes":1}
```

### Vote of dislike

Gives a joke (by id) a vote of dislike

```endpoint
POST /api/jokes/{n}/downvote 
```

#### Example request

```curl
curl --request POST 195.148.217.81:8080/api/jokes/3/downvote
```

#### Example response
```json
{"_id":3,
"created":"2023-04-17 11:21:38",
"downvotes":1,
"text":"I made a graph of all my past relationships... It has an \"ex\" axis and a \"why\" axis.",
"upvotes":1}
```


### List all categories
Retrieve a list of categories
```endpoint
GET	/api/categories
```
#### Example request
```curl
curl http://195.148.217.81:8080/api/categories
```

#### Example response
```json
[
  {"_id":1,
  "created":"2023-04-17 11:21:38",
  "name":"Dark humor"},
  {"_id":2,
  "created":"2023-04-17 11:21:38",
  "name":"Metahumor"},
  {"_id":3,
  "created":"2023-04-17 11:21:38",
  "name":"Puns"},
  {"_id":4,
  "created":"2023-04-17 11:55:53",
  "name":"Funny category!"},
  {"_id":5,
  "created":"2023-04-17 11:56:22",
  "name":"Bad jokes"}
]
```

### Add a new category
Creates a new category. You can add new jokes to 
```endpoint
POST /api/categories
```
#### Example request
```curl
curl --header "Content-Type: application/json" --request POST --data "{\"name\":\"Bad jokes\"}" http://195.148.217.81:8080/api/categories
```

Property | Description
---|---
`name` | (mandatory) the name of the category

#### Example response
```json
{"_id":5,
"created":"2023-04-17 11:56:22",
"name":"Bad jokes"}
```
### List  all jokes per category
Retrieve a list of jokes for a category 
```endpoint
GET /api/categories/{n}/jokes
```
#### Example request
```curl
curl --request GET http://195.148.217.81:8080/api/categories/2/jokes
```

#### Example response
```json
[
  {"_id":4,
  "created":"2023-04-17 11:21:38",
  "downvotes":0,
  "text":"A guy walks into a bar... Which is unfortunate because he has a drinking problem.",
  "upvotes":0},
  {"_id":1,"created":"2023-04-17 11:21:38",
  "downvotes":0,
  "text":"Where did Joe go after getting lost on a minefield? Everywhere.","upvotes":0}
]
```

### Add a new joke to a category
Adds a new perfectly balanced joke for a category.
```endpoint
POST /api/categories/{n}/jokes
```
Property | Description
---|---
`text` | (mandatory) a content of the joke

#### Example request
```curl
$ curl --header "Content-Type: application/json" --request POST --data "{\"text\":\"Joke in category!\"}" 195.148.217.81:8080/api/categories/1/jokes
```

#### Example response
```json
null
```

### Add a  joke to a category via joke id
Add an existing joke to a category by joke id
```endpoint
POST /api/categories/{n}/jokes/add/{i}
```
#### Example request
```curl
$ curl --request POST 195.148.217.81:8080/api/categories/2/jokes/add/1
```
#### Example response
```json
{"_id":6,
"created":"2023-04-17 11:21:53",
"downvotes":0,
"text":"Good joke!",
"upvotes":0}
```

### Add a random joke to a category via joke id

```endpoint
GET	/api/categories/{n}/jokes/random
```
#### Example request
```curl
$ curl --request GET 195.148.217.81:8080/api/categories/2/jokes/random
```
#### Example response
```json
{"_id":4,
"created":"2023-04-17 11:21:38",
"downvotes":0,
"text":"A guy walks into a bar... Which is unfortunate because he has a drinking problem.",
"upvotes":0}
```



















