from controllers.common_methods import clean_name
from models.identity import Identity
from db import init, close
from tortoise import connections
from type import NameType, Location

async def countSpecifcName(name: str, name_type: NameType = NameType.Name) -> int:
    result_instance = 0
    name_type_ = str(name_type.value)
    await init()
    try:
        query_name = f"""
            SELECT count(*)
            FROM identity i
            INNER JOIN passport_fts p ON p.id = i.id
            WHERE passport_fts MATCH ?
            """
        name = clean_name(name)
        query_name_search_term = f'{name_type_}: {name}' # name_type can be father_name, grand_father_name or name, where the deafult is name
        conn = connections.get("default")
        name_number = await conn.execute_query(query_name, [query_name_search_term])
        result_instance = name_number[1][0][0]
        print(f"Number of rows for {name_type_} {result_instance}")
        # print(await Identity.filter(name=name).count()) # this is without using virtual table
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        await close()
    return result_instance

async def countSpecifcNameAndLocation(name: str, location: Location = Location.Addis_Ababa, name_type: NameType = NameType.Name) -> int:
    result_instance = 0
    location_ = str(location.value)
    name_type_ = str(name_type.value)
    location_term = f"i.location = '{location_}'"
    await init()
    try:
        query = f"""
            SELECT count(*)
            FROM identity i
            INNER join passport_fts p ON p.id = i.id
            WHERE passport_fts MATCH ? AND {location_term}
        """
        name = clean_name(name)
        query_search_term = f'{name_type_}: {name}' # name_type can be father_name, grand_father_name or name, where the deafult is name
        conn = connections.get("default")
        name_location_number = await conn.execute_query(query, [query_search_term])
        print(f"[DEBUG] Number of rows for {name_type_} {name} and location {location_} {name_location_number[1][0][0]}")
        result_instance = name_location_number[1][0][0]
        # print(await Identity.filter(name=name, location=location).count()) # with out using vitrual table
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        await close()
    return result_instance

async def countAll() -> int:
    # just returns total number of rows in the table
    all_values = 0
    await init()
    try:
        all_values = await Identity.all().count()
        print(f"[INFO] total number of rows in the table is {all_values}")
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        await close()
    return all_values

async def countSpecificLocation(location: Location) -> int:
    location_ = str(location.value)
    result_instance = 0
    await init()
    try:
        query_location = f"""
            SELECT count(*)
            FROM identity i
            INNER JOIN passport_fts p ON p.id = i.id
            WHERE passport_fts MATCH ?
            """
        query_location_search_term = f'location: {location_}'
        conn = connections.get("default")
        location_number = await conn.execute_query(query_location, [query_location_search_term])
        result_instance = location_number[1][0][0]
        print(f"Number of rows for specific location {location_} is {location_number[1][0][0]}")
        # print(await Identity.filter(location=location).count()) # without virtual table
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        await close()
    return result_instance
