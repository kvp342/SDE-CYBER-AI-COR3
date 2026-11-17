# AI

[All categories](README.md) · 2 topics

## Topics

- [LLMs and RAG apps](#llms-and-rag-apps)
- [Prompt injection and AI security](#prompt-injection-and-ai-security)

## LLMs and RAG apps

*Level 2: Interview-ready*

Your 4-week AI-security project in May (1 hour a day): build a RAG assistant, then attack and defend it. An AI + security project is a rare combination on a fresher resume.

**Key idea**

An LLM predicts the next token from a prompt; it knows only its training data and what you put in the context window.

RAG (retrieval-augmented generation): split documents into chunks, embed them as vectors, store them in a vector index; at question time, embed the question, retrieve the closest chunks and put them in the prompt so the answer is grounded in your data.

Tool calling lets the model request a function (search, database query) that your code runs. Evals: a fixed set of questions with expected answers to measure changes.


**Points**

- Chunk size and overlap matter more than the model
- Always cite retrieved sources in answers
- Evaluate before and after every change

**Traps**

- No evaluation set
- Putting secrets in prompts

**Interviewers ask**

- How does RAG work?
- How would you evaluate an LLM feature?

**Learn more**

- [DeepLearning.AI short courses (free)](https://www.deeplearning.ai/short-courses/)
- [Anthropic docs](https://docs.anthropic.com)

**Related:** [Prompt injection and AI security](#prompt-injection-and-ai-security)

[Back to the topic list](#topics)

## Prompt injection and AI security

*Level 3: Advanced*

Where your AI and cyber tracks meet. Few freshers can talk about it.

**Key idea**

Prompt injection: untrusted text (a web page, an email, a document in your RAG store) contains instructions that the model follows instead of the developer's. Direct injection comes from the user; indirect injection hides in retrieved content.

Risks grow with tools: an injected instruction can make an agent leak data or take actions. Defences: treat model output as untrusted, least-privilege tools, human confirmation for risky actions, separate trusted instructions from data, output filtering, and red-team tests.

The OWASP Top 10 for LLM applications lists prompt injection, sensitive information disclosure, supply chain, data poisoning, improper output handling, excessive agency and more.


**Points**

- Build a test set of injection attempts for your RAG project
- Log and monitor model actions

**Traps**

- Believing a system prompt alone stops injection

**Interviewers ask**

- What is prompt injection and how would you mitigate it?

**Learn more**

- [OWASP LLM Top 10](https://genai.owasp.org/llm-top-10/)
- [Gandalf (Lakera) prompt-injection game](https://gandalf.lakera.ai)

**Related:** [LLMs and RAG apps](#llms-and-rag-apps) · [OWASP Top 10](security.md#owasp-top-10)

[Back to the topic list](#topics)
