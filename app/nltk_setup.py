"""NLTK data initialization - run this at startup"""
import nltk
import os
from pathlib import Path


def setup_nltk_data():
    """Download and setup required NLTK data files"""
    
    # Create nltk_data directory if it doesn't exist
    nltk_data_dir = os.path.expanduser('~/nltk_data')
    Path(nltk_data_dir).mkdir(parents=True, exist_ok=True)
    
    # Add to NLTK path
    if nltk_data_dir not in nltk.data.path:
        nltk.data.path.insert(0, nltk_data_dir)
    
    # List of required NLTK resources
    required_resources = ['wordnet', 'punkt', 'punkt_tab', 'omw-1.4']
    
    for resource in required_resources:
        try:
            nltk.data.find(resource)
            print(f"✅ NLTK resource '{resource}' already exists")
        except LookupError:
            print(f"📥 Downloading NLTK resource: {resource}...")
            try:
                nltk.download(resource, quiet=True)
                print(f"✅ Successfully downloaded: {resource}")
            except Exception as e:
                print(f"⚠️  Failed to download {resource}: {e}")
                # Don't fail completely - some resources might be optional
