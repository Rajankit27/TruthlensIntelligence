# Terminal Testing Guide (PowerShell / Windows)

This guide provides the exact commands you can copy and paste into your Windows terminal (PowerShell) to test the authentication system and protected routes manually. 

> **Important Note for Windows Users:** 
> We use `curl.exe` instead of just `curl` because PowerShell aliases `curl` to `Invoke-WebRequest`, which behaves differently. We also use backticks (\`) to properly escape double-quotes inside the JSON bodies so that PowerShell passes the string perfectly to `curl.exe`.

---

## Phase 3: Authentication System Tests

### 1. Register a User
This command sends a `POST` request to the `/auth/register` endpoint with a test username and password.

**Command:**
```powershell
curl.exe -s -X POST -H 'Content-Type: application/json' -d "{\`"username\`":\`"testuser1\`", \`"password\`":\`"password123\`"}" http://127.0.0.1:5000/auth/register
```
**How it works:**
* `-s`: Silent mode (hides the progress bar).
* `-X POST`: Sets the HTTP method to POST.
* `-H`: Sets the corresponding headers (telling the server we are sending JSON).
* `-d`: The data payload. The backticks (\`) escape the JSON quotes specifically for PowerShell.

### 2. Login a User
This command logs the user in and replies with your **JWT Token**. You will need to copy the `"token": "..."` value for Phase 5.

**Command:**
```powershell
curl.exe -s -X POST -H 'Content-Type: application/json' -d "{\`"username\`":\`"testuser1\`", \`"password\`":\`"password123\`"}" http://127.0.0.1:5000/auth/login
```

---

## Phase 4: Database Logic Verification

### 1. Test Duplicate Registration (Data Persistence)
Run the register command again on a user that was already created. The application database should prevent the insert and return an "already exists" error.

**Command:**
```powershell
curl.exe -s -X POST -H 'Content-Type: application/json' -d "{\`"username\`":\`"testuser1\`", \`"password\`":\`"password123\`"}" http://127.0.0.1:5000/auth/register
```

---

## Phase 5: JWT Protected Routes

*Note: In the backend codebase, the analysis endpoint is located at `/predict`, not `/analyze`.*

### 1. Test Without Token (Should Fail)
This verifies that your route is securely protected against unauthorized requests.

**Command:**
```powershell
curl.exe -s -X POST -H 'Content-Type: application/json' -d "{\`"text\`":\`"This is a test fake news article.\`"}" http://127.0.0.1:5000/predict
```
**Expected Output:** `{"error": "Token missing"}`

### 2. Test With Token (Should Pass)
To make an authorized request, you must include the Authorization header formatted as `Bearer <YOUR_TOKEN>`. 
*(Replace `YOUR_TOKEN_HERE` with the actual token you received from the Phase 3 Login step).*

**Command:**
```powershell
curl.exe -s -X POST -H 'Content-Type: application/json' -H 'Authorization: Bearer YOUR_TOKEN_HERE' -d "{\`"text\`":\`"This is a test fake news article.\`"}" http://127.0.0.1:5000/predict
```
**Expected Output:** JSON prediction result containing `"confidence"` and `"prediction"`.

---

## Alternative: Using a Payload File
If you find escaping quotation marks with backticks annoying, you can store your JSON strictly in a file and use that to pass data into `curl.exe`:

1. Create a `payload.json` file containing:
   ```json
   {
     "text": "This is a test fake news article."
   }
   ```
2. Pass the file directly using `--data-binary` and `'@filename'`:
   ```powershell
   curl.exe -s -X POST -H 'Content-Type: application/json' -H 'Authorization: Bearer YOUR_TOKEN_HERE' --data-binary '@payload.json' http://127.0.0.1:5000/predict
   ```
