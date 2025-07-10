from fastapi import FastAPI, Header, HTTPException
from app.auth import verify_apikey, generate_jwt
from app.models import Payload
from fastapi.responses import JSONResponse, PlainTextResponse


API_KEY = "2f5ae96c-b558-4c7b-a590-a501ae1c3f6c"


app = FastAPI()


@app.post("/DevOps")
async def devops_endpoint(
    payload: Payload,
    x_parse_rest_api_key: str = Header(...),
    x_jwt_kwy: str = Header(None)
):
    if not verify_apikey(x_parse_rest_api_key, API_KEY):
        raise HTTPException(status_code=403, detail="Invalid API Key")

    jwt_token = generate_jwt(payload.dict())

    return JSONResponse(
        content={
            "message": f"Hello {payload.to} your message will be send",
            "jwt": jwt_token
        }
    )


@app.api_route("/DevOps", methods=["GET", "PUT", "DELETE", "PATCH"])
async def invalid_method():
    return PlainTextResponse(content="ERROR", status_code=405)
