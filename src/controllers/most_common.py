from typing import List
from tortoise import connections
from db import init, close
from controllers.common_methods import response_handler_query
from type import NameType, Location

async def mostCommonNameLocation(location: Location, limit: str = "1", name_type: NameType = NameType.Name) -> List:
    # returns the most common name in specific location
    result_instance = []
    name_type_ = str(name_type.value)
    name_type_i = "i."+str(name_type.value)
    location_ = str(location.value)
    print(f"[DEBUG] name_type_ is {name_type_}")
    await init()
    try:
        query = f"""
            SELECT {name_type_i}, COUNT(*) as name_count
            FROM identity i
            INNER JOIN passport_fts p ON p.id = i.id
            WHERE passport_fts MATCH ?
            GROUP BY {name_type_i}
            ORDER BY name_count DESC
            LIMIT ?
            """
        query_search_term = f'location: {location_}'
        conn = connections.get("default")
        results = await conn.execute_query(query, [query_search_term, limit])
        # result_instance = response_handler_query(results)
        print(f"[INFO] Results: {results[1]}")
        for result in results[1]:
            result_instance.append({name_type_: result[name_type_], "count": result["name_count"]})
            # result_dict = dict(result)
            print(f"[INFO] Result: {result_instance}")
        # result_instance = results[1][0][name_type_]
        print(f"[INFO] Result instance: {result_instance}")
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        await close()
    return result_instance

async def mostCommonName(name_type: NameType = NameType.Name, limit: str = "1") -> List:
    # returns the most common name in specific location
    result_instance = []
    name_type_ = str(name_type.value)
    name_type_i = "i."+str(name_type.value)
    print(f"[DEBUG] name_type_ is {name_type_}")
    await init()
    try:
        query = f"""
            SELECT {name_type_i}, COUNT(*) as name_count
            FROM identity i
            INNER JOIN passport_fts p ON p.id = i.id
            GROUP BY {name_type_i}
            ORDER BY name_count DESC
            LIMIT {limit}
            """
        conn = connections.get("default")
        results = await conn.execute_query(query)
        # result_instance = response_handler_query(results)
        for result in results[1]:
            result_instance.append({name_type_: result[name_type_], "count": result["name_count"]})
        # result_instance = results[1][0][name_type_]
        print(f"[INFO] Result instance: {result_instance}")
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        await close()
    return result_instance