# Proactive Context-Awareness Personal AI

> A privacy-first AI agent that maintains persistent awareness of your digital life and proactively provides insights, warnings, and assistance without being asked.

## Overview

This project reimagines the personal AI assistant paradigm. Instead of a reactive Q&A chatbot that forgets everything between sessions, this system creates a **continuous, privacy-respecting memory** of your goals, projects, and habits to act as a true digital partner.

### The Problem

Current AI assistants are context-agnostic and stateless. They:
- Forget everything between conversations
- Require you to manually provide context every time
- Wait for you to ask questions instead of anticipating needs
- Have no awareness of your ongoing projects and commitments

### The Solution

A proactive AI agent that:
- **Maintains persistent context** across all your digital tools
- **Anticipates your needs** based on patterns and upcoming events
- **Provides timely interventions** without being prompted
- **Learns from feedback** to improve its usefulness over time
- **Respects your privacy** with local-first, encrypted architecture

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Data Sources  │    │   MCP Servers    │    │  Core AI Agent  │
│                 │    │                  │    │                 │
│  • Gmail        │◄──►│  • mcp-gmail     │◄──►│  • Context      │
│  • Calendar     │    │  • mcp-calendar  │    │    Engine       │
│  • Notion       │    │  • mcp-notion    │    │  • Alert System │
│  • Slack        │    │  • mcp-slack     │    │  • ML Models    │
│  • Health APIs  │    │  • mcp-health    │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │  Vector DB &    │
                       │  Memory System  │
                       └─────────────────┘
```

### Core Components

1. **MCP (Model Context Protocol) Servers**: Secure, permission-scoped connectors to your data sources
2. **Context Engine**: Continuously processes data streams and maintains a dynamic "state of the user"
3. **Vector Memory**: ChromaDB-based semantic search over your digital activity history
4. **Alert Triage System**: ML-powered filter that learns what constitutes a useful intervention
5. **Proactive Agent**: Orchestrates all components and delivers timely insights

## Key Features

### Proactive Interventions

**Meeting Intelligence**
```
"You have a meeting with Acme Corp in 30 minutes. Your last email to them 
was about Q4 pricing, and the attached proposal document you're working on 
hasn't been saved in 2 hours. Would you like to open it?"
```

**Project Continuity**
```
"I've noticed three emails from different team members about 'Project Phoenix' 
this week, but it's not on your official project list in Notion. Should I 
create a summary page?"
```

**Wellness Monitoring**
```
"Your screen time and calendar stress metrics have been high this week. 
I've blocked a 1-hour 'focus time' slot for you tomorrow afternoon."
```

### Technical Innovations

- **Continuous Learning Pipeline**: Ingests data from MCP streams, updates vector database, and generates intelligent compressed summaries
- **Causal Inference**: ML model learns meaningful correlations vs. noise, with feedback loop for self-improvement
- **Privacy-First Design**: Runs on-premise or with E2E encryption; MCP's permission model ensures data isolation
- **Smart Polling**: Adaptive polling intervals based on data source update patterns
- **Semantic Context Matching**: Vector embeddings for cross-source relationship discovery

## Getting Started

### Prerequisites

- Python 3.10+
- Docker & Docker Compose
- API credentials for your data sources (Gmail, Calendar, etc.)
- 8GB+ RAM recommended

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/proactive-ai.git
cd proactive-ai
```

2. **Set up the project structure**
```bash
mkdir -p core-agent/src/{context_engine,alert_system,memory,models}
mkdir -p mcp-servers/{gmail,calendar,notion,slack,shared}
mkdir -p frontend data config
```

3. **Install core dependencies**
```bash
cd core-agent
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your API keys and credentials
```

5. **Set up data source credentials**
```bash
# Place your OAuth credentials in config/
# - gmail_credentials.json
# - calendar_credentials.json
# - notion_token.txt
```

6. **Launch with Docker Compose**
```bash
docker-compose up -d
```

### Quick Test

Run a minimal test to verify setup:

```bash
python core-agent/src/test_setup.py
```

This will:
- Initialize the vector database
- Create a mock MCP server
- Test context extraction
- Verify alert generation

## Project Structure

```
proactive-ai/
├── core-agent/                 # Main AI agent
│   ├── src/
│   │   ├── context_engine/     # Context processing and extraction
│   │   │   └── engine.py
│   │   ├── alert_system/       # Alert generation and triage
│   │   │   └── triage.py
│   │   ├── memory/             # Vector database interface
│   │   │   └── vector_store.py
│   │   ├── models/             # ML models for prediction
│   │   └── main_agent.py       # Main orchestration loop
│   └── requirements.txt
├── mcp-servers/                # MCP server implementations
│   ├── shared/
│   │   └── base_server.py      # Base MCP server class
│   ├── gmail/                  # Gmail integration
│   ├── calendar/               # Calendar integration
│   ├── notion/                 # Notion integration
│   └── slack/                  # Slack integration
├── frontend/                   # Web interface (optional)
├── data/                       # Local data storage
├── config/                     # Credentials and config files
├── docker-compose.yml
└── README.md
```

## 🔧 Configuration

### MCP Server Configuration

Each MCP server is configured via `config/mcp_config.json`:

```json
{
  "servers": {
    "gmail": {
      "enabled": true,
      "poll_interval": 300,
      "credentials_path": "config/gmail_credentials.json"
    },
    "calendar": {
      "enabled": true,
      "poll_interval": 600,
      "credentials_path": "config/calendar_credentials.json"
    }
  }
}
```

### Alert System Configuration

Adjust alert thresholds in `config/alerts_config.json`:

```json
{
  "meeting_reminder_minutes": 30,
  "min_alert_confidence": 0.7,
  "working_hours": {
    "start": "09:00",
    "end": "18:00"
  },
  "alert_cooldown_minutes": 60
}
```

## How It Works

### 1. Data Collection

MCP servers continuously poll your data sources:
- **Calendar**: Upcoming meetings, schedule changes
- **Gmail**: New emails, threads, attachments
- **Notion**: Project updates, task changes
- **Slack**: Team communications, mentions

### 2. Context Extraction

The Context Engine processes raw data into semantic entities:
- Identifies meetings, projects, tasks, communications
- Calculates importance scores
- Discovers relationships between entities
- Generates vector embeddings for semantic search

### 3. Memory Storage

Entities are stored in ChromaDB for fast semantic retrieval:
- Vector embeddings enable "meaning-based" search
- Metadata allows filtering by time, importance, type
- Compressed summaries keep context window manageable

### 4. Alert Generation

The system identifies actionable patterns:
- Upcoming meetings with unsaved related documents
- Project mentions not tracked in task manager
- Communication patterns suggesting stress or overload
- Schedule conflicts or double-bookings

### 5. Alert Triage

ML model filters alerts to prevent notification fatigue:
- Initial rule-based approach (working hours, priority thresholds)
- Learns from user feedback (dismissals, actions taken)
- Retrains periodically as feedback accumulates
- Adapts to individual preferences and work patterns

### 6. Proactive Delivery

Validated alerts are delivered via:
- Desktop notifications
- Web dashboard
- Mobile app (optional)
- Daily digest emails

## Privacy & Security

This project is designed with privacy as a core principle:

### Local-First Architecture
- All processing happens on your machine or private server
- No data sent to external AI providers (use local LLMs via Ollama)
- ChromaDB runs locally with encrypted storage

### MCP Permission Model
- Each MCP server has scoped access to only its data source
- Gmail server cannot access your health data
- Calendar server cannot read your emails
- Explicit consent required for each data source

### Data Encryption
- All credentials stored encrypted at rest
- Optional E2E encryption for database
- Secure token management for OAuth flows

### Data Retention
- Configurable retention policies (default: 90 days)
- Automatic pruning of old context data
- User-controlled data deletion

## Roadmap

### Phase 1: Foundation (Weeks 1-4)
- [x] Project structure setup
- [x] Basic MCP server implementation
- [x] Vector database integration
- [ ] Calendar & Gmail integration
- [ ] Simple rule-based alerts

### Phase 2: Intelligence (Weeks 5-8)
- [ ] Context Engine with entity extraction
- [ ] Cross-source relationship discovery
- [ ] Alert triage ML model
- [ ] Feedback collection system

### Phase 3: Expansion (Weeks 9-12)
- [ ] Notion integration
- [ ] Slack integration
- [ ] Health API integration
- [ ] Web dashboard UI

### Phase 4: Optimization (Weeks 13-16)
- [ ] Performance tuning
- [ ] ML model improvements
- [ ] Mobile app (optional)
- [ ] Advanced personalization

## Contributing

Contributions are welcome! This project is ambitious and benefits from diverse perspectives.

### Areas for Contribution
- Additional MCP server implementations (GitHub, Todoist, etc.)
- ML model improvements for alert triage
- Privacy-preserving techniques
- UI/UX for the dashboard
- Documentation and examples

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Commit: `git commit -m 'Add amazing feature'`
5. Push: `git push origin feature/amazing-feature`
6. Open a Pull Request

## Performance Considerations

### Resource Usage
- **Memory**: ~2-4GB for vector database and models
- **CPU**: Minimal when idle; spikes during context processing
- **Storage**: ~100MB per month of context data (varies by usage)

### Optimization Tips
- Adjust poll intervals based on data source update frequency
- Use smaller embedding models for faster processing
- Implement incremental updates instead of full scans
- Cache frequently accessed context entities

## Troubleshooting

### Common Issues

**MCP Server Connection Failures**
```bash
# Check server logs
docker-compose logs mcp-calendar

# Verify credentials
cat config/calendar_credentials.json
```

**Vector Database Slow Queries**
```bash
# Rebuild index
python core-agent/src/memory/rebuild_index.py
```

**Too Many/Few Alerts**
- Adjust `min_alert_confidence` in alerts_config.json
- Provide more feedback to improve ML model
- Check working hours configuration

## Further Reading

- [MCP Protocol Specification](https://spec.modelcontextprotocol.io/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Prompt Engineering for Context Management](https://docs.anthropic.com/claude/docs/prompt-engineering)
- [Building Privacy-Preserving AI Systems](https://arxiv.org/abs/2103.00001)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by research in context-aware computing and proactive AI
- Built on the Model Context Protocol (MCP)
- Uses ChromaDB for vector storage
- Leverages sentence-transformers for embeddings

---

**Note**: This is an experimental project exploring the boundaries of proactive AI assistance. Always review and validate any actions suggested by the system before executing them.