# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['rpcx']

package_data = \
{'': ['*']}

install_requires = \
['anyio>=3.3.1,<4.0.0',
 'asyncstdlib>=3.10.1,<4.0.0',
 'msgpack>=1.0.2,<2.0.0',
 'websockets>=10.0,<11.0']

setup_kwargs = {
    'name': 'rpcx',
    'version': '0.1.1',
    'description': 'Asynchronous RPC client/server with streaming support',
    'long_description': '# RPCx\n\n[![CI](https://github.com/uSpike/rpcx/actions/workflows/main.yml/badge.svg)](https://github.com/uSpike/rpcx/actions/workflows/main.yml)\n\nAsynchronous RPC server/client for Python 3.7+ with streaming support.\n\n- Async backend implemented by `anyio` providing support for `asyncio` and `trio`.\n- Generic stream support for transport includes Websockets.\n- Messages are serialized with `msgpack`.\n\n```python\nimport math\n\nimport anyio\nfrom anyio.streams.stapled import StapledObjectStream\nfrom rpcx import RPCClient, RPCManager, RPCServer, Stream\n\n\nasync def add(a: int, b: int) -> int:\n    """Add two numbers"""\n    return a + b\n\n\nasync def fibonacci(n: int, stream: Stream) -> None:\n    """Stream each number as computed in the Fibonacci sequence for a given starting number"""\n    a, b = 0, 1\n\n    for i in range(n):\n        await stream.send(i)\n        a, b = b, a + b\n\n\nasync def sum(stream: Stream) -> int:\n    """Stream numbers from client and return the sum"""\n    total = 0\n\n    async for num in stream:\n        total += num\n\n    return total\n\n\nmanager = RPCManager()\nmanager.register("add", add)\nmanager.register("fibonacci", fibonacci)\nmanager.register("sum", sum)\n\n\nasync def main() -> None:\n    # Create two connected stapled streams to simulate a network connection\n    server_send, server_receive = anyio.create_memory_object_stream(math.inf, item_type=bytes)\n    client_send, client_receive = anyio.create_memory_object_stream(math.inf, item_type=bytes)\n    server_stream = StapledObjectStream(client_send, server_receive)\n    client_stream = StapledObjectStream(server_send, client_receive)\n\n    server = RPCServer(server_stream, manager)\n\n    async with anyio.create_task_group() as task_group:\n        task_group.start_soon(server.serve)\n\n        async with RPCClient(client_stream) as client:\n            # Simple method call\n            assert await client.request("add", 1, 2) == 3\n\n            # Streaming (server to client) example\n            async with client.request_stream("fibonacci", 6) as stream:\n                async for num in stream:\n                    print(num)  # 1, 1, 2, 3, 5, 8\n\n            # Streaming (client to server) example\n            async with client.request_stream("sum") as stream:\n                for num in range(10):\n                    await stream.send(num)\n\n            assert await stream == 45\n\n\nanyio.run(main)\n```\n\n# Development\n\n## Installation\n\nRun `poetry install` to install the project.\n\n## Execute tests\n\nExecute `poetry run tox` to run tests for all python environments.\n\n## Pre-commit hooks\n\nExecute `poetry run pre-commit run -a` to run all linters, formatters, and checks.\n',
    'author': 'Jordan Speicher',
    'author_email': 'jordan@jspeicher.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/uSpike/rpcx',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
