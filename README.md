# Budgi Unstructured Service

Stateless PDF parsing microservice using Unstructured OSS.

## Endpoints

### Health
GET /healthz

### Parse PDF
POST /partition/pdf  
Headers:
- Authorization: Bearer <SERVICE_TOKEN>

Body:
- multipart/form-data
- file: PDF

## Notes
- No Budgi business logic
- No LLM usage
- VLM disabled (Phase 1)
