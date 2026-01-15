from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os

app = FastAPI(title="Titan Fatura API")

# Orkestra Canlı Servis Adresi
ORKESTRA_URL = "https://efaturacim.orkestra.com.tr/servis.php"

class SorguModel(BaseModel):
    vkn_tckn: str
    baslangic: str = "2026-01-01"
    bitis: str = "2026-01-16"
    kullanici_adi: str
    sifre: str

@app.get("/")
def home():
    return {"durum": "API Aktif", "mesaj": "Titan Fatura Sistemi Mermi Gibi!"}

@app.post("/sorgula")
async def fatura_sorgula(data: SorguModel):
    # PHP'deki faturaSorgula metodunun Python isteğine çevrilmiş hali
    payload = {
        "action": "faturaSorgula",
        "user": data.kullanici_adi,
        "pass": data.sifre,
        "baslangic": data.baslangic,
        "bitis": data.bitis,
        "vkn": data.vkn_tckn,
        "tip": "hepsi"
    }
    
    try:
        # Orkestra sunucusuna veri gönderiyoruz
        response = requests.post(ORKESTRA_URL, data=payload, timeout=20)
        
        if response.status_code == 200:
            return {"durum": "basarili", "sonuc": response.text}
        else:
            raise HTTPException(status_code=response.status_code, detail="Sunucu hata verdi.")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
