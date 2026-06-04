# ScholarSight Authentication Architecture

## Complete System Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         SCHOLARIGHT FRONTEND                                │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │  LOGIN PAGE (app.py)                                                │  │
│  │  ┌────────────────────────────────────────────────────────────────┐ │  │
│  │  │ Input Fields:                                                  │ │  │
│  │  │  • Institution ID (STU001 or TEA345)                          │ │  │
│  │  │  • Email (user@institution.com)                              │ │  │
│  │  │  • Password (••••••••)                                        │ │  │
│  │  └────────────────────────────────────────────────────────────────┘ │  │
│  │                            ↓                                         │  │
│  │  POST /auth/login (OAuth2PasswordRequestForm)                        │  │
│  │    {username: email, password: password}                            │  │
│  │                            ↓                                         │  │
│  │  ✅ Response: {access_token, token_type: "bearer"}                  │  │
│  │                            ↓                                         │  │
│  │  Store in session_state:                                            │  │
│  │  {                                                                  │  │
│  │    email: "user@institution.com",                                  │  │
│  │    institution_id: "STU001",                                       │  │
│  │    access_token: "eyJhbGciOiJIUzI1NiIs...",                       │  │
│  │    token_type: "bearer"                                            │  │
│  │  }                                                                  │  │
│  │                            ↓                                         │  │
│  │  get_role() → STU = "student" or TEA = "teacher"                   │  │
│  │                            ↓                                         │  │
│  │  Redirect → pages/dashboard.py                                      │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │  SIGNUP PAGE (pages/signup.py)                                      │  │
│  │  ┌────────────────────────────────────────────────────────────────┐ │  │
│  │  │ STEP 1: Verify Institution ID                                │ │  │
│  │  │  • Input: Institution ID (STU001 or TEA345)                  │ │  │
│  │  │  • POST /user/verify-role?institution_id=STU001              │ │  │
│  │  │  • Response: {token, message: "Verified as student"}         │ │  │
│  │  │                                                               │ │  │
│  │  │ STEP 2: Create Account                                       │ │  │
│  │  │  • Input: firstname, lastname, email, password               │ │  │
│  │  │  • Header: X-Verify-Token: {token from step 1}               │ │  │
│  │  │  • POST /user/signup (JSON body)                             │ │  │
│  │  │  • Response: {message: "Successfully created user"}          │ │  │
│  │  │  • Redirect → app.py (login page)                            │ │  │
│  │  └────────────────────────────────────────────────────────────────┘ │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │  ALL PROTECTED PAGES (utils.py)                                    │  │
│  │  ┌────────────────────────────────────────────────────────────────┐ │  │
│  │  │ Authentication Check:                                         │ │  │
│  │  │  • require_login() → Verify JWT token exists                 │ │  │
│  │  │  • require_teacher() → Verify role == "teacher"              │ │  │
│  │  │  • require_student() → Verify role == "student"              │ │  │
│  │  │                                                               │ │  │
│  │  │ API Calls with JWT:                                          │ │  │
│  │  │  • _get_auth_headers() → {Authorization: Bearer {token}}     │ │  │
│  │  │  • All requests include header in api_*() functions          │ │  │
│  │  │                                                               │ │  │
│  │  │ Navigation:                                                  │ │  │
│  │  │  • Teacher → predict, records, analysis                      │ │  │
│  │  │  • Student → my_record, my_analysis                          │ │  │
│  │  └────────────────────────────────────────────────────────────────┘ │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                      FASTAPI BACKEND (main.py)                              │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │  POST /auth/login (routers/authentication.py)                       │  │
│  │  1. Verify email exists in database                                 │  │
│  │  2. Hash and compare password                                       │  │
│  │  3. Generate JWT token with email in claims                         │  │
│  │  4. Return {access_token, token_type: "bearer"}                     │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │  POST /user/verify-role (routers/user.py)                           │  │
│  │  1. Check institution_id prefix (STU/TEA)                           │  │
│  │  2. Generate UUID token                                             │  │
│  │  3. Store role in temp_verification_store[token]                    │  │
│  │  4. Return {token, message: "Verified as student/teacher"}          │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │  POST /user/signup (routers/user.py)                                │  │
│  │  1. Verify X-Verify-Token header                                    │  │
│  │  2. Get role from temp_verification_store                           │  │
│  │  3. Create new User record with role and institution_id             │  │
│  │  4. Hash password with bcrypt                                       │  │
│  │  5. Return {message: "Successfully created user"}                   │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │  Protected Endpoints (predict, records, analysis, etc.)             │  │
│  │  1. Verify Authorization header: Bearer {token}                     │  │
│  │  2. Validate JWT token                                              │  │
│  │  3. Extract email from token claims (sub)                           │  │
│  │  4. Check user role from database                                   │  │
│  │  5. Enforce role restrictions                                       │  │
│  │  6. Process request and return data                                 │  │
│  │                                                                      │  │
│  │  Example: POST /predict                                             │  │
│  │    • Requires: Authorization: Bearer {token}                        │  │
│  │    • Checks: User is teacher                                        │  │
│  │    • Returns: Prediction result                                     │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │  Database (SQLAlchemy Models)                                       │  │
│  │  ┌────────────────────────────────────────────────────────────────┐ │  │
│  │  │ User Table                                                    │ │  │
│  │  │ • id (PK)                                                    │ │  │
│  │  │ • firstname                                                  │ │  │
│  │  │ • lastname                                                   │ │  │
│  │  │ • email (unique login credential)                           │ │  │
│  │  │ • password (hashed with bcrypt)                             │ │  │
│  │  │ • institution_id (STU001, TEA345, etc.)                     │ │  │
│  │  │ • role ("student" or "teacher")                             │ │  │
│  │  └────────────────────────────────────────────────────────────────┘ │  │
│  │                                                                      │  │
│  │  ┌────────────────────────────────────────────────────────────────┐ │  │
│  │  │ Blog Table (Student Performance Data)                         │ │  │
│  │  │ • student_id (FK to User.institution_id)                     │ │  │
│  │  │ • [Academic attributes...]                                   │ │  │
│  │  │ • Prediction (PASS/FAIL)                                     │ │  │
│  │  └────────────────────────────────────────────────────────────────┘ │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Authentication Flow Sequence

```
User Action              Frontend                Backend              Session
───────────────────────────────────────────────────────────────────────────────
1. Enter credentials          ↓
   (ID, email, password)      │
                              ├─ POST /auth/login
                              │  (form-data)────────→ Verify & create JWT
                              │                       ↓
                              │  ← Response: JWT token
                              │
2. Store in session      Session State Updated
   {                     with email, ID, token
    email: ...,
    institution_id: ...,
    access_token: ...,
    token_type: ...
   }
                              ↓
3. Determine role      get_role() from ID prefix
   (STU → student)      → "student" or "teacher"
   (TEA → teacher)
                              ↓
4. Route to page      Render dashboard
   with role-specific   (role-specific content)
   content
                              ↓
5. User navigates      Page calls api_*()
   to protected page    with JWT header
                              ├─ GET /students
                              │  Header: Authorization: Bearer {token}
                              │  ──────────────────────→ Verify JWT & role
                              │                         Return data
                              │
                              │ ← Response: Student data
                              ↓
6. Display data        Render results
                              ↓
7. Sign out            Clear session state
                       Delete all session keys
```

## Role-Based Access Matrix

```
┌────────────────────────────────────────────────────────────────────────┐
│                        ACCESS CONTROL MATRIX                            │
├────────────────────────────────────────────────────────────────────────┤
│ Page                    │ Student Access │ Teacher Access │ Anonymous  │
├────────────────────────┼────────────────┼────────────────┼────────────┤
│ app.py (Login)         │ ✅ Yes         │ ✅ Yes         │ ✅ Yes     │
│ pages/signup.py        │ ✅ Yes         │ ✅ Yes         │ ✅ Yes     │
│ pages/dashboard.py     │ ✅ Yes         │ ✅ Yes         │ ❌ No      │
│                        │ (student view) │ (teacher view) │ (redirect) │
│ pages/predict.py       │ ❌ No          │ ✅ Yes         │ ❌ No      │
│ pages/records.py       │ ❌ No          │ ✅ Yes         │ ❌ No      │
│ pages/analysis.py      │ ❌ No          │ ✅ Yes         │ ❌ No      │
│ pages/my_record.py     │ ✅ Yes         │ ❌ No          │ ❌ No      │
│ pages/my_analysis.py   │ ✅ Yes         │ ❌ No          │ ❌ No      │
└────────────────────────┴────────────────┴────────────────┴────────────┘

Authentication Check:
  ✅ Yes  = require_login() + require_student() or require_teacher()
  ❌ No   = Page blocked, error shown, or redirect to login

Role Determination:
  Institution ID "STU*" → role = "student"
  Institution ID "TEA*" → role = "teacher"
```

## JWT Token Lifecycle

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         JWT TOKEN LIFECYCLE                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  LOGIN                                                                  │
│    └─→ Generate JWT                                                     │
│         └─→ Claims: {sub: email}                                        │
│         └─→ Signed with SECRET_KEY                                      │
│         └─→ No expiration (future: add ACCESS_TOKEN_EXPIRE_MINUTES)    │
│                                                                         │
│  STORE                                                                  │
│    └─→ st.session_state["user"]["access_token"]                        │
│         └─→ Safe for local testing                                      │
│         └─→ HttpOnly cookies recommended for production                 │
│                                                                         │
│  USAGE                                                                  │
│    └─→ Each API call includes: Authorization: Bearer {token}           │
│         └─→ _get_auth_headers() adds automatically                      │
│         └─→ Backend verifies signature and claims                       │
│                                                                         │
│  LOGOUT                                                                 │
│    └─→ Delete from session_state                                       │
│         └─→ Token becomes invalid on backend                            │
│         └─→ User redirected to login                                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Error Handling Flow

```
Invalid Credentials
    └─→ 404 Not Found
        └─→ Show: "❌ Invalid credentials"
        └─→ Stay on login page
        └─→ Allow retry

Expired Token (Future)
    └─→ 401 Unauthorized
        └─→ Clear session
        └─→ Redirect to login
        └─→ Show: "Session expired, please login again"

Access Denied
    └─→ Teacher accessing student page
        └─→ Show: "⛔ Access denied. Teachers only."
        └─→ Stop page execution
        └─→ Redirect to dashboard

Network Error
    └─→ Cannot reach backend
        └─→ Show: "❌ Cannot reach the backend server"
        └─→ Suggest checking backend status
        └─→ Allow retry

Database Error
    └─→ 500 Internal Server Error
        └─→ Show: "❌ Server error 500"
        └─→ Log error details
        └─→ Suggest contacting admin
```

---

**This architecture ensures**:
1. ✅ Secure authentication with JWT tokens
2. ✅ Role-based access control at multiple levels
3. ✅ Clear separation between frontend and backend
4. ✅ Proper error handling and user feedback
5. ✅ Scalable and maintainable design
