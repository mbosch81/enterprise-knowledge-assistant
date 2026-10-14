# Five-minute demo

1. Follow the local setup instructions in the README. State that the baseline uses an offline provider and synthetic documents.
2. Ask `How many annual leave days?` Show the answer containing 30 days, the original quote, and the chunk ID.
3. Ask `What is the CEO salary?` Show that the application declines to answer because evidence is missing.
4. Try an invalid bearer token and a request containing a client-supplied tenant ID. Show that authentication or request validation rejects them.
5. Run the tests and offline evaluation. Explain what they verify and the limits of the small dataset.

The optional Ollama run demonstrates model-assisted selection of verified quotes. It does not yet demonstrate semantic retrieval or autonomous task planning.

## Project motivation and learning goals

This personal project is driven by curiosity about AI applications and a desire to extend my experience with Python, APIs, and deployment into retrieval-augmented generation (RAG), evaluation, and bounded agent workflows.

I want to understand the individual components, develop them step by step, and investigate their strengths and limitations through reproducible tests. The offline baseline supports deterministic tests without model calls. Building on it, I will explore local models, semantic search, access control, and the tradeoffs between quality, cost, and latency.
