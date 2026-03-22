import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

project_name = "real-estate-ai"

list_of_files = [
    # --- Backend: Core & Security ---
    "backend/app/__init__.py",
    "backend/app/main.py",
    "backend/app/core/config.py",
    "backend/app/core/security.py",
    "backend/app/core/logger.py",
    "backend/app/core/exceptions.py",
    "backend/app/core/middleware.py", # For Rate Limiting & CORS
    
    # --- Backend: API & Auth ---
    "backend/app/api/v1/endpoints/api.py",
    "backend/app/api/v1/endpoints/auth.py",
    "backend/app/api/v1/endpoints/users.py",
    "backend/app/api/v1/endpoints/properties.py",
    "backend/app/api/deps.py",
    
    # --- Backend: New Advanced Services ---
    "backend/app/services/data_ops.py",
    "backend/app/services/agents/lease_agent.py",
    "backend/app/services/analysis/risk_engine.py",
    "backend/app/services/document_processing/pdf_parser.py",
    "backend/app/services/document_processing/ocr_service.py", # For scanned documents
    "backend/app/services/vector_store/pinecone_service.py", # For RAG/Semantic Search
    "backend/app/services/notifications/email_service.py", # For alerts & reports
    "backend/app/services/audit/audit_logger.py", # Security tracking of user actions
    
    # --- Backend: Database & Models ---
    "backend/app/db/session.py",
    "backend/app/db/base.py",
    "backend/app/models/domain/user.py",
    "backend/app/models/domain/property.py",
    "backend/app/models/domain/audit_log.py", # New: Track who accessed what
    "backend/app/models/schemas/auth.py",
    "backend/app/models/schemas/user.py",
    "backend/app/models/schemas/property.py",
    "backend/app/models/schemas/analysis.py",
    
    # --- Frontend Structure ---
    "frontend/src/app/page.tsx",
    "frontend/src/app/dashboard/page.tsx",
    "frontend/src/components/Navbar.tsx",
    "frontend/src/components/ProtectedRoute.tsx", # Frontend Auth guard
    "frontend/src/hooks/useAuth.ts",
    "frontend/src/lib/api-client.ts",
    "frontend/src/store/authStore.ts",
    "frontend/src/store/propertyStore.ts",
    "frontend/src/styles/globals.css",
    "frontend/next.config.js",
    "frontend/package.json",
    "frontend/Dockerfile",

    # --- Infrastructure ---
    "docker-compose.yml",
    "nginx/nginx.conf", # Reverse proxy for security/SSL
    ".env.example",
    ".gitignore",
    "README.md"
]

for filepath in list_of_files:
    filepath = Path(project_name) / Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for the file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filename} already exists")

# Auto-add __init__.py to all backend python directories
for root, dirs, files in os.walk(os.path.join(project_name, "backend/app")):
    if "__init__.py" not in files:
        Path(os.path.join(root, "__init__.py")).touch()