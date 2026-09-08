# LLM Integration Plan (Claude)

## Decision
- Primary model provider: Anthropic Claude
- Reason: paper alignment with Claude/MCP agent ecosystem
- Initial model: latest Sonnet-class model available to the account

## Auth
- Environment variable: `ANTHROPIC_API_KEY`
- Do not hardcode keys in source code
- Do not commit keys to git

## Architecture
1. Convert local ToolRegistry tools into Claude tool schemas
2. Send user message + system prompt + tools to Claude Messages API
3. If model returns `tool_use`, execute tool via ToolRegistry
4. Send `tool_result` back to Claude
5. Repeat until final text answer

## Injection Points
- system_message: modify system prompt before request
- tool_output: modify tool result before returning to Claude
- retrieved_document: modify document/search payloads
- intermediate_message: insert message between tool result and next model call

## Deliverables
- `agent/tool_schema.py`
- `agent/llm_agent.py`
- ScenarioRunner integration
- Control/Treatment verification logs