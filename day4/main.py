from fastapi import FastAPI
from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json
from pydantic import BaseModel,Field
from typing import Annotated,Literal
from fastapi.responses import JSONResponse

app = FastAPI()

def load():
    with open("patients.json","r") as f:
        data= json.load(f)
        return data

def save_data(data):
    with open("patients.json","w") as f:
        json.dump(data,f)


class Patient(BaseModel):
    id:Annotated[str,Field(...,description="give patient id",examples=["POO1"])]
    name:Annotated[str,Field(...,description="gve the name of the patient", max_length= 50)]
    city:Annotated[str,Field(...,description="give the name of the city ",max_length=50)]
    age:Annotated[int,Field(...,description="enter age of the patient should not in -",lt=100,gt=0)]
    gender:Annotated[Literal["male","female","other"],Field(...,description="give the gender of the patient male,female,other")]
    height:Annotated[float,Field(...,description="enter the hight of the patient in meters ",gt=0)]
    weight:Annotated[float,Field(...,description="give the weight of the patient in kg",gt=0)]
    @computed_field
    @property
    def bmi(self)-> float:
        bmi=round((self.weight/self.height**2),2)
        return bmi

    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Normal'
        else:
            return 'Obese'







@app.post("/creat")
def creat_patient(patient:Patient):
    data_base=load()
    if patient.id in data_base:
        raise HTTPException(status_code=404,detail="patient already exit")
    data_base[patient.id] = patient.model_dump(exclude= ["id"])
    save_data(data_base)
    return JSONResponse(status_code=201,content={"message":"patient created sucessfully"})




@app.get("/")
def hello():
    return {"message":"patient management system"}



@app.get("/about")
def about():
    return {"message":"a fully functonal api "}




@app.get("/view")
def view():
    data=load()
    return data



@app.get("/patient/{patient_id}")
def get_by_patient_id(patient_id :str =Path(...,description="serch by patient id",example="P001")):
    data = load()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404,detail="patient not found")




@app.get("/sort")
def sorted_data(sortby :str = Query(...,description="sort on the basis of height weight and bmi"), order :str =Query('asc',description="accending and desending order ")):
    valid_fields=["height","weight","bmi"]
    if sortby not in valid_fields:
        raise HTTPException(status_code=400,detail=f"invalid field seleted,select from {valid_fields}")
    valid_order=['asc','desc']
    if order not in valid_order:
        raise HTTPException(status_code=400,detail=f"the order is invalid select from {valid_order}")

    sort_order = True if order=='desc' else False


    data = load()
    sorteddata=sorted(data.values()
                      ,key=lambda x: x.get(sortby,0)
                      ,reverse=sort_order)
    return sorteddata 


