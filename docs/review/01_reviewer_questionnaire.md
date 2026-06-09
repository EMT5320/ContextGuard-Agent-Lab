# Reviewer Questionnaire

## A. Positioning

1. Can you summarize the revised project in one sentence after reading the docs?
2. Does the project look like an Agent strategy benchmark, an eval project, a RAG project, a protocol project, or a safety project?
3. Which target role does it best support?
4. Which target role does it fail to support?
5. Does it clearly avoid Loomstead's Agent Behavior Observatory story?

## B. Differentiation

1. What makes this different from a normal RAG demo?
2. What makes this different from a guardrail framework sample?
3. What makes this different from Loomstead's trace / audit portfolio story?
4. Is MCP-compatible essential to the architecture, or just a packaging label?
5. Is context budget strong enough as a strategy signal?

## C. Technical Feasibility

1. Which module is likely to consume the most time?
2. Which module can be implemented deterministically before hosted LLM integration?
3. Which module requires external API or model dependency?
4. What should be mocked first?
5. What should be implemented before FastMCP adapter work starts?

## D. Eval Validity

1. Are the metrics aligned with the claims?
2. Which metric can be gamed?
3. Which case family needs richer data?
4. What bad cases should be mandatory?
5. How many cases are enough for a convincing MVP if they are high quality?

## E. Scope Control

1. What is the smallest impressive MVP?
2. What should be cut from W1/W2?
3. What should remain stretch only?
4. What would trigger a pivot?
5. Should coding fixture be included at all, given Loomstead's secondary coding evidence?

## F. Interview Value

1. What questions would an interviewer ask about this project?
2. What evidence should be visible in README?
3. Which architecture diagram is needed?
4. Which case card should be first?
5. Would this project help more for Agent algorithm roles or Agent engineering roles?
