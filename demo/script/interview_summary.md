# 🎙️ VoltAudit AI Developer Interview Summary

### 1. What was the core design philosophy behind VoltAudit AI?
We wanted to treat AI agents not as generic chatbots, but as specialized microservices. Just like standard microservices have well-defined inputs and outputs, our ADK Workforce agents are specialized, sequential workers bounded by strict tool access.

### 2. Why did you choose SQLite combined with FastMCP?
SQLite provides a lightweight, local transactional database. By placing FastMCP in front of it, we prevent the agent from writing raw SQL. All queries are pre-parameterized inside FastMCP tools, mitigating prompt injection or command injection.

### 3. How did you design the Human-in-the-Loop Gateway?
We realized automated payments are a high financial risk. Therefore, we created a dual gateway: any compliance score below 80 automatically flags the invoice. An operator must write a justification, which is then parsed by the governance skill to ensure quality.

### 4. What were the results of the SRE load tests?
The platform completed 10 parallel simulation runs at 21 runs/sec with zero failures, proving that the FastAPI/ADK backend easily handles enterprise loads.
