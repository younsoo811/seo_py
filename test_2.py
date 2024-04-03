import json


data = {
  "event_id": -1,
  "camera_id": "ecca8b02041242729ba512392dbc5d0d:0",
  "address": "192.168.0.68",
  "profile_id": 2,
  "token": "pad1",
  "area_id": 1,
  "points": [],
  "scenario_id": 2,
  "scenario": "배회",
  "object_id": "20240328100816_12075",
  "tags": [
    "person"
  ],
  "frame_num": 191842,
  "cam_dt": 1711594994780011000,
  "ed_dt": 1711594995859,
  "desc": "",
  "thumbnail": ""
}

with open('event.json', 'w') as json_file:
    json.dump(data, json_file)