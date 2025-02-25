from uvicorn import run

if __name__ == "__main__":
    run(
        app="api.app:get_application",
        host="0.0.0.0",
        port=8000,
        http="httptools",
        loop="uvloop",
        interface="asgi3",
        factory=True,
        reload=True,
    )
