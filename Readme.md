## Simulator Control API
### Get current status
```bash
curl -XGET 'localhost:5000/controller'
$ curl -XGET 'localhost:5000/controller'
{
  "interval": 15,
  "on": true
}
```
### Turn off
```bash
$ curl -XPUT 'localhost:5000/controller?on=False'
{
  "interval": 15,
  "on": false
}
```

### Turn on
```bash
$ curl -XPUT 'localhost:5000/controller?on=True'
{
  "interval": 15,
  "on": false
}
```

### Set interval in seconds
```bash
curl -XPUT 'localhost:5000/controller?interval=2'
```

### Turn on and set interval in seconds
```bash
curl -XPUT 'localhost:5000/controller?on=True&interval=2'
```

## Data API
### Summary report
```bash
curl -XGET "localhost:5000/summary?from_ts='2017-07-10T22:19:47'&to_ts='2017-07-11T21:23:07.534027'"
{
  "avg-humidity": 49.70745928338762,
  "avg-precipitation": 51.12104234527688,
  "avg-temperature": 25.41814332247557,
  "avg-wind_speed": 26.49758957654723,
  "max-humidity": 99.78,
  "max-precipitation": 99.54,
  "max-temperature": 49.82,
  "max-wind_speed": 49.99,
  "min-humidity": 0.44,
  "min-precipitation": 0.59,
  "min-temperature": 0.01,
  "min-wind_speed": 0.09
}
```

