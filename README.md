# Backend Endpoints

# Contents
+ [Get All Places](#getPlaces)
+ [Get Place by id](#getPlace)
+ [Get info abot currently authorized place](#currentPlace)
+ [Add new Place](#postPlace)
+ [Update Place](#patchPlace)
+ [Remove Place](#deletePlace)
+ [Login](#login)



### <a name="getPlaces"></a> Get All Places [GET /places]
+ Response 200 (application/json)
```
[
  {
    "address": {
      "city": "Groningen", 
      "country": "Netherlands", 
      "house_number": "2", 
      "postcode": "9321CV", 
      "street": "Greenstraat"
    }, 
    "description": "We have good food!", 
    "email": "contact@ksf.world", 
    "free_seats": 10, 
    "id": 1, 
    "name": "KFS", 
    "phone_number": "+123456789", 
    "total_seats": 20, 
    "type": "fast food", 
    "website": "https://www.KSFsuperwebsite3000.world"
  }, 
  {
    "address": {
      "city": "Amsterdam", 
      "country": "Netherlands", 
      "house_number": "3a", 
      "postcode": "9821CV", 
      "street": "Redstraat"
    }, 
    "description": null, 
    "email": null, 
    "free_seats": 75, 
    "id": 2, 
    "name": "Burgers Queen", 
    "phone_number": null, 
    "total_seats": 120, 
    "type": "restaurant", 
    "website": null
  }, 
  {
    "address": {
      "city": "Amsterdam", 
      "country": "Netherlands", 
      "house_number": "12", 
      "postcode": "9342CV", 
      "street": "Whitestraat"
    }, 
    "description": null, 
    "email": null, 
    "free_seats": 2, 
    "id": 3, 
    "name": "MacersDruft", 
    "phone_number": null, 
    "total_seats": 20, 
    "type": "bar", 
    "website": null
  }
]
```
### <a name="getPlace"></a> Get Place? by id [GET /places/<place_id>]
If there is no place with that id returns status code **404**.
+ Response 200 (application/json)
```
Request: GET /places/1
Response:
{
  "address": {
    "city": "Groningen", 
    "country": "Netherlands", 
    "house_number": "2", 
    "postcode": "9321CV", 
    "street": "Greenstraat"
  }, 
  "description": "We have good food!", 
  "email": "contact@ksf.world", 
  "free_seats": 10, 
  "id": 1, 
  "name": "KFS", 
  "phone_number": "+123456789", 
  "total_seats": 20, 
  "type": "fast food", 
  "website": "https://www.KSFsuperwebsite3000.world"
}
```

### <a name="currentPlace"></a> Get info abot currently authorized place [GET /current-place]
**Requiers** header  'Authorization' with this authorization token in this format: "Bearer < token >'"
+ Response 200 (application/json) - 
Request: GET /currentPlace (while authorized as restourant with id 1)
Response:
[Same as here](#getPlace)

### <a name="postPlace"></a> Add new Place [POST /places]
Request should contain JSON with this fields with information about the place:
'username', 'password', 'name', 'description', 'type', 'total_seats', 'email', 'website', 'phone_number'
+ Example
Request: POST /places
Response: 
```
Request: GET /places/1
Response:
{ "place":
	{
	  "address": {
	    "city": "Groningen", 
	    "country": "Netherlands", 
	    "house_number": "2", 
	    "postcode": "9321CV", 
	    "street": "Greenstraat"
	  }, 
	  "description": "We have good food!", 
	  "email": "contact@ksf.world", 
	  "free_seats": 10, 
	  "id": 1, 
	  "name": "KFS", 
	  "phone_number": "+123456789", 
	  "total_seats": 20, 
	  "type": "fast food", 
	  "website": "https://www.KSFsuperwebsite3000.world"
	},
 "token" : "secret_token"
}
```

### <a name="patchPlace"></a> Update place by id [PATCH /places/<place_id>]
**Requiers** header  'Authorization' with this authorization token in this format: "Bearer < token >'"
If place_id is not equal to id of currently authorized place - will return Response with status code **403**.
JSON in reques (with information that has to be changed) can contain those fields:
'username', 'password', 'name', 'description', 'type', 'total_seats', 'free_seats', 'email', 'website', 'phone_number'

+ Response 200 (application/json) - 
Request: PATCH /places/1 (while authorized as restourant with id 1)
Response (info about updated place): 
[Same as here](#getPlace)

### <a name="#deletePlace"></a> Remove place by id [PATCH /places/<place_id>]
**Requiers** header  'Authorization' with this authorization token in this format: "Bearer < token >'"
If place_id is not equal to id of currently authorized place - will return Response with status code **403**.

+ Response 200 (application/json) - 
Request: DELETE /places/1 (while authorized as restourant with id 1)
Response (info about deleted place):
[Same as here](#getPlace)

### <a name="#login"></a> Login [POST /login]
+ Request have to contain JSON with this fields: username, password. Otherwise it will return status code **400** and JSON with {'success': false, 'message': 'Bad username or password'}
+ If pair of password and username doesn't exist in the system - it will return status code **401** and JSON with {'success': false, 'message': 'Bad username or password'}.

+ Example: 
```
Request: POST login
Response 200:
{ 
	"succsess: true",
	"token": "secret_token"
	"place" : [Info about the place]
}
```
