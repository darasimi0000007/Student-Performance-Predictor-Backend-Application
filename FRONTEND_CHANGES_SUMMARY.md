# Frontend Integration Changes - Quick Reference

## What Changed

### 1. Login Page (frontend/app.py)
**Before**: Email + Password only
**After**: Institution ID + Email + Password
**Storage**: email, institution_id, access_token, token_type

### 2. Authentication System (frontend/utils.py)
**New Functions**:
- `get_access_token()` - Retrieve JWT token
- `get_role()` - Determine role from institution_id (STU/TEA prefix)
- `_get_auth_headers()` - Add Authorization header to requests
- `require_teacher()` - Enforce teacher-only access
- `require_student()` - Enforce student-only access

**Updated Functions**:
- All `api_*()` functions now include JWT token in headers

### 3. API Authentication
**All API calls now include**:
```
Authorization: Bearer {jwt_token}
```

## Migration Guide (For Backend Calls)

### Old Code
```python
response = requests.get(f"{API_BASE}/students", timeout=10)
```

### New Code
```python
headers = _get_auth_headers()
response = requests.get(f"{API_BASE}/students", headers=headers, timeout=10)
```

## Role Assignment
```
Institution ID | Role    | Access
STU*           | Student | My Record, My Analysis
TEA*           | Teacher | Make Prediction, Records, SHAP Analysis
```

## Session State
```python
st.session_state["user"] = {
    "email": "user@institution.com",
    "institution_id": "STU001234",
    "access_token": "jwt_token_here",
    "token_type": "bearer"
}
```

## Testing Checklist
- [ ] Can signup as student (STU prefix)
- [ ] Can signup as teacher (TEA prefix)
- [ ] Can login with email + password
- [ ] Institution ID loads in session
- [ ] Role badge shows correctly in sidebar
- [ ] Students see only student pages
- [ ] Teachers see only teacher pages
- [ ] API calls include JWT token
- [ ] Logout clears session properly

## Key Files Modified
1. `frontend/app.py` - Login page
2. `frontend/utils.py` - Auth helpers and API wrappers
3. `frontend/pages/dashboard.py` - Already compatible
4. All other pages - Already compatible

## Backward Compatibility
✅ All existing pages work without modification
✅ API wrapper functions updated transparently
✅ Role-based access control enforced

## Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| "Cannot reach backend" | Backend not running | `uvicorn main:app --reload` |
| "Invalid credentials" | Wrong email/password | Check registration details |
| "Access denied" | Wrong institution ID prefix | Use STU* or TEA* format |
| JWT not sent | Function not updated | Use `_get_auth_headers()` |

## Performance Impact
- Minimal: One additional header per request
- No database queries added
- No additional API calls for auth validation

## Security Improvements
✅ JWT authentication on all API calls
✅ Role-based access control enforced at page level
✅ Institution ID validates role type
✅ Token stored in secure session

## Next Phase Features
- [ ] Password reset flow
- [ ] Email verification
- [ ] Token refresh mechanism
- [ ] Remember me option
- [ ] Two-factor authentication
- [ ] User profile management
