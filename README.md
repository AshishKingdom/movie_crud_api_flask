# Movies CRUD API with Flask and SQLAlchmeny

## How to run?

### Using Docker
1. Build the image

```sh
sudo docker build -t flask_app:latest .
```

2. Run the image

```sh
sudo docker run -it --rm -p 5000:5000 flask_app:latest
```

### Without Docker

1. Create a virtual environment

```sh
python3 -m venv .venv
```

2. Activate the environment

```sh
source .venv/bin/activate
```

3. Install the required packages

```sh
pip install -r requirements.txt
```

4. Run the application
```sh
python app.py
```

## API Documentation

### Movies Route

#### Create new movie

Route

```http
POST /movies/create
```

Request Header
| Key          | Value              |
---------------|---------------------
|Authorization | Bearer <JWT_TOKEN> |

Request Body
```json
{
    "title": "whodunit mystery",
    "description": "unmask the culprit",
    "release_date": "2018-09-14",
    "director": "Sleuth",
    "genre": "mystery",
    "avg_rating": 7.7,
    "ticket_price": 2100,
    "cast": "Detective, Suspect"
}
```

Response
```json
{
    "message": "Movie created successfully"
}
```

#### Update the existing movie
Route

```http
PUT /movies/update/<movie_id:int>
```
Route Parameter
| Key          | Value              |
---------------|---------------------
|Movie ID      | ID of the movie    |

Request Header
| Key          | Value              |
---------------|---------------------
|Authorization | Bearer <JWT_TOKEN> |

Request Body
```json
{
    "title": "whodunit mystery",
    "description": "unmask the culprit",
    "release_date": "2018-09-14",
    "director": "Sleuth",
    "genre": "mystery",
    "avg_rating": 7.7,
    "ticket_price": 2100,
    "cast": "Detective, Suspect"
}
```

Response
```json
{
    "message": "Movie updated successfully"
}
```

#### Deleting a movie
Route

```http
DELETE /movies/delete/<movie_id:int>
```
Route Parameter
| Key          | Value              |
---------------|---------------------
|Movie ID      | ID of the movie    |

Request Header
| Key          | Value              |
---------------|---------------------
|Authorization | Bearer <JWT_TOKEN> |


Response
```json
{
    "message": "Movie deleted successfully"
}
```

#### Get movies by ID
Route

```http
GET /movies/get/<movie_id:int>
```
Route Parameter
| Key          | Value              |
---------------|---------------------
|Movie ID      | ID of the movie    |

Example
```http
GET /movies/get/2
```

Response
```json
{
    "avg_rating": 5.5,
    "cast": "Raj, Anjali",
    "description": "this is a very cool description",
    "director": "Mr Mommy",
    "genre": "comedy",
    "id": 2,
    "release_date": "2019-04-23",
    "ticket_price": 1800.0,
    "title": "apple pie"
}
```

#### Get movies with page, filter and sorting parameters

Route

```http
GET /movies/all
```

Route Parameter
| Key          | Value                                       |
---------------|----------------------------------------------
| page         | page number of the result to be returned    |
| sort_by      | sorting criteria (price or release_year)    |
| filter_by    | filter criteria  (genere, director, year)   |
| filter_value | the actual value of the filter              |

Example:
```http
GET movies/get/all?sort_by=price&filter_by=genre&filter_value=action&page=1
```

Response
```json
[
    {
        "avg_rating": 8.6,
        "cast": "Tom, Jessica",
        "description": "heart-pounding excitement",
        "director": "Adrenaline Junkie",
        "genre": "action",
        "id": 8,
        "release_date": "2021-11-05",
        "ticket_price": 2300.0,
        "title": "action-packed thriller"
    },
    {
        "avg_rating": 9.5,
        "cast": "Superman, Batman",
        "description": "epic battle of good vs. evil",
        "director": "Marvelous Director",
        "genre": "action",
        "id": 12,
        "release_date": "2022-11-15",
        "ticket_price": 2500.0,
        "title": "superhero showdown"
    }
]
```

#### Search movie

Route

```http
GET /movies/search
```

Route Parameter
| Key          | Value                                       |
---------------|----------------------------------------------
| search_param | the parameter on which search is done       |
| search_value | the actual seach value                      |

Example:
```http
GET movies/search?search_param=cast&search_value=Alex
```

Response
```json
[
    {
        "avg_rating": 9.0,
        "cast": "Alex, Lisa",
        "description": "explore the universe",
        "director": "Captain Cosmos",
        "genre": "sci-fi",
        "id": 6,
        "release_date": "2022-05-10",
        "ticket_price": 2500.0,
        "title": "space adventure"
    },
    {
        "avg_rating": 9.1,
        "cast": "Alex, Sarah",
        "description": "journey to the stars",
        "director": "Stellar Explorer",
        "genre": "sci-fi",
        "id": 17,
        "release_date": "2022-08-30",
        "ticket_price": 2400.0,
        "title": "space odyssey"
    }
]
```

### User Route

#### User Registration
Route

```http
PUT /user/register
```

Request Body
```json
{
    "name":"Test",
    "email":"test@gmail.com",
    "password":"12345"
}
```

Response
```json
{
    "message": "User created successfully"
}
```

#### User Login
Route

```http
PUT /user/login
```

Request Body
```json
{
    "email":"test@gmail.com",
    "password":"12345"
}
```

Response
```json
{
    "access_token": "<JWT_TOKEN>"
}
```