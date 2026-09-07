# FastAPI Learning Journey 🚀

A day-by-day log of learning [FastAPI](https://fastapi.tiangolo.com/), from basic routing all the way to serving a machine learning model through a clean, modular API. Each `Day X` folder is a self-contained mini-project building on the concepts from the day before.

## 📅 Day-by-Day Breakdown

### Day 1 — First Steps with FastAPI
The very basics: creating a `FastAPI()` app and serving static HTML pages.
- `GET /` → serves `index.html`
- `GET /about` → serves `about.html`
- **Concepts:** `FastAPI`, `FileResponse`, basic routing

### Day 2 — Building a Patient Records API
A read-only API for managing patient records stored in `patients.json`.
- `GET /` — welcome message
- `GET /about` — API description
- `GET /view` — view all patient records
- `GET /patient/{patient_id}` — fetch a single patient by ID
- `GET /sort` — sort patients by height, weight, or BMI (asc/desc)
- **Concepts:** `Path`, `Query`, `HTTPException`, JSON file I/O

### Day 3 — Data Validation with Pydantic
Standalone practice script (no API endpoints) exploring advanced Pydantic features.
- Nested models (`Address` inside `Patient`)
- Field constraints via `Annotated` + `Field`
- `EmailStr` and `AnyUrl` validated types
- Custom `@field_validator` (e.g. restricting email domains)
- Cross-field `@model_validator`
- `@computed_field` (auto-calculated BMI)
- **Concepts:** `pydantic`, nested models, validators, computed fields

### Day 4 — Adding Create (POST) Support
Extends Day 2's API into a proper `Patient` model with validation, plus the ability to add new records.
- All Day 2 endpoints, now backed by a Pydantic `Patient` model
- `POST /create` — add a new patient record
- Auto-computed `bmi` and `verdict` (Underweight/Normal/Obese) fields
- **Concepts:** Pydantic models as request bodies, `computed_field`, `JSONResponse`

### Day 5 — Full CRUD API
Completes the patient records API with update and delete support.
- All Day 4 endpoints
- `PUT /edit/{patient_id}` — partially update a patient (via an `UpdatePatient` model with optional fields)
- `DELETE /delete/{patient_id}` — remove a patient record
- **Concepts:** partial updates with `exclude_unset=True`, full CRUD lifecycle

### Day 6 — Serving a Machine Learning Model
Pivots from CRUD to ML: wraps a trained model (`model.pkl`) in a FastAPI endpoint, plus a Streamlit frontend to interact with it.
- `POST /pridict` — predicts an **insurance premium category** from user details
- Engineered features computed on the fly: `bmi`, `lifestyle_risk`, `age_group`, `city_tier`
- `frontend.py` — a Streamlit UI that collects user input and calls the API
- **Concepts:** loading a `pickle` model, `pandas` for inference input, computed fields for feature engineering, connecting a Streamlit frontend to a FastAPI backend

### Day 7 — Refactoring into a Modular Project Structure
Takes the Day 6 ML API and reorganizes it into a clean, production-style layout.
```
Day 7/
├── app.py                     # FastAPI app & routes
├── config/
│   └── city_tier.py           # City tier lookup lists
├── schema/
│   └── user_input.py          # UserInput Pydantic schema
└── model/
    ├── model.pkl              # Trained model
    └── predict_premium.py     # Model loading & prediction logic
```
- `GET /` — welcome message
- `GET /health` — health check (confirms the model loaded)
- `POST /predict` — predicts insurance premium category
- Adds a `field_validator` to normalize city name input
- **Concepts:** separating concerns (schema / config / model / app), code organization for scalable APIs

## 🛠️ Tech Stack
- **FastAPI** — web framework
- **Pydantic** — data validation & settings management
- **Uvicorn** — ASGI server (implied, for running the apps)
- **Pandas** — data handling for model inference (Day 6–7)
- **Scikit-learn** (or similar) — the trained model used in Day 6–7
- **Streamlit** — quick frontend for the ML prediction demo (Day 6)

## ▶️ Running a Day's Project
Each day's project can be run independently. From inside the relevant `Day X` folder:

```bash
pip install fastapi uvicorn pydantic pandas streamlit
uvicorn main:app --reload      # for Day 1, 2, 4, 5 (entry file is main.py)
uvicorn app:app --reload       # for Day 6, 7 (entry file is app.py)
```

Then open **http://127.0.0.1:8000/docs** for the interactive Swagger UI.

For Day 6's Streamlit frontend, run the API first, then in another terminal:
```bash
streamlit run frontend.py
```

## 📌 Notes
- Each folder is independent — install dependencies and run separately.
- `patients.json` files hold sample data used by the CRUD days (2, 4, 5).
- `__pycache__` folders are compiled bytecode and can be safely ignored/deleted.
