# About
This is an api which allows users to add rooms and collect temperatures of those rooms.
## API: Home_temperature_collect_api
technology usage: postgreSQL(AWS service), flask
### ADD ROOM
.../api/room  (within this post request, send json data: {"roomname":"LIVING ROOM"})

### ADD TEMPERATURE
.../api/temp (within this post request, send json data: {
"roomid":1,
"temperature":67,
"date": "06-12-2023 11:45:03"
} )

### get all temerature data entries for a room
..../api/room/1 (formate: /api/room/roomid)

output: name of room and all temperature entries
