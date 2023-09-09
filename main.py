from fastapi import FastAPI
from fastapi.responses import JSONResponse

from scrappers import *

app = FastAPI()

websites = ["myntra"]


@app.post("/scrapper")
async def create_request(label=None, max_pages: int = 15, request_id: str = None, website: str = None):
    if label is None:
        return JSONResponse(content={"Error": "Missing Parameter : label"}, status_code=400)
    if request_id is None:
        return JSONResponse(content={"Error": "Missing Parameter : request_id"}, status_code=400)
    if website is None:
        return JSONResponse(content={"Error": "Missing Parameter : website"}, status_code=400)

    if request_id in scrapper_data:
        return JSONResponse(content={"Error": "Request ID Already Exists"}, status_code=409)

    if website.lower in websites:
        request_id = start_scrapp(label, max_pages, request_id, website)
        content = {"request_id": request_id,
                   "status_url": f"scrapper/{request_id}/status",
                   "data_url": f"scrapper/{request_id}/data"
                   }
        return JSONResponse(content=content, status_code=201)
    else:
        content = {
            "error ": f"website scrapper not available",
            "available_websites": websites
        }

        return JSONResponse(content=content, status_code=400)


@app.get("/scrapper/{request_id}/status")
async def get_satus(request_id):
    if request_id in scrapper_data:
        thread = scrapper_data[request_id]['thread']
        content = {"status": "processing",
                   'label': scrapper_data[request_id]['label'],
                   'scraped_pages': scrapper_data[request_id]['scraped_pages'],
                   'scrapping_page': scrapper_data[request_id]['scrapping_page'],
                   'max_pages': scrapper_data[request_id]['max_pages']
                   }
        if thread.is_alive():
            content["status"] = "processing"

        else:
            content["status"] = "completed"
        return JSONResponse(content=content, status_code=200)
    else:
        content = {"Error": "Request ID : Does not exist"}
        return JSONResponse(content=content, status_code=404)


@app.get("/scrapper/{request_id}/data")
async def get_data(request_id, page: int = 1):
    page_length = 50
    if request_id in scrapper_data:
        full_data = scrapper_data[request_id]['data']
        data_points = len(full_data)
        total_pages = (data_points // page_length) + (1 if data_points % page_length != 0 else 0)
        if page < 1 or page > total_pages:
            content = {"Error": "Wrong Page Number Entered"}
            return JSONResponse(content=content, status_code=404)
        page_data = full_data[page_length * (page - 1):page_length * page]
        content = {
            'request_id': request_id,
            'website': scrapper_data[request_id]['website'],
            'label': scrapper_data[request_id]['label'],
            'current_page': page,
            'total_pages': total_pages if total_pages != 0 else 1,
            'data': page_data,

        }
        return JSONResponse(content=content, status_code=200)
    else:
        content = {"Error": "Request ID : Does not exist"}
        return JSONResponse(content=content, status_code=404)

@app.post("/scrapper/product")
async def create_request( website: str = None,url=None,):
    if url is None:
        return JSONResponse(content={"Error": "Missing Parameter : url"}, status_code=400)
    if website is None:
        return JSONResponse(content={"Error": "Missing Parameter : website"}, status_code=400)

    if website.lower() in websites:
        data = start_single_page_scrapper(website,url)
        if data is None:
            return JSONResponse(content={"Error": "Wrong url, Product not found"}, status_code=404)
        return JSONResponse(content=data, status_code=200)
    else:
        content = {
            "error ": f"""website "{website}" scrapper not available""",
            "available_websites": websites
        }

        return JSONResponse(content=content, status_code=400)