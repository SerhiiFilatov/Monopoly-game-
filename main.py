from game import Monopoly

import asyncio

async def main():
    f = Monopoly()
    await f.run()

if __name__ == '__main__':
    asyncio.run(main())