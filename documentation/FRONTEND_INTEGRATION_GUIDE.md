# ScholarSight Frontend Integration Guide

## Overview
The frontend has been fully integrated with the FastAPI backend using OAuth2 JWT authentication. All pages are now equipped with proper role-based access control and JWT token management.

## Authentication System

### Login Flow
```
User enters: Institution ID + Email + Password
    ↓
POST /auth/login with OAuth2PasswordRequestForm (username=email, password)
    ↓
Backend returns: {access_token, token_type}
    ↓
Frontend stores: {email, institution_id, access_token, token_type}
    ↓
Role determined from institution_id prefix (STU=student, TEA=teacher)
    ↓
Redirect to Dashboard
```

### Signup Flow
```
Step 1: User enters Institution ID
    ↓
POST /user/verify-role?institution_id=... 
    ↓
Backend returns: {token, message}
    ↓
Role extracted from message (Verified as student/teacher)
    ↓
Step 2: User fills signup form (firstname, lastname, email, password)
    ↓
POST /user/signup with X-Verify-Token header + JSON body
    ↓
Account created
    ↓
Redirect to Login page
```

## Session State Structure
```python
st.session_state["user"] = {
    "email": "user@institution.com",           # User's login email
    "institution_id": "STU001234",             # Institutional identifier
    "access_token": "eyJhbGciOiJIUzI1NiIs...", # JWT token for API calls
    "token_type": "bearer"                     # Always "bearer"
}
```

## Role Determination
Role is automatically determined from the institution_id prefix:
- **STU*** (e.g., STU001, STU12345) → `role = "student"`
- **TEA*** (e.g., TEA001, TEA99) → `role = "teacher"`

This is handled by the `get_role()` function in utils.py.

## API Authentication
All API calls to the backend include the JWT token in the Authorization header:
```
Authorization: Bearer {access_token}
```

This is handled by the `_get_auth_headers()` function which is used by all API wrappers:
- `api_predict()`
- `api_get_student()`
- `api_get_all_students()`
- `api_delete_student()`
- `api_get_shap_chart()`

## Page Access Control

### Teacher-Only Pages
Require `require_teacher()` at the top:
- **pages/predict.py** - Make predictions
- **pages/records.py** - View student records
- **pages/analysis.py** - SHAP analysis

Access: Only users with institution_id starting with "TEA"

### Student-Only Pages
Require `require_student()` at the top:
- **pages/my_record.py** - View own academic record
- **pages/my_analysis.py** - View own SHAP analysis

Access: Only users with institution_id starting with "STU"

### Shared Pages
- **pages/dashboard.py** - Shows different content based on role
  - Teachers: See student statistics and management tools
  - Students: See personal prediction and analysis options

## Testing Instructions

### Prerequisites
1. FastAPI backend running on `http://127.0.0.1:8000`
2. Database populated with test users (see backend setup)
3. Streamlit frontend running

### Test Scenario 1: Student Signup & Login

```bash
# Terminal 1: Start FastAPI backend
cd /path/to/Student-Performance-Predictor
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000

# Terminal 2: Start Streamlit frontend
cd /path/to/Student-Performance-Predictor/frontend
streamlit run app.py
```

1. **Sign Up as Student:**
   - Click "Create one here" link on login page
   - Enter Institution ID: `STU001001`
   - Click "Verify & Continue"
   - Fill in: First Name, Last Name, Email, Password
   - Click "Create Account"
   - Click "Go to Login"

2. **Login as Student:**
   - Enter Institution ID: `STU001001`
   - Enter Email: (the one you just created)
   - Enter Password: (the one you created)
   - Click "Sign In"
   - **Expected**: Redirect to dashboard with "Student" role
   - **Navigation**: Only see "My Record" and "My Analysis" in sidebar

### Test Scenario 2: Teacher Signup & Login

1. **Sign Up as Teacher:**
   - Go to signup page
   - Enter Institution ID: `TEA001001`
   - Click "Verify & Continue"
   - Fill in: First Name, Last Name, Email, Password
   - Click "Create Account"
   - Click "Go to Login"

2. **Login as Teacher:**
   - Enter Institution ID: `TEA001001`
   - Enter Email: (the one you just created)
   - Enter Password: (the one you created)
   - Click "Sign In"
   - **Expected**: Redirect to dashboard with "Teacher" role
   - **Navigation**: See "Make Prediction", "Student Records", "SHAP Analysis" in sidebar

### Test Scenario 3: Access Control Verification

1. **As Logged-In Student:**
   - Try accessing `/pages/predict.py` directly
   - **Expected**: Error message "Access denied. Teachers only." + stop

2. **As Logged-In Teacher:**
   - Try accessing `/pages/my_record.py` directly
   - **Expected**: Error message "Access denied. Students only." + stop

### Test Scenario 4: API Authentication

1. **Make a Prediction (Teacher):**
   - Login as teacher
   - Click "Make Prediction"
   - Fill in student data
   - Click "Generate Prediction"
   - **Expected**: Prediction returned with "PASS" or "FAIL"
   - **Backend**: JWT token is verified in the request

2. **View Student Records (Teacher):**
   - Click "Student Records"
   - **Expected**: Table of all student records loads successfully
   - **Backend**: JWT token allows access to /students endpoint

3. **View Own Record (Student):**
   - Login as student
   - Click "My Record"
   - **Expected**: Your student record displays
   - **Backend**: Uses institution_id for lookup with JWT auth

## Troubleshooting

### Issue: "Cannot reach the backend server"
- Check if FastAPI is running on port 8000
- Verify no firewall blocks `127.0.0.1:8000`
- Check backend logs for errors

### Issue: "Invalid credentials" on login
- Verify institution_id is correct (STU* or TEA*)
- Check email and password match what was registered
- Ensure database contains the user record

### Issue: "Access denied" messages on pages
- Check institution_id prefix (must match role requirement)
- Verify user is logged in (check session state in Streamlit)
- Clear browser cache and re-login

### Issue: JWT token expired
- Currently not implemented (tokens don't expire in basic setup)
- For production, implement token refresh mechanism
- See token.py in backend for ACCESS_TOKEN_EXPIRE_MINUTES

## File Changes Summary

### New/Modified Files:
- `frontend/app.py` - Added institution_id input to login
- `frontend/utils.py` - Added JWT authentication and role detection
- `frontend/pages/dashboard.py` - Role-based content (no changes needed)
- All other pages - Already use require_teacher() or require_student()

### Key Functions:
- `get_role()` - Returns role based on institution_id prefix
- `get_access_token()` - Returns JWT token from session
- `require_login()` - Redirects to login if not authenticated
- `require_teacher()` - Restricts page to teachers only
- `require_student()` - Restricts page to students only
- `_get_auth_headers()` - Adds Authorization header to API calls

## Security Notes

1. **JWT Token Storage**: Stored in `st.session_state` (Streamlit's session storage)
   - Safe for local testing
   - For production, use secure storage mechanisms

2. **HTTPS**: Currently using HTTP
   - Use HTTPS in production
   - Set secure cookies for token storage

3. **CORS**: Backend allows all origins (`allow_origins=["*"]`)
   - Restrict to frontend domain in production

4. **Token Expiration**: Not currently implemented
   - Implement token refresh for production
   - See backend `token.py` for configuration

## Next Steps

1. **Testing**: Run through all test scenarios above
2. **Logging**: Add comprehensive logging for debugging
3. **Error Handling**: Enhance error messages for users
4. **Password Reset**: Implement forgot password flow
5. **Email Verification**: Add email confirmation on signup
6. **Token Refresh**: Implement JWT refresh tokens
7. **Rate Limiting**: Add rate limiting to prevent brute force
8. **Deployment**: Deploy frontend to production server

## Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [FastAPI OAuth2 Documentation](https://fastapi.tiangolo.com/tutorial/security/)
- [JWT (JSON Web Tokens)](https://jwt.io/)
- [ScholarSight Backend Guide](./INTEGRATION_GUIDE.md)
