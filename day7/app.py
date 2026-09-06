from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema.user_input import UserInput
from model.predict_premium import predict_premium , model




app=FastAPI()
@app.get("/home")
def home():
    return {"message":"premium prediction fast api"}


@app.get("/helth")
def helth():
    {
        "status":"OK",
        "model": model is not None
    }

@app.post("/pridict")
def predict_premium_(data: UserInput):

    input = {
        "bmi": data.bmi,
        "age_group": data.age_group,
        "lifestyle_risk": data.lifestyle_risk,
        "city_tier": data.city_tier,
        "income_lpa": data.income_lpa,
        "occupation": data.occupation
    }
    prediction = predict_premium(input)
    return JSONResponse(
        status_code=200,
        content={"predicted_category": prediction}
    )
