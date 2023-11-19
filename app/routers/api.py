from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import get_token_header
import app.crud as crud

router = APIRouter(
    prefix="/api",
    tags=["api"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.get("/costtypes/")
async def read_costtypes():
    costtypes = crud.fetch_all('costtypes', 'name')
    return costtypes

@router.get("/costtypes/{costtype_id}")
async def read_costtype(costtype_id: str):
    costtype = crud.fetch_one('costtypes', 'id', costtype_id)
    if costtype is None:
        raise HTTPException(status_code=404, detail="Costtype not found")
    return {"name": costtype["name"], "costtype_id": costtype['id']}

@router.get("/projects/")
async def read_projects():
    projects = crud.fetch_all('projects', 'name')
    return projects

@router.get("/projects/{project_id}")
async def read_project(project_id: str):
    project = crud.fetch_one('projects', 'id', project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"name": project["name"], "project_id": project['id']}

@router.get("/domains/")
async def read_domains():
    domains = crud.fetch_all('domains', 'name')
    return domains

@router.get("/domains/{domain_id}")
async def read_domain(domain_id: str):
    domain = crud.fetch_one('domains', 'id', domain_id)
    if domain is None:
        raise HTTPException(status_code=404, detail="Domain not found")
    return {"name": domain["name"], "domain_id": domain['id']}