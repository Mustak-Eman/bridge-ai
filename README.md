# Bridge AI

> AI-powered operational intelligence for community organizations.

Bridge AI is a production-style full-stack AI Operations Platform that transforms complex operational documents into structured, actionable insights for nonprofits, workforce development organizations, housing agencies, educational institutions, food assistance programs, and local governments.

Instead of acting as a general-purpose chatbot, Bridge AI analyzes operational documents and produces consistent, structured findings that help staff understand policies, eligibility requirements, required documentation, deadlines, risks, and recommended next steps.

---

## Project Overview

Community organizations rely on lengthy policy manuals, government guidance, grant requirements, and internal operating procedures. Staff often spend significant time locating critical information needed to support clients and make operational decisions.

Bridge AI streamlines this process by automatically extracting key operational knowledge into a standardized format, reducing manual review while improving consistency and efficiency.

Typical questions Bridge AI helps answer include:

- Who is eligible?
- What documents are required?
- What deadlines must be met?
- What actions should staff take?
- What operational risks exist?
- What are the recommended next steps?

---

## Features

### AI Document Analysis

Upload operational documents such as:

- Policy manuals
- Program guides
- Housing policies
- Internal procedures
- Service documentation
- Eligibility requirements

Bridge AI generates structured operational findings including:

- Executive Summary
- Action Items
- Required Documents
- Eligibility Requirements
- Important Deadlines
- Operational Risks
- Recommended Next Steps
- Verification Status

---

### Workspace Management

Organize multiple organizations or departments into separate workspaces.

---

### Project Management

Create projects within each workspace to organize operational initiatives and document analyses.

---

### Modern Dashboard

Professional user interface built with Next.js and Tailwind CSS featuring:

- Workspace selector
- Project selector
- Document upload
- Structured AI analysis results
- Operational metadata display
- Responsive design

---

## Architecture

Bridge AI follows a layered architecture designed for maintainability, scalability, and testability.

```text
                    Frontend
        Next.js • React • TypeScript

                      │

                 REST API

                      │

                   FastAPI

                      │

              Application Services

                      │

             Repository Pattern

                      │

              SQLAlchemy ORM

                      │

         SQLite / PostgreSQL

                      │

          AI Provider Abstraction

             Fake Provider
      (Production-ready architecture)
```

### Architectural Principles

- Layered Architecture
- Repository Pattern
- Service Layer
- Dependency Injection
- Provider Abstraction
- Pydantic Validation
- Modular API Design
- Production-ready Configuration
- Comprehensive Testing

---

## AI Analysis Workflow

1. Upload an operational document.
2. Validate file type and content.
3. Extract document text.
4. Generate structured AI prompt.
5. Analyze document using the AI provider.
6. Validate structured output.
7. Display operational findings in the dashboard.

---

## Technology Stack

### Backend

- FastAPI
- SQLAlchemy 2
- Alembic
- Pydantic v2
- SQLite
- PostgreSQL-ready
- Dependency Injection
- Repository Pattern
- Pytest

### Frontend

- Next.js 16
- React
- TypeScript
- Tailwind CSS

### AI Layer

- Provider Abstraction
- Structured Output Models
- Prompt Templates
- Fake AI Provider
- Document Validation
- Document Parsing

---

## Project Structure

```text
bridge-ai/

├── backend/
│   ├── app/
│   │   ├── ai/
│   │   ├── api/
│   │   ├── core/
│   │   ├── domain/
│   │   ├── repositories/
│   │   ├── schemas/
│   │   └── services/
│   └── tests/
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   └── services/
│   └── public/
│
└── README.md
```

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/Mustak-Eman/bridge-ai.git

cd bridge-ai
```

---

### Backend Setup

```bash
cd backend

python -m venv .venv
```

Activate the virtual environment.

Windows

```powershell
.venv\Scripts\activate
```

macOS/Linux

```bash
source .venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Start the backend.

```bash
uvicorn app.main:app --reload
```

---

### Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

---

## Environment Variables

Create a `.env` file inside the backend directory.

Example:

```env
DATABASE_URL=sqlite:///bridge_ai.db

AI_PROVIDER=fake

AI_MODEL=fake-document-analyzer-v1
```

---

## API Overview

| Endpoint | Description |
|----------|-------------|
| GET /api/v1/health | Health check |
| Workspaces | Workspace CRUD operations |
| Projects | Project CRUD operations |
| Document Analysis | Upload and analyze operational documents |

Interactive API documentation is available at:

```
/docs
```

---

## Example AI Analysis

### Executive Summary

Housing applicants must provide proof of residency and proof of income before eligibility determination.

### Action Items

- Collect proof of residency
- Verify household income
- Schedule eligibility review
- Notify applicant

### Required Documents

- Government-issued ID
- Proof of Address
- Income Verification

### Risk

Incomplete documentation may delay eligibility review.

### Recommended Next Steps

Review submitted documents and schedule applicant verification.

---

## Testing

Backend

```bash
pytest
```

Frontend

```bash
npm run lint

npm run build
```

Current project status:

- ✅ 114 backend tests passing
- ✅ ESLint passing
- ✅ TypeScript passing
- ✅ Production build passing

---

## Screenshots

The following screenshots will be added after deployment:

- Dashboard
- Workspace Management
- Project Management
- Document Upload
- AI Analysis Results

---

## Future Improvements

Potential future enhancements include:

- Support for multiple AI providers
- OCR support for scanned documents
- Enhanced PDF parsing
- Searchable document knowledge base
- Export analysis results to PDF
- Bulk document analysis
- Additional operational analysis templates

---

## License

This project is licensed under the MIT License.

---

## Author

**Mustak Eman**

Computer Science Student
Lehman College (CUNY)

GitHub
https://github.com/Mustak-Eman

LinkedIn
https://linkedin.com/in/mustak-eman-6517b2198
