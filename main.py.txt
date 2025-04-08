from fastapi import FastAPI, Query
from pytrends.request import TrendReq
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/trends")
def get_trends(keyword: str = Query(...)):
    pytrends = TrendReq(hl='es-ES', tz=360)
    pytrends.build_payload([keyword], timeframe='today 12-m')
    data = pytrends.interest_over_time()
    if data.empty:
        return {"message": f"No se encontraron datos para: {keyword}"}
    last_month = data.tail(30).reset_index().to_dict(orient="records")
    return {"keyword": keyword, "data": last_month}
