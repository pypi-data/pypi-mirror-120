## drone-api-client ##

drone-api-client - is a client for provide integration with Drone server

General information about [Drone server](https://docs.drone.io/api/overview/)

**Requirements**
- requests

**Installation**
```shell
pip install drone-api-client
```

**Configuration**
```shell
from drone_api_client.drone_api_client import DroneApi
drone = DroneApi('your_host', 'your_token', 'repository_name')
```
**Features in version: 0.2**
- Supported api:
  - cron
  - secrets
  - user
  - users
- Change repository name without initialization new class instance

**TODO**
- Add support:
  - builds
  - repos
  - templates

**Usage examples**
```shell
cron_jobs = drone.cron.get_cron_list()
secrets = drone.secrets.get_secrets()
```
