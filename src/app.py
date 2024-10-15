from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

import uvicorn

from controllers.query import queryById, queryByRequestNo
from controllers.count import countAll, countSpecifcName, countSpecifcNameAndLocation, countSpecificLocation
from controllers.most_common import mostCommonName, mostCommonNameLocation
from type import Location, NameType

limiter = Limiter(key_func=get_remote_address, default_limits=["5/minute"])

app = FastAPI(debug=True)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded,_rate_limit_exceeded_handler)

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:3001",
    "http://localhost:8001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])

@app.get("/api/v1")
@limiter.limit("5/minute")
async def trial(request: Request):
    return {"message": "Hello World"}

@app.get("/api/v1/count_all")
@limiter.limit("5/minute")
async def root(request: Request):
    """
    To get total number of rows in the table
    """
    all_values = await countAll()
    print(f"[INFO] Total number of rows in the table is {all_values}")
    return {"number of rows": f"{all_values}"}

@app.get("/api/v1/count_identity_location/{location}")
@limiter.limit("5/minute")
async def count_identity_location(location: Location, request: Request):
    """
    To count identity information by location
        :param location: location - Location
    """
    count = await countSpecificLocation(location)
    print(f"count is {count}")
    return count

@app.get("/api/v1/count_identity_name_location/{name}/{location}/{name_type}")
@limiter.limit("5/minute")
async def count_identity_name_location(request: Request, name: str, location: Location, name_type: NameType = NameType.Name):
    """
    To count identity information by name and location
        :param name: name - str
        :param location: location - Location
    """
    count = await countSpecifcNameAndLocation(name, location, name_type)
    print(f"count is {count}")
    return count

@app.get("/api/v1/count_identity_name/{name}/{name_type}")
@limiter.limit("5/minute")
async def count_identity_name(request: Request, name: str, name_type: NameType = NameType.Name):
    """
    To count identity information by name
        :param name: name - str
    """
    count = await countSpecifcName(name, name_type)
    print(f"count is {count}")
    return count

@app.get("/api/v1/identity/{id}")
@limiter.limit("5/minute")
async def query_identity_id(id: int, request: Request):
    """
    To get identity information by id
        :param id: identity id - int
    """
    identity = await queryById(id)
    if identity is None:
        return {"message": "Identity not found"}
    else:
        print(f"identity is {identity}")
        return identity
    
@app.get("/api/v1/common_name/{location}/{limit}/{name_type}")
@limiter.limit("5/minute")
async def common_name(request: Request, location: Location, limit: int = 1, name_type: NameType = NameType.Name):
    """
    Most common name for given location
        :parma location: Location
    """
    name_list = await mostCommonNameLocation(location, limit, name_type)
    if name_list == []:
        return {"message": "result not found"}
    else:
        print(f"name is {name_list}")
        return name_list
    
@app.get("/api/v1/common_name/{limit}/{name_type}")
@limiter.limit("5/minute")
async def common_name(request: Request, limit: int = 1, name_type: NameType = NameType.Name):
    """Most common name
    entirely on the database
    """
    name = await mostCommonName(limit, name_type)
    if name is None:
        return {"message": "result not found"}
    else:
        print(f"name is {name}")
        return name

@app.get("/api/v1/identity_request_no/{request_no}")
@limiter.limit("5/minute")
async def query_identity_request_no(request_no: str, request: Request):
    """
    To get identity information by request_no
        :param request_no: request_no - str
    """
    identity = await queryByRequestNo(request_no)
    if identity is None:
        return {"message": "Identity not found"}
    else:
        print(f"identity is {identity}")
        return identity

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)