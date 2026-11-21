"""
WorthIQ - Feature Engineering Module
Provides scikit-learn compatible transformers and ColumnTransformer pipeline
for transforming categorical, numerical, and multi-label skills features.
Strictly ensures zero data leakage by fitting exclusively on training sets.
"""

import json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder, StandardScaler, RobustScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# 35 Canonical skills from Phase 1 profiles catalog
CANONICAL_SKILLS = [
    "AWS", "C++", "CI/CD", "CSS3", "Data Analysis", "Django", "Docker",
    "Express.js", "FastAPI", "Flutter", "Git", "Go", "GraphQL", "HTML5",
    "Java", "JavaScript", "Kubernetes", "Linux", "Machine Learning",
    "Microservices", "MongoDB", "Next.js", "Node.js", "NumPy", "Pandas",
    "PostgreSQL", "Python", "REST APIs", "React.js", "Redis", "SQL",
    "Scikit-Learn", "Spring Boot", "Tailwind CSS", "TypeScript"
]

class MultiLabelSkillsEncoder(BaseEstimator, TransformerMixin):
    """
    Scikit-learn compatible transformer that converts semicolon-separated
    skills strings or list-of-strings into a binary indicator matrix
    for canonical WorthIQ skills.
    """
    def __init__(self, canonical_skills=None):
        self.canonical_skills = canonical_skills
        
    def fit(self, X, y=None):
        # Establish canonical skills index during fit
        if self.canonical_skills is not None:
            self.skills_ = sorted(list(self.canonical_skills))
        else:
            self.skills_ = sorted(CANONICAL_SKILLS)
        self.skill_to_idx_ = {s: i for i, s in enumerate(self.skills_)}
        return self
        
    def transform(self, X):
        if not hasattr(self, "skill_to_idx_"):
            self.fit(X)
            
        # Handle Series or array
        if isinstance(X, pd.DataFrame):
            skills_series = X.iloc[:, 0]
        elif isinstance(X, pd.Series):
            skills_series = X
        elif isinstance(X, np.ndarray):
            skills_series = pd.Series(X.ravel())
        else:
            skills_series = pd.Series(list(X))
            
        n_samples = len(skills_series)
        n_skills = len(self.skills_)
        matrix = np.zeros((n_samples, n_skills), dtype=np.float32)
        
        for row_idx, item in enumerate(skills_series):
            if pd.isnull(item):
                continue
            if isinstance(item, str):
                tokens = [t.strip() for t in item.split(";") if t.strip()]
            elif isinstance(item, (list, tuple, set)):
                tokens = [str(t).strip() for t in item if str(t).strip()]
            else:
                tokens = [str(item).strip()]
                
            for token in tokens:
                if token in self.skill_to_idx_:
                    matrix[row_idx, self.skill_to_idx_[token]] = 1.0
                    
        return matrix
        
    def get_feature_names_out(self, input_features=None):
        skills = getattr(self, "skills_", CANONICAL_SKILLS)
        return [f"skill__{s.lower().replace(' ', '_').replace('.', '_').replace('+', 'p')}" for s in skills]


def build_preprocessor(categorical_strategy="onehot", numeric_scaler="standard") -> ColumnTransformer:
    """
    Constructs a ColumnTransformer combining:
    - OneHotEncoder for job_role, location, education
    - StandardScaler or RobustScaler for years_of_experience, company_rating
    - MultiLabelSkillsEncoder for skills_str
    """
    cat_cols = ["job_role", "location", "education"]
    num_cols = ["years_of_experience", "company_rating"]
    skill_cols = ["skills_str"]
    
    cat_transformer = OneHotEncoder(
        handle_unknown="ignore",
        sparse_output=False
    )
    
    num_transformer = StandardScaler() if numeric_scaler == "standard" else RobustScaler()
    skill_transformer = MultiLabelSkillsEncoder(CANONICAL_SKILLS)
    
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", cat_transformer, cat_cols),
            ("num", num_transformer, num_cols),
            ("skills", skill_transformer, skill_cols)
        ],
        remainder="drop"
    )
    
    return preprocessor

def get_engineered_feature_names(preprocessor: ColumnTransformer) -> list:
    """Extract flattened engineered feature names from the fitted ColumnTransformer."""
    names = []
    for name, transformer, cols in preprocessor.transformers_:
        if name == "cat":
            cat_names = list(transformer.get_feature_names_out(cols))
            names.extend(cat_names)
        elif name == "num":
            names.extend([f"num__{c}" for c in cols])
        elif name == "skills":
            names.extend(list(transformer.get_feature_names_out(cols)))
    return names
