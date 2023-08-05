import asyncio

from tracardi.service.storage.elastic_client import ElasticClient
from tracardi.service.storage.sql import to_sql_query


async def main():
    es = ElasticClient.instance()
    q = to_sql_query("tracardi-event", query="type='view' and event_server.browser.browser.engine='xxx'")
    print(q)
    q = await es.translate(q)
    print(q)
    await es.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()