"""
=========================
DON'T USE THIS!
websocket simple client
=========================
"""

import asyncio

import click
import websockets


async def hello(uri):
    async with websockets.connect(
            uri) as websocket:
        name = input("What's your name? ")

        await websocket.send(name)
        print(f"> {name}")

        greeting = await websocket.recv()
        print(f"< {greeting}")


async def consumer_handler(websocket, path):
    async for message in websocket:
        await consumer(message)


@click.command()
@click.argument('uri')
def ws(uri):
    """ws test client"""

    asyncio.get_event_loop().run_until_complete(hello(uri))
    pass
