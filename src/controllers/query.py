from tortoise import connections
from controllers.common_methods import response_handler_query
from models.identity import Identity
from db import init, close

async def full_search(searArg: str) -> None:
    # here implement full text search using passport_fts with the name, father_name and grand_father_name columns - based on the argument given
    full_name = searArg.split(" ")
    if len(full_name) >= 3:
        name = full_name[0]
        father_name = full_name[1]
        grand_father_name = full_name[2]
    elif len(full_name) == 2:
        name = full_name[0]
        father_name = full_name[1]
        grand_father_name = ""
    elif len(full_name) == 1:
        name = full_name[0]
        father_name = ""
        grand_father_name = ""

async def queryById(id: int) -> Identity | None:
    # here impletemnt full text search using passport_fts with only the id column
    result_instance = None
    await init()
    try:
        query = f"""
            SELECT i.id, i.name, i.father_name, i.request_no, i.location
            FROM identity i
            INNER JOIN passport_fts p ON p.id = i.id
            WHERE passport_fts MATCH ?
            """
        query_search_term = f'id: {id}'
        conn = connections.get("default")
        results = await conn.execute_query(query, [query_search_term])
        result_instance = response_handler_query(results)
        # result_instance = await Identity.get(id=id) # without using virtual table
        print(f"[INFO] {result_instance}")
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        await close()
    return result_instance

async def queryByRequestNo(request_no: str) -> Identity | None:
    # only returns the first result - and there should be only one result
    # here implement full text search using passport_fts with only the request_no column
    result_instance = None
    await init()
    try:
        query = f"""
            SELECT i.id, i.name, i.father_name, i.request_no, i.location
            FROM identity i
            INNER JOIN passport_fts p ON p.id = i.id
            WHERE passport_fts MATCH ?
            """
        query_search_term = f'request_no: {request_no}'
        conn = connections.get("default")
        results = await conn.execute_query(query, [query_search_term])
        result_instance = response_handler_query(results)
        # result_instance = await Identity.get(id=id) # without using virtual table
        print(f"[INFO] {result_instance}")

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        await close()
    return result_instance
