import uvicorn, routes, os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from cases import database as db
from cases.utils import render_template
from objects import settings
from cases.logger import log, err, Colors

app = FastAPI()

# mount static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# routers
app.include_router(routes.router)

# init services
@app.on_event("startup")
async def init_startup():
    try:
        await db.init_pool()
        log("Database initialized.", Colors.LIGHT_GREEN)
    except Exception as e:
        err(f"Database initialization failed: {e}", Colors.LIGHT_RED)
        os._exit(0)
        
    log("Startup complete.", Colors.GRAY)
    
# dispose of services
@app.on_event("shutdown")
async def finish_shutdown():
    if db.conn.is_connected:
        await db.close_pool()
        log(f"Database closed.", Colors.GRAY)

@app.exception_handler(404)
async def not_found_page(request : Request, error):
    return render_template("404.html", request)

def main():
    uvicorn.run(
        app,
        host = "0.0.0.0",
        port = 8000,
        server_header = False,
        date_header = False,
        headers = (
            ("server-version", settings.APP_VERSION),
        )
    )
    
if __name__ == "__main__":
    main()