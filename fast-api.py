from fastapi import FastAPI

app = FastAPI()

@app.post("/trade/")
def trade_signal(ticker: str):
    # Fetch live data and make predictions
    prediction = model.predict([latest_data])
    return {"ticker": ticker, "signal": "BUY" if prediction == 1 else "SELL"}
