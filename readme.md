## simpati
a lib to communicate with weiss simpati software.

## usage

```
from simpati import Client
import asyncio

conf = {
    "host":"127.0.0.1",
    "port": 20000,
}

loop = asyncio.get_event()

## create asyncio client, feel free to create multiple client if server support
client = Client.create(conf["host"], conf["port"], loop)
loop.run_until_complete(asyncio.ensure_future(client))

## get data asyn




```