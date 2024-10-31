from typing import List
from tortoise import connections
from db import init, close

async def topLocations(limit: str = "5") -> List:
    # returns the top locations with the most identities
    result_instance = []
    await init()
    try:
        query = f"""
            SELECT location, COUNT(*) as location_count
            FROM identity i
            GROUP BY location
            ORDER BY location_count DESC
            LIMIT {limit}
            """
        conn = connections.get("default")
        results = await conn.execute_query(query)
        # result_instance = response_handler_query(results)
        print(f"[INFO] {results}")
        for result in results[1]:
            result_instance.append({"location": result["location"], "count": result["location_count"]})
            print(f"[INFO] Result: {result}")
        print(f"[INFO] Result instance: {result_instance}")
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        await close()
    return result_instance