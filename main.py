from fastapi import FastAPI
from fastapi.responses import JSONResponse

from scrappers import *
import requests
import json

app = FastAPI(title="Webscrapper")

websites = ["myntra"]


@app.post("/scrapper")
async def create_request(label=None, max_pages: int = 15, request_id: str = None, website: str = None):
    """
    An endpoint to start scrapping of any website
    """
    if label is None:
        return JSONResponse(content={"Error": "Missing Parameter : label"}, status_code=400)
    if request_id is None:
        return JSONResponse(content={"Error": "Missing Parameter : request_id"}, status_code=400)
    if website is None:
        return JSONResponse(content={"Error": "Missing Parameter : website"}, status_code=400)

    if request_id in scrapper_data:
        return JSONResponse(content={"Error": "Request ID Already Exists"}, status_code=409)

    if website.lower() in websites:
        start_scrapp(label, max_pages, request_id, website)
        content = {"request_id": request_id,
                   "label": label,
                   "website": website,
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
    """
    An End-point to see the status of request
    """
    if request_id in scrapper_data:

        content = {'status': 'completed',
                   'request_id': request_id,
                   'label': scrapper_data[request_id]['label'],
                   'website': scrapper_data[request_id]['website'],
                   'scraped_pages': scrapper_data[request_id]['scraped_pages'],
                   'scrapping_page': scrapper_data[request_id]['scrapping_page'],
                   'max_pages': scrapper_data[request_id]['max_pages']
                   }
        if request_id in threads:
            thread = threads[request_id]
            if thread.is_alive():
                content["status"] = "processing"

        return JSONResponse(content=content, status_code=200)


    else:
        content = {"Error": "Request ID : Does not exist"}
        return JSONResponse(content=content, status_code=404)


@app.get("/scrapper/{request_id}/data")
async def get_data(request_id, page: int = 1):
    """
    An End-point to see the data of request
    """
    page_length = 10
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

@app.get("/scrapper/{request_id}/senddata")
async def get_data(request_id, page: int = 1):
    """
    An End-point to see the data of request
    """
    #print("a")
    page_length = 10
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
        json_content = json.dumps(content)
        #print(json_content)
        #print("m")
        try:
            #url=f"https://jholashop.com/scrappy-data?data={json_content}"
            url = f"https://jholashop.com/scrappy-data"
            status = requests.post(url,json=content).status_code
            print(status)
        except Exception as e:
            print(e)
        return JSONResponse(content=content, status_code=200)
    else:
        content = {"Error": "Request ID : Does not exist"}
        return JSONResponse(content=content, status_code=404)


@app.get("/scrapper/product")
async def get_single_product_data(website: str = None, url=None, ):
    """
    An End-point to get data of a single product
    """
    if url is None:
        return JSONResponse(content={"Error": "Missing Parameter : url"}, status_code=400)
    if website is None:
        return JSONResponse(content={"Error": "Missing Parameter : website"}, status_code=400)

    if website.lower() in websites:
        data = start_single_page_scrapper(website, url)
        if data is None:
            return JSONResponse(content={"Error": "Wrong url, Product not found"}, status_code=404)
        return JSONResponse(content=data, status_code=200)
    else:
        content = {
            "error ": f"""website "{website}" scrapper not available""",
            "available_websites": websites
        }

        return JSONResponse(content=content, status_code=400)

# @app.get("/scrapper/{request_id}/send_mail")
# async def send_data(request_id, page: int = 1):
#     """
#     An End-point to mail data in batch\n It's just for example do not call this method
#     """
#     page_length = 50
#     if request_id in scrapper_data:
#         full_data = scrapper_data[request_id]['data']
#         data_points = len(full_data)
#         total_pages = (data_points // page_length) + (1 if data_points % page_length != 0 else 0)
#         if page < 1 or page > total_pages:
#             content = {"Error": "Wrong Page Number Entered"}
#             return JSONResponse(content=content, status_code=404)
#         page_data = full_data[page_length * (page - 1):page_length * page]
#         content = {
#             'request_id': request_id,
#             'website': scrapper_data[request_id]['website'],
#             'label': scrapper_data[request_id]['label'],
#             'current_page': page,
#             'total_pages': total_pages if total_pages != 0 else 1,
#             'data': page_data,
#         }
#
#         mail(content)
#     else:
#         content = {"Error": "Request ID : Does not exist"}
#         return JSONResponse(content=content, status_code=404)


@app.get("/scrapper/receive")
async def send_data(data={}):
    # Specify the file path
    file_path = 'your_file.txt'  # Replace 'your_file.txt' with the actual file path

    try:
        # Open the file in read mode
        with open(file_path, 'r') as file:
            # Read the contents of the file
            file_contents = file.read()

            # Print the contents
            print(file_contents)
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    print(len(data))
    return JSONResponse({"status":"received"},status_code=200)