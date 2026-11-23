import os
import sys
import time
import json
import statistics
import requests

BASE_URL = "http://localhost:8000"

def get_auth_token():
    test_email = "benchmark_eval@worthiq.com"
    test_password = "BenchmarkPassword123!"

    login_resp = requests.post(f"{BASE_URL}/api/auth/login/", json={"email": test_email, "password": test_password})
    if login_resp.status_code != 200:
        reg_resp = requests.post(f"{BASE_URL}/api/auth/register/", json={
            "email": test_email,
            "password": test_password,
            "confirm_password": test_password,
            "full_name": "Benchmark Evaluation User"
        })
        if reg_resp.status_code in [200, 201]:
            data = reg_resp.json()
            token = data.get('tokens', {}).get('access') or data.get('access')
            refresh = data.get('tokens', {}).get('refresh') or data.get('refresh')
        else:
            raise RuntimeError(f"Could not register test user: {reg_resp.text}")
    else:
        data = login_resp.json()
        token = data.get('tokens', {}).get('access') or data.get('access')
        refresh = data.get('tokens', {}).get('refresh') or data.get('refresh')

    headers = {"Authorization": f"Bearer {token}"}

    # Ensure profile exists
    prof_resp = requests.get(f"{BASE_URL}/api/profile/", headers=headers)
    if prof_resp.status_code == 404:
        create_resp = requests.post(f"{BASE_URL}/api/profile/", headers=headers, json={
            "job_role": "Full Stack Developer",
            "years_of_experience": 3.0,
            "location": "Bengaluru",
            "education": "Bachelor's Degree",
            "skills": ["Python", "Django", "React.js", "Docker", "PostgreSQL"]
        })
        if create_resp.status_code not in [200, 201]:
            print("Warning: Profile creation returned:", create_resp.status_code, create_resp.text)

    return token, refresh, test_email, test_password

def run_benchmarks():
    print(f"Connecting to live backend server at {BASE_URL}...")
    token, initial_refresh, test_email, test_password = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    print("Test user authenticated and profile initialized.")

    benchmarks_config = [
        {
            "name": "Auth: Login",
            "method": "POST",
            "url": f"{BASE_URL}/api/auth/login/",
            "json": {"email": test_email, "password": test_password},
            "headers": {},
            "iterations": 10
        },
        {
            "name": "Auth: Token Refresh",
            "method": "POST_REFRESH",
            "url": f"{BASE_URL}/api/auth/token/refresh/",
            "headers": {},
            "iterations": 10
        },
        {
            "name": "Profile: Retrieve (User Profile)",
            "method": "GET",
            "url": f"{BASE_URL}/api/profile/",
            "headers": headers,
            "iterations": 15
        },
        {
            "name": "ML Engine: Salary Prediction",
            "method": "POST",
            "url": f"{BASE_URL}/api/predictions/salary/",
            "headers": headers,
            "json": {
                "job_role": "Full Stack Developer",
                "years_of_experience": 3.5,
                "location": "Bengaluru",
                "education": "Bachelor's Degree",
                "skills": ["Python", "Django", "React.js", "Docker", "PostgreSQL"]
            },
            "iterations": 12
        },
        {
            "name": "Intelligence: Job Role Matching",
            "method": "POST",
            "url": f"{BASE_URL}/api/intelligence/roles/match/",
            "headers": headers,
            "json": {
                "skills": ["Python", "Django", "React.js", "PostgreSQL", "Docker"]
            },
            "iterations": 12
        },
        {
            "name": "Intelligence: Skill Impact Analysis",
            "method": "GET",
            "url": f"{BASE_URL}/api/intelligence/skills/impact/",
            "headers": headers,
            "iterations": 10
        },
        {
            "name": "Intelligence: Global SHAP Explanations",
            "method": "GET",
            "url": f"{BASE_URL}/api/intelligence/explanations/global/",
            "headers": headers,
            "iterations": 10
        },
        {
            "name": "Intelligence: Career Roadmap Generation",
            "method": "POST",
            "url": f"{BASE_URL}/api/intelligence/roadmaps/",
            "headers": headers,
            "json": {
                "target_role_id": 4,
                "current_role": "Full Stack Developer",
                "current_experience": 3.0,
                "current_skills": ["Python", "Django", "React.js"]
            },
            "iterations": 8
        },
        {
            "name": "Simulator: What-If Compare",
            "method": "POST",
            "url": f"{BASE_URL}/api/scenarios/compare/",
            "headers": headers,
            "json": {
                "include_baseline": True,
                "new_scenarios": [
                    {
                        "name": "Cloud DevOps Pivot",
                        "job_role": "DevOps Engineer",
                        "years_of_experience": 4.0,
                        "location": "Bengaluru",
                        "education": "Bachelor's Degree",
                        "skills": ["AWS", "Docker", "Kubernetes", "Python"]
                    }
                ]
            },
            "iterations": 10
        },
        {
            "name": "Simulator: List Scenarios",
            "method": "GET",
            "url": f"{BASE_URL}/api/scenarios/",
            "headers": headers,
            "iterations": 15
        },
        {
            "name": "Reports: Generate Report Snapshot",
            "method": "POST",
            "url": f"{BASE_URL}/api/reports/generate/",
            "headers": headers,
            "json": {
                "title": "Benchmark Career Strategy",
                "report_type": "salary_prediction",
                "summary": "Benchmark performance test report evaluation."
            },
            "iterations": 5
        }
    ]

    all_results = []

    for cfg in benchmarks_config:
        name = cfg["name"]
        print(f"Benchmarking {name} ({cfg['iterations']} iterations)...")
        latencies = []
        errors = 0

        for i in range(cfg["iterations"]):
            t0 = time.perf_counter()
            try:
                if cfg["method"] == "GET":
                    resp = requests.get(cfg["url"], headers=cfg["headers"], timeout=20)
                elif cfg["method"] == "POST":
                    resp = requests.post(cfg["url"], headers=cfg["headers"], json=cfg.get("json"), timeout=20)
                elif cfg["method"] == "POST_REFRESH":
                    # Get fresh token to refresh
                    l_res = requests.post(f"{BASE_URL}/api/auth/login/", json={"email": test_email, "password": test_password})
                    cur_ref = l_res.json().get('tokens', {}).get('refresh')
                    t0 = time.perf_counter()
                    resp = requests.post(cfg["url"], json={"refresh": cur_ref}, timeout=20)
                else:
                    raise ValueError("Unknown method")
                
                elapsed_ms = (time.perf_counter() - t0) * 1000.0
                latencies.append(elapsed_ms)
                if resp.status_code not in [200, 201]:
                    errors += 1
                    if i == 0:
                        print(f"  Warning: First iteration returned status {resp.status_code}: {resp.text[:120]}")
            except Exception as e:
                elapsed_ms = (time.perf_counter() - t0) * 1000.0
                latencies.append(elapsed_ms)
                errors += 1

        latencies_sorted = sorted(latencies)
        avg_latency = statistics.mean(latencies_sorted)
        p50 = statistics.median(latencies_sorted)
        p90 = latencies_sorted[int(len(latencies_sorted) * 0.9)]
        p95 = latencies_sorted[int(len(latencies_sorted) * 0.95)]

        res_obj = {
            "name": name,
            "endpoint": cfg["url"].replace(BASE_URL, ""),
            "total_requests": cfg["iterations"],
            "successful_requests": cfg["iterations"] - errors,
            "error_rate_pct": round((errors / cfg["iterations"]) * 100.0, 1),
            "avg_latency_ms": round(avg_latency, 2),
            "min_latency_ms": round(latencies_sorted[0], 2),
            "p50_latency_ms": round(p50, 2),
            "p90_latency_ms": round(p90, 2),
            "p95_latency_ms": round(p95, 2),
            "max_latency_ms": round(latencies_sorted[-1], 2),
            "throughput_req_sec": round(1000.0 / avg_latency, 2) if avg_latency > 0 else 0
        }
        all_results.append(res_obj)

    # Output JSON & print
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'testing', 'reports', 'performance')
    os.makedirs(output_dir, exist_ok=True)
    out_file = os.path.join(output_dir, 'performance_metrics.json')
    with open(out_file, 'w') as f:
        json.dump(all_results, f, indent=2)

    print("\n" + "="*85)
    print(f"{'Endpoint':<40} | {'Avg (ms)':<9} | {'P50 (ms)':<9} | {'P95 (ms)':<9} | {'Throughput':<11} | {'Error %'}")
    print("="*85)
    for r in all_results:
        print(f"{r['name']:<40} | {r['avg_latency_ms']:<9} | {r['p50_latency_ms']:<9} | {r['p95_latency_ms']:<9} | {r['throughput_req_sec']:<11} | {r['error_rate_pct']}%")
    print("="*85)

if __name__ == '__main__':
    run_benchmarks()
