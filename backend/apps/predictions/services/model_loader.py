"""
Model Loader Service
Thread-safe singleton caching service for loading and serving
WorthIQ machine learning models and preprocessing pipelines.
"""

import sys
import json
import logging
from pathlib import Path
import joblib

logger = logging.getLogger("predictions.model_loader")

class ModelLoadingError(Exception):
    """Raised when machine learning model artifacts cannot be loaded."""
    pass

class MLModelRegistry:
    """Singleton registry caching loaded ML models and preprocessors in memory."""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MLModelRegistry, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
            
        self.base_dir = Path(__file__).resolve().parent.parent.parent.parent.parent
        self.ml_dir = self.base_dir / "ml"
        self.models_dir = self.ml_dir / "models"
        
        # Ensure project root is on sys.path for unpickling custom transformers
        if str(self.base_dir) not in sys.path:
            sys.path.insert(0, str(self.base_dir))
            
        self.salary_model = None
        self.preprocessor = None
        self.quantile_p10 = None
        self.quantile_p50 = None
        self.quantile_p90 = None
        self.metadata = None
        self._is_loaded = False
        self._initialized = True

    def load_artifacts(self, force_reload=False):
        """Loads all ML models into memory if not already loaded."""
        if self._is_loaded and not force_reload:
            return
            
        logger.info(f"Loading WorthIQ ML model artifacts from {self.models_dir}...")
        
        # 1. Check artifact paths
        model_path = self.models_dir / "salary_model.joblib"
        prep_path = self.models_dir / "preprocessing_pipeline.joblib"
        if not prep_path.exists():
            prep_path = self.ml_dir / "data" / "processed" / "preprocessor.joblib"
            
        q10_path = self.models_dir / "quantile_models" / "quantile_p10.joblib"
        q50_path = self.models_dir / "quantile_models" / "quantile_p50.joblib"
        q90_path = self.models_dir / "quantile_models" / "quantile_p90.joblib"
        meta_path = self.models_dir / "model_metadata.json"
        
        missing = [str(p.name) for p in [model_path, prep_path, q10_path, q50_path, q90_path, meta_path] if not p.exists()]
        if missing:
            err_msg = f"Missing required ML model artifacts: {', '.join(missing)}"
            logger.error(err_msg)
            raise ModelLoadingError(err_msg)
            
        try:
            self.salary_model = joblib.load(model_path)
            self.preprocessor = joblib.load(prep_path)
            self.quantile_p10 = joblib.load(q10_path)
            self.quantile_p50 = joblib.load(q50_path)
            self.quantile_p90 = joblib.load(q90_path)
            
            with open(meta_path, "r", encoding="utf-8") as f:
                self.metadata = json.load(f)
                
            self._is_loaded = True
            logger.info("All WorthIQ ML artifacts loaded successfully into memory.")
        except Exception as e:
            err_msg = f"Failed to load ML model artifacts: {str(e)}"
            logger.exception(err_msg)
            raise ModelLoadingError(err_msg) from e

    def is_ready(self) -> bool:
        """Returns True if all model artifacts are loaded in memory."""
        return self._is_loaded

    def get_metadata(self) -> dict:
        """Returns safe model metadata dictionary."""
        if not self._is_loaded:
            self.load_artifacts()
        return self.metadata or {}

# Global singleton accessor
def get_model_registry() -> MLModelRegistry:
    registry = MLModelRegistry()
    if not registry.is_ready():
        try:
            registry.load_artifacts()
        except ModelLoadingError as e:
            logger.warning(f"Registry load deferred: {e}")
    return registry
