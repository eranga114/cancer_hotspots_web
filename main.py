import uvicorn
from fastapi import FastAPI, Request, Body, File, UploadFile, Form
from pydantic import BaseModel
import pickle
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

with open( 'rfc_model_pickle', 'rb' ) as file:
    rf_pickle = pickle.load( file )

templates = Jinja2Templates( directory="templates" )

app = FastAPI()


class Item( BaseModel ):
    startPosition: int
    mut_count: int
    total_mut_count: int


@app.get( '/' )
async def home(request: Request):
    return templates.TemplateResponse( "index.html", {"request": request} )


@app.post( '/submitform' )
async def handle_form(request: Request , startPosition: int = Form( ... ),
                      mut_count: int = Form( ... ),
                      total_mut_count: int = Form( ... ),
                      ):
    prediction = rf_pickle.predict( [[startPosition, mut_count, total_mut_count]] )
    if prediction == 1:
        hotspot = "It's a cancer hotspot"
    else:
        hotspot = "It's not a cancer hotspot"
    print(prediction)
    print(hotspot)
    return templates.TemplateResponse( "index.html", {"request": request, "prediction":prediction, "hotspot":hotspot} )


# @app.post( '/hotspots' )
# async def hotspots_pred(data: Item, request: Request):
#     data = data.dict()
#     startPosition = data['startPosition']
#     mut_count = data['mut_count']
#     total_mut_count = data['total_mut_count']
#
#     prediction = rf_pickle.predict( [[startPosition, mut_count, total_mut_count]] )
#     if prediction == 1:
#         hotspot = "It's a cancer hotspot"
#     else:
#         hotspot = "It's not a cancer hotspot"
#
#     return templates.TemplateResponse("index_2.html", {"request": request, "prediction": prediction, "hotspot": hotspot})


if __name__ == "__main__":
    uvicorn.run( app, host='localhost', port=8888 )
