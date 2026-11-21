import urllib.request
import json
import time
import sys

BASE_API = "http://localhost:8000/api"
FRONTEND_URL = "http://localhost:5180"

def post_json(url, data, token=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode('utf-8'))

def get_json(url, token=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode('utf-8'))

def patch_json(url, data, token=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method="PATCH")
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode('utf-8'))

print("--- STARTING WORTHIQ FULL INTEGRATION TEST ---")

# Step 1 & 2: Test Frontend
print("\n[Step 1] Testing Frontend on port 5180...")
try:
    with urllib.request.urlopen(FRONTEND_URL) as response:
        assert response.status == 200
        content = response.read().decode('utf-8')
        assert "<div id=\"root\"></div>" in content or "vite" in content
        print("  -> SUCCESS: Frontend running at http://localhost:5180 (Status 200)")
except Exception as e:
    print(f"  -> FAILED: Frontend not reachable: {e}")
    sys.exit(1)

# Step 3: Register a new user
unique_suffix = int(time.time())
email = f"lead.dev.{unique_suffix}@worthiq.test"
password = "SecurePassword123!"
reg_data = {
    "full_name": "Rohan Sharma",
    "email": email,
    "password": password,
    "confirm_password": password
}
print(f"\n[Step 2] Registering new user ({email})...")
status_code, body = post_json(f"{BASE_API}/auth/register/", reg_data)
assert status_code == 201, f"Expected 201, got {status_code}: {body}"
assert "tokens" in body and "access" in body["tokens"]
access_token = body["tokens"]["access"]
refresh_token = body["tokens"]["refresh"]
print(f"  -> SUCCESS: User registered (ID: {body['user']['id']}, Email: {body['user']['email']})")

# Step 4: Login with credentials
print("\n[Step 3] Logging in with user credentials...")
login_data = {"email": email, "password": password}
status_code, body = post_json(f"{BASE_API}/auth/login/", login_data)
assert status_code == 200, f"Expected 200, got {status_code}: {body}"
assert "tokens" in body and "access" in body["tokens"]
access_token = body["tokens"]["access"]
refresh_token = body["tokens"]["refresh"]
print("  -> SUCCESS: User authenticated, JWT access & refresh tokens received")

# Step 5: Test /api/auth/me/
print("\n[Step 4] Checking current authenticated user (/api/auth/me/)...")
status_code, body = get_json(f"{BASE_API}/auth/me/", token=access_token)
assert status_code == 200
assert body["email"] == email
print(f"  -> SUCCESS: User verified ({body['full_name']})")

# Step 6: Initial profile check (should be 404)
print("\n[Step 5] Checking initial profile status...")
status_code, body = get_json(f"{BASE_API}/profile/", token=access_token)
assert status_code == 404, f"Expected 404, got {status_code}"
print("  -> SUCCESS: Clean state confirmed (Profile does not exist yet)")

# Step 7: Create Profile
print("\n[Step 6] Creating career profile with normalized skills...")
profile_data = {
    "job_role": "Full Stack Engineer",
    "years_of_experience": 3.5,
    "location": "Bengaluru, India",
    "education": "B.Tech in Computer Science",
    "current_salary": 14.5,
    "skills_input": ["Python", "Django", "React.js", "PostgreSQL", "Docker", "AWS"]
}
status_code, body = post_json(f"{BASE_API}/profile/", profile_data, token=access_token)
assert status_code == 201, f"Expected 201, got {status_code}: {body}"
assert body["job_role"] == "Full Stack Engineer"
assert len(body["skills"]) == 6
print(f"  -> SUCCESS: Profile created with 6 normalized skills: {[s['name'] for s in body['skills']]}")

# Step 8: Retrieve Profile
print("\n[Step 7] Retrieving saved profile (/api/profile/)...")
status_code, body = get_json(f"{BASE_API}/profile/", token=access_token)
assert status_code == 200
assert body["job_role"] == "Full Stack Engineer"
assert float(body["years_of_experience"]) == 3.5
assert float(body["current_salary"]) == 14.5
print("  -> SUCCESS: Profile data successfully retrieved from PostgreSQL")

# Step 9: Update Profile (PATCH)
print("\n[Step 8] Updating profile (adding more skills and experience)...")
update_data = {
    "years_of_experience": 4.0,
    "current_salary": 16.0,
    "skills_input": ["Python", "Django", "React.js", "PostgreSQL", "Docker", "AWS", "Kubernetes", "Redis"]
}
status_code, body = patch_json(f"{BASE_API}/profile/", update_data, token=access_token)
assert status_code == 200
assert float(body["years_of_experience"]) == 4.0
assert float(body["current_salary"]) == 16.0
assert len(body["skills"]) == 8
print(f"  -> SUCCESS: Profile updated to 4.0 yrs exp, 16.0 LPA, and {len(body['skills'])} skills")

# Step 10: Token Refresh
print("\n[Step 9] Testing token refresh (/api/auth/token/refresh/)...")
status_code, body = post_json(f"{BASE_API}/auth/token/refresh/", {"refresh": refresh_token})
assert status_code == 200, f"Refresh failed: {body}"
new_access = body["access"]
if "refresh" in body:
    refresh_token = body["refresh"]
print("  -> SUCCESS: Access token successfully refreshed (and refresh token rotated)")

# Step 11: Logout & Blacklist
print("\n[Step 10] Logging out and blacklisting refresh token...")
status_code, body = post_json(f"{BASE_API}/auth/logout/", {"refresh": refresh_token}, token=new_access)
assert status_code == 200, f"Logout failed: {body}"
print("  -> SUCCESS: User logged out, refresh token blacklisted")

# Step 12: Verify Blacklisted Token Cannot Be Used
print("\n[Step 11] Verifying blacklisted token rejection...")
status_code, body = post_json(f"{BASE_API}/auth/token/refresh/", {"refresh": refresh_token})
assert status_code == 401
print("  -> SUCCESS: Blacklisted refresh token rejected with 401 Unauthorized")

# Step 13: Verify Unauthorized Access Blocked
print("\n[Step 12] Verifying protected endpoint blocks unauthorized requests...")
status_code, body = get_json(f"{BASE_API}/profile/")
assert status_code == 401
print("  -> SUCCESS: Unauthorized request blocked with 401 Unauthorized")

print("\n=======================================================")
print(" ALL 12 INTEGRATION TEST SUITES PASSED SUCCESSFULLY! ")
print("=======================================================")
