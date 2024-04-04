from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from bcrypt import hashpw
from faunadb import query as q
from faunadb.client import FaunaClient

app = Starlette()

# Initialize FaunaDB client
client = FaunaClient(secret="YOUR_FAUNADB_SECRET_KEY")


async def register_user(request):
    data = await request.json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # Hash the password
    hashed_password = hashpw(password, salt=10)

    # Save user data to FaunaDB
    try:
        result = client.query(
            q.create(
                q.collection("users"),
                {
                    "data": {
                        "username": username,
                        "email": email,
                        "password": hashed_password
                    }
                }
            )
        )
        return JSONResponse({"message": "User registered successfully"})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

# Register the endpoint
app.add_route("/register", register_user, methods=["POST"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
