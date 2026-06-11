# 🔧 FIXES & BACKEND CHANGES REQUIRED

## ✅ Frontend Fixes Completed

### 1. Navigation Buttons Fixed
- ✅ "Back to Login" button on signup step 1 now works properly
- ✅ "Go to Login" button on signup success now works properly  
- ✅ Both buttons use Streamlit's `st.switch_page()` for reliable navigation

### 2. Logout Button
- ✅ Already exists in sidebar on all pages (except login/signup)
- ✅ Visible once user is logged in
- ✅ Clears all session data and returns to login page

---

## 🚨 BACKEND CHANGES NEEDED

The frontend is calling endpoints that **don't exist** on your backend. You have two options:

### **OPTION A: Create Alias Endpoints (Recommended - Minimal Changes)**

Add these endpoint aliases to your backend routers:

#### **File: routers/prediction.py**
Add this endpoint (keep the existing `/raw` endpoint):
```python
@router.post("/")  # NEW - This will handle POST /predict
async def predict_wrapper(item: schema.StudentDetails, db: Session = Depends(get_db), 
                          clf = Depends(get_model), preproc = Depends(get_preprocessor),
                          current_user: schema.UserExtended = Depends(oauth2.get_current_user)):
    # Just call your existing predict() function
    return await predict(item, db, clf, preproc, current_user)
```

#### **File: routers/records.py**
Add these endpoint aliases (keep the existing ones):
```python
# NEW endpoint - GET /records (returns all students like /records/get_all_records)
@router.get("/")
async def get_all_records_wrapper(db: Session = Depends(get_db), 
                                  current_user: schema.UserExtended = Depends(oauth2.get_current_user)):
    return await get_students(db, current_user)

# Note: The existing /records/get_all_records still works, but /records also works now
# Note: The existing /records/student/{student_id} already exists - NO CHANGE NEEDED
# Note: The existing /records/student/{student_id}/shap already exists - NO CHANGE NEEDED
```

---

### **OPTION B: Rename Router Prefixes (Maximum Impact)**

In **main.py**, modify how routers are included:

```python
# BEFORE (current):
app.include_router(prediction.router)           # Prefix: /predict
app.include_router(records.router)              # Prefix: /records

# AFTER (what frontend expects):
app.include_router(prediction.router, prefix="/predict")    # Keep as is, but check prefix
app.include_router(records.router, prefix="/records")       # Keep as is, but check prefix
```

Wait - actually checking your main.py, the prefixes are already defined in the router classes themselves:
- `prediction.router` has `prefix="/predict"`
- `records.router` has `prefix="/records"`

So the endpoints ARE:
- `/predict/raw` ✓ (exists)
- `/records/get_all_records` ✓ (exists)
- `/records/student/{student_id}` ✓ (exists)
- `/records/student/{student_id}/shap` ✓ (exists)

But the frontend is calling:
- `/predict` ✗ (doesn't exist - should be `/predict/raw`)
- `/students` ✗ (doesn't exist - should be `/records/get_all_records`)
- `/students/{student_id}` ✗ (doesn't exist - should be `/records/student/{student_id}`)
- `/students/{student_id}/shap` ✗ (doesn't exist - should be `/records/student/{student_id}/shap`)

---

## 📝 ENDPOINT MAPPING

| Frontend Calls | Backend Should Provide | Current Status | Fix |
|---|---|---|---|
| `POST /predict` | `POST /predict/raw` | ❌ Missing | Add alias `/predict` → calls `/predict/raw` |
| `GET /students` | `GET /records/get_all_records` | ❌ Missing | Add alias `/records` → calls `/get_all_records` |
| `GET /students/{id}` | `GET /records/student/{id}` | ❌ Missing | Add alias `/records/{id}` → calls `/records/student/{id}` |
| `DELETE /students/{id}` | `DELETE /records/student/{id}` | ❌ Missing | Add alias `/records/{id}` → calls `/records/student/{id}` |
| `GET /students/{id}/shap` | `GET /records/student/{id}/shap` | ✓ EXISTS | Already there! |

---

## 🎯 QUICKEST FIX

Add these two endpoint aliases to your router files:

**routers/prediction.py** (after the existing `/raw` endpoint):
```python
@router.post("")
async def predict_default(item: schema.StudentDetails, db: Session = Depends(get_db), 
                          clf = Depends(get_model), preproc = Depends(get_preprocessor),
                          current_user: schema.UserExtended = Depends(oauth2.get_current_user)):
    return await predict(item, db, clf, preproc, current_user)
```

**routers/records.py** (after the existing `/get_all_records` endpoint):
```python
@router.get("")
async def get_all_records_default(db: Session = Depends(get_db), 
                                  current_user: schema.UserExtended = Depends(oauth2.get_current_user)):
    return await get_students(db, current_user)

@router.get("/{student_id}")
async def get_one_student_default(student_id: str, response: Response, db: Session = Depends(get_db),
                                  current_user: schema.UserExtended = Depends(oauth2.get_current_user)):
    return get_student(student_id, response, db, current_user)
```

This way:
- Frontend calls `/predict` which maps to your POST `/predict` endpoint
- Frontend calls `/students` which maps to your GET `/records` endpoint  
- Frontend calls `/students/{id}` which maps to your GET `/records/{student_id}` endpoint
- All existing endpoints still work

---

## 📋 Testing Checklist After Backend Changes

- [ ] Student can create account
- [ ] Student can login
- [ ] Student clicks "My Record" and data loads ✓
- [ ] Student clicks "My Analysis" and SHAP chart appears ✓
- [ ] Teacher can create account
- [ ] Teacher can login
- [ ] Teacher clicks "Make Prediction", fills form, gets result ✓
- [ ] Teacher clicks "Student Records", sees list of students ✓
- [ ] Teacher clicks "SHAP Analysis", enters student ID, gets chart ✓
- [ ] Logout button works on all pages ✓
- [ ] Navigation buttons work (signup ↔ login) ✓

---

## 💡 Note

The existing `/records/student/{id}/shap` endpoint is already correct, so SHAP analysis might already work once the other endpoints are fixed!
