"""FastAPI server for MCP Broker with agentic workflow."""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import asyncio
from loguru import logger

from mcp_broker import (
    MCPBroker,
    MCPAgent,
    AgentRole,
    AgentTask,
    KnowledgeItem,
    TaskStatus,
)

# Initialize FastAPI app
app = FastAPI(
    title="MCP Broker API",
    description="Model Context Protocol Broker with Agentic Workflow for Enterprise KT",
    version="1.0.0",
)

# Initialize MCP Broker
broker = MCPBroker()


# Request/Response Models
class AgentRegistrationRequest(BaseModel):
    name: str
    role: AgentRole
    description: str
    capabilities: List[str]


class TaskCreationRequest(BaseModel):
    agent_id: str
    task_type: str
    description: str
    parameters: Dict[str, Any] = {}


class KnowledgeStorageRequest(BaseModel):
    title: str
    content: str
    source: str
    tags: Optional[List[str]] = None


class KnowledgeRetrievalRequest(BaseModel):
    query: str
    tags: Optional[List[str]] = None


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "broker_status": broker.get_status(),
    }


# Agent Management Endpoints
@app.post("/agents/register")
async def register_agent(request: AgentRegistrationRequest):
    """Register a new agent."""
    try:
        agent = await broker.register_agent(
            name=request.name,
            role=request.role,
            description=request.description,
            capabilities=request.capabilities,
        )
        return {
            "status": "success",
            "agent_id": agent.id,
            "agent": agent.dict(),
        }
    except Exception as e:
        logger.error(f"Error registering agent: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/agents")
async def list_agents():
    """List all registered agents."""
    agents = [
        agent.dict() for agent in broker.agents.values()
    ]
    return {
        "status": "success",
        "agents_count": len(agents),
        "agents": agents,
    }


# Task Management Endpoints
@app.post("/tasks/create")
async def create_task(request: TaskCreationRequest):
    """Create a new task."""
    try:
        task = await broker.create_task(
            agent_id=request.agent_id,
            task_type=request.task_type,
            description=request.description,
            parameters=request.parameters,
        )
        if task is None:
            raise HTTPException(status_code=404, detail="Agent not found")
        return {
            "status": "success",
            "task_id": task.id,
            "task": task.dict(),
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error creating task: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/tasks/{task_id}/execute")
async def execute_task(task_id: str, background_tasks: BackgroundTasks):
    """Execute a task."""
    try:
        if task_id not in broker.tasks:
            raise HTTPException(status_code=404, detail="Task not found")
        
        background_tasks.add_task(broker.execute_task, task_id)
        return {
            "status": "submitted",
            "task_id": task_id,
            "message": "Task execution started",
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error executing task: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/tasks")
async def list_tasks():
    """List all tasks."""
    tasks = [
        task.dict() for task in broker.tasks.values()
    ]
    return {
        "status": "success",
        "tasks_count": len(tasks),
        "tasks": tasks,
    }


# Knowledge Management Endpoints
@app.post("/knowledge/store")
async def store_knowledge(request: KnowledgeStorageRequest):
    """Store knowledge in the knowledge base."""
    try:
        item = await broker.store_knowledge(
            title=request.title,
            content=request.content,
            source=request.source,
            tags=request.tags,
        )
        return {
            "status": "success",
            "knowledge_id": item.id,
            "knowledge": item.dict(),
        }
    except Exception as e:
        logger.error(f"Error storing knowledge: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/knowledge/retrieve")
async def retrieve_knowledge(request: KnowledgeRetrievalRequest):
    """Retrieve knowledge from the knowledge base."""
    try:
        items = await broker.retrieve_knowledge(
            query=request.query,
            tags=request.tags,
        )
        return {
            "status": "success",
            "items_count": len(items),
            "knowledge": [item.dict() for item in items],
        }
    except Exception as e:
        logger.error(f"Error retrieving knowledge: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


# Status Endpoint
@app.get("/status")
async def get_status():
    """Get broker status."""
    return broker.get_status()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
