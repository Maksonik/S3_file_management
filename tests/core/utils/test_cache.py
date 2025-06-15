import asyncio
from datetime import UTC, datetime, timedelta

from sfm.core.utils.async_cache import async_cache


async def test_async_cache():
    ttl_seconds = 5

    @async_cache(ttl_seconds)
    async def cached_func_with_ttl(seconds: int):
        return datetime.now(tz=UTC) - timedelta(seconds=seconds)

    @async_cache()
    async def cached_func_without_ttl(seconds: int):
        return datetime.now(tz=UTC) - timedelta(seconds=seconds)

    result_with_ttl_1 = await cached_func_with_ttl(1)
    result_without_ttl_1 = await cached_func_without_ttl(1)
    await asyncio.sleep(1)
    result_with_ttl_2 = await cached_func_with_ttl(1)
    result_without_ttl_2 = await cached_func_without_ttl(1)
    assert result_with_ttl_1 == result_with_ttl_2
    assert result_without_ttl_1 == result_without_ttl_2

    await asyncio.sleep(ttl_seconds)

    result_with_ttl_3 = await cached_func_with_ttl(1)
    result_without_ttl_3 = await cached_func_without_ttl(1)
    assert result_with_ttl_1 != result_with_ttl_3
    assert result_without_ttl_1 == result_without_ttl_3
    await asyncio.sleep(1)
    result_with_ttl_4 = await cached_func_with_ttl(1)
    result_without_ttl_4 = await cached_func_without_ttl(1)
    assert result_with_ttl_3 == result_with_ttl_4
    assert result_without_ttl_3 == result_without_ttl_4
