from pydantic import BaseModel,Field, EmailStr, AnyUrl, field_validator, model_validator, computed_field
from typing import Annotated, Optional, List, Dict

# nested_models, field_validator, model_validator, computed_fields, serialization
class Address(BaseModel):
    province:str
    city:str
    postal_code:str


class Patient(BaseModel):

    name: Annotated[str, Field(max_length=50, description="Maximum lenght of patient name should be of 50 characters.")]
    age: Annotated[int, Field(gt=0, lt=80, description="Pateint should be greater than 0 and less than 80.")]
    email: EmailStr
    linkedin: AnyUrl
    weight: Annotated[float, Field(gt=0, description="Give the weight of pateint in kg.")]
    height: Annotated[float, Field(gt=0, description="Give the height of patient in m.")]
    allergies: Annotated[Optional[List[str]], Field(default=None, description="List the allergies of the patient but not more than 5", max_length=5)]
    contact_info: Annotated[Dict[str, str], Field(description="Give the contact information of patient in key value pairs", examples=[{"emergency_number": "934830948"}, {"contact_num": "5348593"}])]
    address:Address

    @field_validator("email")
    @classmethod
    def email_validator(cls, value):
        validate_domains = ["ubl.com", "hbl.com", "yaki.com"]
        domain_name = value.split('@')[-1]
        if domain_name not in validate_domains:
            raise ValueError("invalid domain")
        return value

    @model_validator(mode="after")
    def model_validation(cls, model):
        if model.age > 60 and "emergency" not in model.contact_info:
            raise ValueError("Emergency required for 60+ old patient.")
        return model
    @computed_field
    @property
    def bmi(self)->float:
        bmi=round((self.weight/self.height**2),2)
        return bmi



def insert_patient(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.email)
    print(patient.linkedin)
    print(patient.weight)
    print(patient.height)
    print(patient.allergies)
    print(patient.contact_info)
    print("bmi",patient.bmi)
    print(patient.address)
    print("Inserted")

address_info={"province":"punjab","city":"sargodha","postal_code":"40100"}
address1=Address(**address_info)
patient_info = {'name': "Hassan", 'age': 12, 'email': "abc@ubl.com", 'linkedin': "https://www.linkedin.com/in/muhammad-hamza-b8834b428", 'weight': 56, 'height': 1.79, 'allergies': ["dust","pollen","Bull shit"], 'contact_info': {'phone': "87787979"},"address":address1}

patient1 = Patient(**patient_info)

insert_patient(patient1)