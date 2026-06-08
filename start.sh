#!/bin/bash
# Pre-startup setup for Render deployment

echo "🔧 Setting up NLTK data..."
python -c "
import nltk
import os

# Ensure NLTK data directory
nltk_dir = os.path.expanduser('~/nltk_data')
os.makedirs(nltk_dir, exist_ok=True)

# Download required resources
resources = ['punkt', 'punkt_tab', 'wordnet', 'omw-1.4']
for resource in resources:
    try:
        nltk.data.find(resource)
        print(f'✅ {resource} already exists')
    except LookupError:
        print(f'📥 Downloading {resource}...')
        nltk.download(resource, quiet=False)
        print(f'✅ Downloaded {resource}')
"

echo "✅ NLTK setup complete!"
echo "🚀 Starting application..."

# Start the app
uvicorn app.main:app --host 0.0.0.0 --port $PORT
