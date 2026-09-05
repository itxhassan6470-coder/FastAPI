from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json

app = FastAPI()

def load():
    with open("patients.json","r") as f:
        return json.load(f)

def save_data(data):
    with open("patients.json","w") as f:
        json.dump(data,f, indent=4)

class Patient(BaseModel):
    id: Annotated[str, Field(..., description="give patient id", examples=["P001"])]
    name: Annotated[str, Field(..., description="give the name of the patient", max_length=50)]
    city: Annotated[str, Field(..., description="give the name of the city", max_length=50)]
    age: Annotated[int, Field(..., description="enter age of the patient", lt=120, gt=0)]
    gender: Annotated[Literal["male","female","other"], Field(..., description="gender: male, female, other")]
    height: Annotated[float, Field(..., description="height in meters", gt=0)]
    weight: Annotated[float, Field(..., description="weight in kg", gt=0)]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / self.height**2, 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight" # Fixed
        else:
            return "Obese"

class UpdatePatient(BaseModel): # Class names usually start with Capital
    name: Annotated[Optional[str], Field(default=None, max_length=50)]
    city: Annotated[Optional[str], Field(default=None, max_length=50)]
    age: Annotated[Optional[int], Field(default=None, lt=120, gt=0)]
    gender: Annotated[Optional[Literal["male","female","other"]], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]

@app.post("/create") # fixed typo
def create_patient(patient: Patient):
    data_base = load()
    if patient.id in data_base:
        raise HTTPException(status_code=409, detail="patient already exists") # fixed

    # Save full data including bmi and verdict
    patient_dict = patient.model_dump()
    data_base[patient.id] = patient_dict
    save_data(data_base)
    return JSONResponse(status_code=201, content={"message": "patient created successfully"})

@app.get("/")
def hello():
    return {"message": "patient management system"}

@app.get("/about")
def about():
    return {"message": "a fully functional api"}

@app.get("/view")
def view():
    return load()

@app.get("/patient/{patient_id}")
def get_by_patient_id(patient_id: str = Path(..., description="search by patient id", examples=["P001"])): # fixed 'example'
    data = load()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="patient not found")

@app.get("/sort")
def sorted_data(sortby: str = Query(..., description="sort by height, weight, bmi"),
                order: str = Query('asc', description="asc or desc")):
    valid_fields = ["height", "weight", "bmi"]
    if sortby not in valid_fields:
        raise HTTPException(status_code=400, detail=f"invalid field. select from {valid_fields}")
    valid_order = ['asc', 'desc']
    if order not in valid_order:
        raise HTTPException(status_code=400, detail=f"invalid order. select from {valid_order}")

    data = load()
    # Rebuild Patient to get computed bmi
    patients = [Patient(**v) for v in data.values()]
    sorteddata = sorted(patients, key=lambda x: getattr(x, sortby), reverse=(order=='desc'))
    return [p.model_dump() for p in sorteddata] # return with bmi

@app.put("/edit/{patient_id}")
def update_patient(patient_id: str, updated_info: UpdatePatient):
    data = load()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="patient does not exist") # fixed 403 -> 404

    existing_patientdata = data[patient_id]
    updated_info_patient = updated_info.model_dump(exclude_unset=True)

    for key, value in updated_info_patient.items():
        existing_patientdata[key] = value

    # Recalculate bmi and verdict
    updated_patient = Patient(**existing_patientdata)
    data[patient_id] = updated_patient.model_dump()
    save_data(data)

    return JSONResponse(status_code=200, content={"message": "updated data successfully"})

@app.delete('/delete/{patient_id}') # Fixed indentation
def delete_patient(patient_id: str):
    data = load()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')

    del data[patient_id]
    save_data(data)

    return JSONResponse(status_code=200, content={'message': 'patient deleted'})