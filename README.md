# mcp-broker-agentic-workflow
MCP Broker with Agentic Workflow for Enterprise Knowledge Transfer - A comprehensive system for building intelligent model context protocol brokers with autonomous agents for seamless enterprise knowledge management and transfer.


## Features

- **MCP Broker Core**: Robust Model Context Protocol broker implementation with async support
- **Agent Management**: Dynamic registration and management of autonomous agents with role-based access
- **Task Execution**: Asynchronous task processing with retry logic and error handling
- **Knowledge Management**: Enterprise-grade knowledge base with search and tagging capabilities
- **FastAPI Integration**: High-performance REST API for seamless integration
- **Enterprise KT**: Specialized workflows for enterprise knowledge transfer
- **Scalability**: Built for enterprise-scale deployments with configurable resource limits
- **Monitoring**: Built-in logging and status endpoints for operational visibility

## Architecture

```
┌─────────────────────────────────────────────────────┐
│           FastAPI Server (api_server.py)            │
│  ├─ /agents/* (Agent Management)                    │
│  ├─ /tasks/* (Task Management)                      │
│  ├─ /knowledge/* (Knowledge Management)             │
│  └─ /status (Broker Status)                         │
└────────────────┬────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────┐
│      MCPBroker Core (mcp_broker.py)                 │
│  ├─ Agent Registry                                  │
│  ├─ Task Queue                                      │
│  ├─ Knowledge Base                                  │
│  └─ Workflow Engine                                 │
└─────────────────────────────────────────────────────┘
```

## Installation

```bash
# Clone the repository
git clone https://github.com/KiruthikaPalanivelu/mcp-broker-agentic-workflow.git
cd mcp-broker-agentic-workflow

# Install dependencies
pip install -r requirements.txt

# Run the server
python -m src.api_server
```

## Configuration

Edit `config.yaml` to customize:
- Server settings (host, port, workers)
- Broker configuration (max agents, tasks, knowledge retention)
- Agent scaling policies
- Task execution parameters
- Knowledge base settings
- Security and monitoring options

## Usage Examples

### Register an Agent
```bash
curl -X POST http://localhost:8000/agents/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "DocumentProcessor",
    "role": "executor",
    "description": "Processes enterprise documents",
    "capabilities": ["parse", "extract", "validate"]
  }'
```

### Create and Execute a Task
```bash
curl -X POST http://localhost:8000/tasks/create \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "<agent_id>",
    "task_type": "document_processing",
    "description": "Process Q4 reports",
    "parameters": {"format": "pdf", "extract_tables": true}
  }'
```

### Store Knowledge
```bash
curl -X POST http://localhost:8000/knowledge/store \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Enterprise Best Practices",
    "content": "...",
    "source": "internal_wiki",
    "tags": ["enterprise", "best-practices"]
  }'
```

## Enterprise Knowledge Transfer (KT)

This system is specifically designed for enterprise knowledge transfer scenarios:

1. **Knowledge Capture**: Automated collection of domain expertise and processes
2. **Agent-Based Processing**: Intelligent agents handle different aspects of KT workflows
3. **Scalable Distribution**: Distribute knowledge across organization with configurable workflows
4. **Quality Assurance**: Built-in validation and verification agents
5. **Continuous Learning**: Knowledge base continuously updates with new insights

## API Endpoints

### Health & Status
- `GET /health` - Health check
- `GET /status` - Broker status

### Agent Management
- `POST /agents/register` - Register new agent
- `GET /agents` - List all agents

### Task Management
- `POST /tasks/create` - Create task
- `POST /tasks/{task_id}/execute` - Execute task
- `GET /tasks` - List all tasks

### Knowledge Management
- `POST /knowledge/store` - Store knowledge item
- `POST /knowledge/retrieve` - Retrieve knowledge items

## Development

```bash
# Run with auto-reload
uvicorn src.api_server:app --reload

# View API documentation
# Navigate to http://localhost:8000/docs
```

## Contributing

Contributions are welcome! Please follow the project guidelines and submit pull requests.

## License

MIT License

## Support

For issues and questions, please open an issue on the GitHub repository.
