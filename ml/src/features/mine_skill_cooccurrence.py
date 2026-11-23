"""
Skill Co-occurrence & Valuation Mining Script
Extracts canonical skill taxonomy, co-occurrence matrices, support, confidence,
lift, and median salary distributions from the verified 25,332 records.
"""

import sys
import json
from pathlib import Path
from collections import defaultdict, Counter
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
DATASET_PATH = BASE_DIR / "ml" / "data" / "processed" / "salary_features_dataset.csv"
OUTPUT_PATH = BASE_DIR / "ml" / "data" / "processed" / "skill_cooccurrence_matrix.json"

# Canonical Skill Taxonomy & Aliases
SKILL_TAXONOMY = {
    "Python": {
        "category": "Programming Languages",
        "aliases": ["py", "python3", "python 3"],
        "description": "General-purpose programming language widely used in AI, data science, and web backends."
    },
    "JavaScript": {
        "category": "Programming Languages",
        "aliases": ["js", "ecmascript", "es6"],
        "description": "Core client-side and full-stack runtime language powering modern web applications."
    },
    "TypeScript": {
        "category": "Programming Languages",
        "aliases": ["ts"],
        "description": "Typed superset of JavaScript providing static type definitions for enterprise codebases."
    },
    "Java": {
        "category": "Programming Languages",
        "aliases": ["core java", "java 11", "java 17"],
        "description": "Object-oriented, high-performance language widely used for large-scale enterprise services."
    },
    "C++": {
        "category": "Programming Languages",
        "aliases": ["cpp", "cplusplus", "c/c++"],
        "description": "High-performance systems language used in high-frequency trading, game engines, and low-latency systems."
    },
    "Go": {
        "category": "Programming Languages",
        "aliases": ["golang"],
        "description": "Concurrent compiled language developed by Google, dominant in cloud-native microservices."
    },
    "React.js": {
        "category": "Frontend",
        "aliases": ["react", "reactjs", "react.js"],
        "description": "Component-based declarative UI library developed by Meta for reactive single-page applications."
    },
    "Next.js": {
        "category": "Frontend",
        "aliases": ["nextjs", "next.js", "next"],
        "description": "React framework for server-side rendering (SSR), static site generation (SSG), and edge deployment."
    },
    "HTML5": {
        "category": "Frontend",
        "aliases": ["html"],
        "description": "Standard semantic markup language for structuring web documents."
    },
    "CSS3": {
        "category": "Frontend",
        "aliases": ["css"],
        "description": "Style sheet language used for describing presentation and responsive UI design."
    },
    "Tailwind CSS": {
        "category": "Frontend",
        "aliases": ["tailwind", "tailwindcss"],
        "description": "Utility-first CSS framework for rapid responsive interface development."
    },
    "Flutter": {
        "category": "Frontend",
        "aliases": ["dart/flutter", "flutter sdk"],
        "description": "Google cross-platform UI framework for compiling mobile, web, and desktop apps from single codebase."
    },
    "Node.js": {
        "category": "Backend",
        "aliases": ["nodejs", "node", "node.js"],
        "description": "Asynchronous event-driven JavaScript runtime built on Chrome's V8 engine."
    },
    "Express.js": {
        "category": "Backend",
        "aliases": ["express", "expressjs", "express.js"],
        "description": "Fast, unopinionated, minimalist web framework for Node.js."
    },
    "Django": {
        "category": "Backend",
        "aliases": ["django framework", "django rest framework", "drf"],
        "description": "High-level Python web framework encouraging clean, pragmatic design and rapid development."
    },
    "FastAPI": {
        "category": "Backend",
        "aliases": ["fast-api", "fastapi"],
        "description": "Modern, fast (high-performance) web framework for building APIs with Python 3.8+ based on standard type hints."
    },
    "Spring Boot": {
        "category": "Backend",
        "aliases": ["spring", "springboot", "spring-boot"],
        "description": "Opinionated Java enterprise framework for creating stand-alone, production-grade Spring applications."
    },
    "REST APIs": {
        "category": "Backend",
        "aliases": ["rest", "restful apis", "restful api", "rest api"],
        "description": "Architectural style for networked hypermedia systems facilitating client-server communication."
    },
    "Microservices": {
        "category": "Backend",
        "aliases": ["microservice", "microservices architecture"],
        "description": "Architectural approach designing software as small, independently deployable services."
    },
    "GraphQL": {
        "category": "Backend",
        "aliases": ["graphql api", "gql"],
        "description": "Query language for APIs and runtime for fulfilling queries with existing data."
    },
    "PostgreSQL": {
        "category": "Databases",
        "aliases": ["postgres", "postgresql db", "psql"],
        "description": "Powerful open-source object-relational database system with strong reliability and ACID guarantees."
    },
    "MongoDB": {
        "category": "Databases",
        "aliases": ["mongo", "mongodb atlas"],
        "description": "Document-oriented NoSQL database designed for high availability and horizontal scaling."
    },
    "SQL": {
        "category": "Databases",
        "aliases": ["structured query language", "rdbms"],
        "description": "Domain-specific language used in programming and managing relational data streams."
    },
    "Redis": {
        "category": "Databases",
        "aliases": ["redis cache"],
        "description": "In-memory data structure store used as a distributed cache, message broker, and fast database."
    },
    "AWS": {
        "category": "Cloud & DevOps",
        "aliases": ["amazon web services", "amazon aws"],
        "description": "Comprehensive cloud computing platform offering compute, storage, and managed services."
    },
    "Docker": {
        "category": "Cloud & DevOps",
        "aliases": ["docker containers", "dockerized"],
        "description": "Containerization platform packaging applications and dependencies into standardized units."
    },
    "Kubernetes": {
        "category": "Cloud & DevOps",
        "aliases": ["k8s", "kube"],
        "description": "Open-source system for automating deployment, scaling, and management of containerized applications."
    },
    "CI/CD": {
        "category": "Cloud & DevOps",
        "aliases": ["continuous integration", "cicd", "github actions", "gitlab ci"],
        "description": "Method of frequently delivering apps to customers by introducing automation into development stages."
    },
    "Linux": {
        "category": "Cloud & DevOps",
        "aliases": ["unix", "ubuntu", "debian", "redhat"],
        "description": "Open-source Unix-like operating system kernel dominant across servers and cloud infrastructure."
    },
    "Git": {
        "category": "Cloud & DevOps",
        "aliases": ["github", "gitlab", "version control"],
        "description": "Distributed version control system tracking source code modifications across engineering teams."
    },
    "Machine Learning": {
        "category": "Data & AI",
        "aliases": ["ml", "machine-learning"],
        "description": "Field of artificial intelligence enabling computer systems to learn and infer from data patterns."
    },
    "Scikit-learn": {
        "category": "Data & AI",
        "aliases": ["sklearn", "scikit learn"],
        "description": "Python module for machine learning built on NumPy, SciPy, and matplotlib."
    },
    "Pandas": {
        "category": "Data & AI",
        "aliases": ["pandas library"],
        "description": "Fast, flexible, and expressive data structures designed to make working with structured tabular data easy."
    },
    "NumPy": {
        "category": "Data & AI",
        "aliases": ["numpy library"],
        "description": "Core scientific computing library providing multidimensional array objects and linear algebra routines."
    },
    "Data Analysis": {
        "category": "Data & AI",
        "aliases": ["exploratory data analysis", "eda"],
        "description": "Process of inspecting, cleansing, transforming, and modeling data with the goal of discovering useful findings."
    }
}

# Build reverse alias mapping
ALIAS_LOOKUP = {}
for canon, meta in SKILL_TAXONOMY.items():
    ALIAS_LOOKUP[canon.lower()] = canon
    for alias in meta["aliases"]:
        ALIAS_LOOKUP[alias.lower()] = canon

def normalize_skill_name(raw_name):
    """Maps raw skill string to canonical name if recognized."""
    if not raw_name:
        return None
    cleaned = raw_name.strip().lower()
    return ALIAS_LOOKUP.get(cleaned, raw_name.strip())

def mine_cooccurrence():
    print(f"Reading dataset from {DATASET_PATH}...")
    df = pd.read_csv(DATASET_PATH)
    total_records = len(df)
    print(f"Total dataset records: {total_records}")

    # Track skill individual frequencies & salaries
    skill_counts = Counter()
    skill_salaries = defaultdict(list)
    pair_counts = Counter()
    pair_salaries = defaultdict(list)

    for _, row in df.iterrows():
        salary = float(row["annual_salary_inr"])
        skills_raw = str(row.get("skills_str", "")).split(";")
        
        # Canonicalize row skills
        row_skills = set()
        for s in skills_raw:
            norm = normalize_skill_name(s)
            if norm and norm in SKILL_TAXONOMY:
                row_skills.add(norm)

        for s in row_skills:
            skill_counts[s] += 1
            skill_salaries[s].append(salary)

        # Pairs
        sorted_skills = sorted(list(row_skills))
        for i in range(len(sorted_skills)):
            for j in range(i + 1, len(sorted_skills)):
                pair = (sorted_skills[i], sorted_skills[j])
                pair_counts[pair] += 1
                pair_salaries[pair].append(salary)

    # Compile individual skill statistics
    skill_stats = {}
    for skill, count in skill_counts.items():
        salaries = skill_salaries[skill]
        skill_stats[skill] = {
            "frequency": count,
            "support_pct": round((count / total_records) * 100, 2),
            "median_salary": float(np.median(salaries)),
            "mean_salary": float(round(np.mean(salaries), 2)),
            "p25_salary": float(np.percentile(salaries, 25)),
            "p75_salary": float(np.percentile(salaries, 75)),
            "category": SKILL_TAXONOMY[skill]["category"],
            "description": SKILL_TAXONOMY[skill]["description"]
        }

    # Compile pairwise co-occurrence relationships
    cooccurrence_list = []
    for (s_a, s_b), count in pair_counts.items():
        if count < 5:  # Minimum support threshold
            continue
            
        salaries = pair_salaries[(s_a, s_b)]
        supp_ab = count / total_records
        supp_a = skill_counts[s_a] / total_records
        supp_b = skill_counts[s_b] / total_records
        
        # Confidence P(B|A) and P(A|B)
        conf_a_to_b = count / skill_counts[s_a]
        conf_b_to_a = count / skill_counts[s_b]
        lift = supp_ab / (supp_a * supp_b) if (supp_a * supp_b) > 0 else 1.0

        cooccurrence_list.append({
            "skill_a": s_a,
            "skill_b": s_b,
            "pair_count": count,
            "support_pct": round(supp_ab * 100, 3),
            "confidence_a_to_b": round(conf_a_to_b * 100, 2),
            "confidence_b_to_a": round(conf_b_to_a * 100, 2),
            "lift": round(lift, 2),
            "pair_median_salary": float(np.median(salaries)),
            "pair_mean_salary": float(round(np.mean(salaries), 2))
        })

    cooccurrence_list.sort(key=lambda x: x["pair_count"], reverse=True)

    result_payload = {
        "total_dataset_records": total_records,
        "taxonomy": SKILL_TAXONOMY,
        "skill_statistics": skill_stats,
        "top_cooccurrences": cooccurrence_list[:120],  # Top 120 validated relationships
        "generated_timestamp": pd.Timestamp.now().isoformat()
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(result_payload, f, indent=2)

    print(f"Co-occurrence mining complete! Saved to {OUTPUT_PATH}")
    print(f"Top 5 most frequent pairs:")
    for pair in cooccurrence_list[:5]:
        print(f"  {pair['skill_a']} + {pair['skill_b']}: {pair['pair_count']} times (Median: ₹{pair['pair_median_salary']:,.0f}, Lift: {pair['lift']})")

if __name__ == "__main__":
    mine_cooccurrence()
