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
    try:
        pytrends = TrendReq(hl='es-ES', tz=360)
        pytrends.build_payload([keyword], timeframe='today 12-m')
        data = pytrends.interest_over_time()
        if data.empty:
            return {"message": f"No se encontraron datos para: {keyword}"}
        
        # Eliminar columna 'isPartial' si existe
        if 'isPartial' in data.columns:
            data = data.drop(columns=['isPartial'])
        
        # Convertimos a formato amigable para JSON
        datos = [
            {
                "date": str(row[0].date()),
                "value": int(row[1][0])
            } for row in data.iterrows()
        ]
        return {"keyword": keyword, "data": datos}
    
    except Exception as e:
        return {"error": str(e)}
