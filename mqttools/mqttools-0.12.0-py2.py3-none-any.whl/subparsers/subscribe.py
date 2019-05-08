import asyncio

from ..client import Client
from . import try_decode


async def subscriber(host, port, client_id, topic, qos, keep_alive_s):
    client = Client(host,
                    port,
                    client_id,
                    keep_alive_s=keep_alive_s,
                    topic_alias_maximum=10)

    await client.start()
    await client.subscribe(topic, qos)

    while True:
        topic, message = await client.messages.get()

        if topic is None:
            print('Broker connection lost!')
            break

        print(f'Topic:   {topic}')
        print(f'Message: {try_decode(message)}')


def _do_subscribe(args):
    asyncio.run(subscriber(args.host,
                           args.port,
                           args.client_id,
                           args.topic,
                           args.qos,
                           args.keep_alive))


def add_subparser(subparsers):
    subparser = subparsers.add_parser('subscribe',
                                      description='Subscribe for given topic.')
    subparser.add_argument('--host',
                           default='broker.hivemq.com',
                           help='Broker host (default: broker.hivemq.com).')
    subparser.add_argument('--port',
                           type=int,
                           default=1883,
                           help='Broker port (default: 1883).')
    subparser.add_argument('--client-id',
                           help='Client id (default: mqttools-<UUID[0..14]>).')
    subparser.add_argument('--qos',
                           type=int,
                           default=0,
                           help='Quality of service (default: 0).')
    subparser.add_argument('--keep-alive',
                           type=int,
                           default=0,
                           help=('Keep alive time in seconds (default: 0). Give '
                                 'as 0 to disable keep alive.'))
    subparser.add_argument('topic', help='Topic to subscribe for.')
    subparser.set_defaults(func=_do_subscribe)
