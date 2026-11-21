# DBeaver Database Setup & Management Guide for WorthIQ

This guide provides exact step-by-step instructions to connect **DBeaver** to the **WorthIQ PostgreSQL Docker container** running on your Windows machine.

---

## 1. Prerequisites

1. **Docker Desktop** running on Windows.
2. The WorthIQ PostgreSQL container running:
   ```powershell
   cd database
   docker compose up -d
   ```
3. **DBeaver Community Edition** installed on your system.
   - If not installed, download the installer from: [https://dbeaver.io/download/](https://dbeaver.io/download/)

---

## 2. Connection Parameters

When configuring a new connection in DBeaver, use the following credentials:

| Setting | Value | Notes |
| :--- | :--- | :--- |
| **Database Type** | `PostgreSQL` | Select PostgreSQL in connection wizard |
| **Host** | `localhost` or `127.0.0.1` | Local port forward from Docker |
| **Port** | `5432` | Standard PostgreSQL port |
| **Database** | `worthiq_db` | Configured via `database/.env` |
| **Username** | `worthiq_user` | Configured via `database/.env` |
| **Password** | `worthiq_password` | Configured via `database/.env` |
| **Authentication** | `Database Native` | Default |

---

## 3. Step-by-Step Connection Instructions

1. **Open DBeaver**.
2. Click **Database** in the top menu &rarr; **New Database Connection** (or click the plug icon with a `+`).
3. Select **PostgreSQL** from the list of drivers and click **Next**.
4. In the **Connection Settings** window:
   - **Host**: `localhost`
   - **Port**: `5432`
   - **Database**: `worthiq_db`
   - **Username**: `worthiq_user`
   - **Password**: `worthiq_password`
   - Check the **Show all databases** checkbox if desired.
5. Click **Test Connection ...** in the bottom left corner.
   - *Note*: If DBeaver asks to download the PostgreSQL JDBC driver files, click **Download**.
   - You should see a dialog confirming: `Connected! Server: PostgreSQL 16.x`.
6. Click **Finish**.

---

## 4. How to Inspect & Manage WorthIQ Data in DBeaver

### A. View Database Tables
1. Expand the `worthiq_db` connection in the left-hand **Database Navigator** panel.
2. Expand **Databases** &rarr; **worthiq_db** &rarr; **Schemas** &rarr; **public** &rarr; **Tables**.
3. You will see all 15 tables created by Django:
   - `accounts_user` – User credentials, full name, active status, date joined.
   - `profiles_userprofile` – User career profiles (job role, experience, location, education, current salary).
   - `profiles_skill` – Normalized skills table (name, created_at).
   - `profiles_userprofile_skills` – Normalized many-to-many relationship join table.
   - `token_blacklist_blacklistedtoken` – Revoked JWT refresh tokens.
   - `token_blacklist_outstandingtoken` – Issued JWT refresh tokens.

### B. View Records
1. Double-click any table (e.g. `accounts_user` or `profiles_userprofile`).
2. Click the **Data** tab at the top of the main editor.
3. All registered users and career profiles appear in a spreadsheet-like grid.

### C. Inspect Columns and Data Types
1. Click the **Properties** tab for any table.
2. Inspect column names, data types (`varchar`, `numeric`, `timestamp with time zone`), primary keys, and foreign keys.

### D. Execute SQL Queries
1. Press `Ctrl + ]` or click **SQL Editor** &rarr; **New SQL Script**.
2. Run sample queries:
   ```sql
   -- View all users and their profile details
   SELECT 
       u.id AS user_id,
       u.full_name,
       u.email,
       p.job_role,
       p.years_of_experience,
       p.current_salary,
       p.location
   FROM accounts_user u
   LEFT JOIN profiles_userprofile p ON u.id = p.user_id;
   ```
   ```sql
   -- View normalized skills per user
   SELECT 
       u.full_name,
       p.job_role,
       s.name AS skill_name
   FROM accounts_user u
   JOIN profiles_userprofile p ON u.id = p.user_id
   JOIN profiles_userprofile_skills ps ON p.id = ps.userprofile_id
   JOIN profiles_skill s ON ps.skill_id = s.id
   ORDER BY u.full_name, s.name;
   ```

### E. View Entity-Relationship (ER) Diagrams
1. Double-click the `public` schema in Database Navigator.
2. Click the **ER Diagram** tab in the main editor.
3. DBeaver will visually render the relationships between `accounts_user`, `profiles_userprofile`, `profiles_skill`, and `profiles_userprofile_skills`.

---

## 5. Docker CLI Commands Reference

To manage the PostgreSQL container from PowerShell:

```powershell
# Navigate to database directory
cd database

# Start container in background
docker compose up -d

# Check container status and health check
docker compose ps

# View live container logs
docker compose logs -f

# Restart container
docker compose restart

# Stop container (safely preserves data volume)
docker compose stop

# Open interactive psql shell inside container
docker exec -it worthiq_postgres psql -U worthiq_user -d worthiq_db
```
