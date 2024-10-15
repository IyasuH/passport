from models.identity import Identity

def clean_name(name: str) -> str:
    name = name.strip().upper()
    return name

def response_handler_query(result: tuple) -> Identity | None:
    if result[1]:
        result = result[1][0]
        return (Identity(
                id=result['id'],
                name=result['name'],
                father_name=result['father_name'],
                request_no=result['request_no'],
                location=result['location']
            ))
    else:
        return {"message": "No result found"}