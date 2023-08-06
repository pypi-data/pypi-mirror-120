import asyncio
import websockets
import random
import json

from asyncio import AbstractEventLoop

from . import events

from .intents import Intents

class Gateway(object):

    __slots__ = (
        "token",
        "shard",
        "loop",
        "intents",
        "__sequence",
        "__disconnected",
        "__resume",
        "__session_id",
        "__websocket",
        "__interval",
        "__future",
    )

    def __init__(
        self,
        token,
        shard: list = [0, 1],
        loop: AbstractEventLoop = asyncio.get_event_loop(),
        intents: Intents = Intents.all(),
    ):

        # store required arguments
        self.token = token
        
        # store optional arguments
        self.shard = shard
        self.loop = loop
        self.intents = intents
        
        # initialize internal vars
        self.__sequence = None
        self.__disconnected = False
        self.__resume = False
        
        # store connect future
        self.__future = websockets.connect(
            "wss://gateway.discord.gg/?v=9&encoding=json",
            ping_interval=None,
            ping_timeout=None,
            max_size=None,
            max_queue=None
        )
        
        # add scheduler to loop as task
        self.loop.create_task(self.__connect())

    # honestly just a shortcut to run_forever
    def run(self):
        self.loop.run_forever()

    # send payload
    async def __send_payload(self, payload) -> None:
        await self.__websocket.send(
            json.dumps(payload)
        )

    # send heartbeat
    async def __send_heartbeat(self, wait: int = None) -> None:
        if wait is not None: await asyncio.sleep(wait)
        await self.__send_payload({
            "op": 1,
            "d": self.__sequence
        })
    
    # send identify
    async def __send_identify(self) -> None:
        await self.__send_payload({
            "op": 2,
            "d": {
                "token": self.token,
                "intents": self.intents.flags,
                "properties": {
                    "$os": "linux",
                    "$browser": "discordws",
                    "$device": "discordws",
                }
            }
        })
        
    # send resume
    async def __send_resume(self) -> None:
        self.__resume = False
        await self.__send_payload({
            "op": 6,
            "d": {
                "token": self.token,
                "session_id": self.__session_id,
                "seq": self.__sequence,
            }
        })

    # schedule heartbeat @ interval
    async def __sched_heartbeat(self, interval, wait) -> None:
        await asyncio.sleep(wait + interval)
        while True:
            await self.__send_heartbeat()
            await asyncio.sleep(interval)
            if self.__disconnected == True:
                self.__disconnected == False
                break

    # receive "dispatch" (opcode 0) payload
    async def __recv_dispatch(self, payload) -> None:
        if payload["t"] == "ready":
            self.__session_id = payload["d"]["session_id"]
        await events.handle_event(self, payload)

    # receive "heartbeat" (opcode 1) payload
    async def __recv_heartbeat(self, payload) -> None:
        await self.__send_heartbeat() # send heartbeat post-haste

    # receive "reconnect" (opcode 7) payload
    async def __recv_reconnect(self, payload) -> None:
        self.__resume = True
        await self.__websocket.close()

    # receive "invalid session" (opcode 9) payload
    async def __recv_invalid(self, payload) -> None:
        await self.__websocket.close()

    # receive "hello" (opcode 10) payload
    async def __recv_hello(self, payload) -> None:

        # calculate interval and first random inteval
        interval = payload["d"]["heartbeat_interval"] / 1000
        rnd_interval = interval * random.random()

        # schedule heartbeats
        self.loop.create_task(self.__send_heartbeat(wait=rnd_interval))
        self.loop.create_task(self.__sched_heartbeat(interval, rnd_interval))

        # send identify payload
        await self.__send_identify()

        # resume connection
        if self.__resume:
            await self.__send_resume()

    # receive "heartbeat ack" (opcode 11) payload
    async def __recv_ack(self, payload) -> None:
        pass # TODO: Check if I received and ack and if not reconnect

    # opcode to function map
    __opcodes = {
        0: __recv_dispatch,
        1: __recv_heartbeat,
        7: __recv_reconnect,
        9: __recv_invalid,
        10: __recv_hello,
        11: __recv_ack,
    }

    # handle responses from gateway
    async def __handle(self, response: str):
        payload = json.loads(response) # parse response

        # update stored sequence
        if payload["s"] is not None:
            if self.__sequence is None:
                self.__sequence = payload["s"]
            elif payload["s"] > self.__sequence:
                self.__sequence = payload["s"]

        if payload["op"] in self.__opcodes:
            await self.__opcodes[ payload["op"] ](self, payload)

    # receive loop
    async def __recv(self):
        frame = await self.__websocket.recv()
        if self.__sequence is not None and self.__sequence % 1000 == 0: print(self.__sequence)
        self.loop.create_task(self.__handle(frame))

    # connect to the discord websocket api
    async def __connect(self):

        # websockets async connection iter
        async for websocket in self.__future:

            # store connected websocket
            self.__websocket = websocket

            # main loop
            try:
                while True:
                    await self.__recv()

            # handle connection closed exceptions
            except websockets.ConnectionClosed:
                self.__resume = True
                self.__disconnected = True
                