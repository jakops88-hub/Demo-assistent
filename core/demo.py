"""
Demo mode functionality for the Streamlit RAG application.
Provides demo asset loading and configuration overrides.
"""
import json
from pathlib import Path
from typing import Dict, List, Tuple, Any
from core.logging_utils import get_logger

logger = get_logger(__name__)


class DemoConfig:
    """Demo configuration and asset management."""
    
    def __init__(self, demo_assets_dir: str = "demo_assets"):
        """
        Initialize demo configuration.
        
        Args:
            demo_assets_dir: Path to demo assets directory
        """
        self.demo_assets_dir = Path(demo_assets_dir)
        self.demo_files = {
            'hr': self.demo_assets_dir / 'hr' / 'employee_handbook_demo.txt',
            'legal': self.demo_assets_dir / 'legal' / 'lease_agreement_demo.txt',
            'commerce': self.demo_assets_dir / 'commerce' / 'sales_q4_demo.csv'
        }
        self.questions_file = self.demo_assets_dir / 'demo_questions.json'
    
    def get_demo_file_paths(self) -> List[str]:
        """
        Get list of demo file paths.
        
        Returns:
            List of absolute file paths
        """
        paths = []
        for file_path in self.demo_files.values():
            if file_path.exists():
                paths.append(str(file_path.absolute()))
            else:
                logger.warning(f"Demo file not found: {file_path}")
        
        return paths
    
    def load_demo_questions(self) -> Dict[str, List[str]]:
        """
        Load demo questions from JSON file.
        
        Returns:
            Dictionary with categories as keys and lists of questions as values
        """
        if not self.questions_file.exists():
            logger.error(f"Demo questions file not found: {self.questions_file}")
            return {}
        
        try:
            with open(self.questions_file, 'r') as f:
                questions = json.load(f)
            logger.info(f"Loaded {sum(len(q) for q in questions.values())} demo questions")
            return questions
        except Exception as e:
            logger.error(f"Error loading demo questions: {e}")
            return {}
    
    def get_demo_config_overrides(self) -> Dict[str, Any]:
        """
        Get configuration overrides for demo mode.
        These settings ensure deterministic, reproducible outputs.
        
        Returns:
            Dictionary of configuration overrides
        """
        return {
            'temperature': 0,
            'top_k': 5,
            'chunk_size': 900,
            'chunk_overlap': 150
        }
    
    def validate_demo_assets(self) -> Tuple[bool, List[str]]:
        """
        Validate that all demo assets exist.
        
        Returns:
            Tuple of (all_exist, missing_files)
        """
        missing = []
        
        for category, file_path in self.demo_files.items():
            if not file_path.exists():
                missing.append(f"{category}: {file_path}")
        
        if not self.questions_file.exists():
            missing.append(f"questions: {self.questions_file}")
        
        return len(missing) == 0, missing
