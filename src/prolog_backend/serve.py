from prolog_backend.config.server import server_settings

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "prolog_backend.app:app", host=server_settings.HOST, port=server_settings.PORT, reload=server_settings.RELOAD
    )
