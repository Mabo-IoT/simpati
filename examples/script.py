from context import Request, Client,Transition
import asyncio


conf = {
    "host": "127.0.0.1",
    "port": 20000
}

cmds=[{
        "cmd": "11004",
        "charmber_index":"1",
        "id":"1",
    },
    {
        "cmd": "12002",
        "charmber_index":"1",
        "id":"1",
    },
    {
        "cmd": "11004",
        "charmber_index":"1",
        "id":"1",
    },
    {
        "cmd": "17009",
        "charmber_index":"1",
        "id":"1",
    },]

def client(conf, loop):
    client = Client(conf["host"], conf["port"], loop)
    return client


async def query(client, cmd):
    try:
        data = await client.read(cmd["cmd"], cmd["charmber_index"], cmd["id"])
    except Exception as e:
        print(e)
    return data
 


def main():
    loop = asyncio.get_event_loop()
    # first loop to create clients 
    clients_coroutine = [Client.create(conf["host"], conf["port"], loop) for i in range(len(cmds))]
    create_clients_tasks = [asyncio.ensure_future(client) for client in clients_coroutine]
    loop.run_until_complete(asyncio.wait(create_clients_tasks))
    # loop.close()

    clients = [task.result() for task in create_clients_tasks]
    i = 1
    print(loop.is_running())
    while True:
        # loop = asyncio.get_event_loop()
        
        ## get responses list
        resps = []
        tasks = [asyncio.ensure_future(query(client, cmd)) for client, cmd in zip(clients,cmds)]
        print(loop.is_running())
        loop.run_until_complete(asyncio.wait(tasks))
        print(loop.is_running())
        for task in tasks:
            print(task.result().data)
            resps.append(task.result())
        
        i = i + 1
        print("run for {} ".format(i))
        ## handle response list

        order_keys = {
            ("11004", "1"): "temperature",
            ("12002", "1"): "humidity",
            ("17009", "1"): "temp error",
        }
        
        data_dict = {}
        for resp in resps:
            key = order_keys[(resp.cmd,resp.num)]
            value =  resp.data
            data_dict.update({key: value})
        
        print(data_dict)
    
    
if __name__ == '__main__':
    main()    

