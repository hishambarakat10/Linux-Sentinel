# LinuxSentinel
A lightweight RAG + Prompt Injection-Protected Chatbot for Linux Commands

Overview
Linux Sentinel is an intelligent chatbot designed to help users understand Linux commands easily and safely.
It reads commands and explanations from a trusted PDF, and uses Retrieval-Augmented Generation (RAG) combined with prompt injection defense to ensure accurate and secure answers.

The model retrieves the correct Linux command information based on user queries and blocks unrelated or malicious prompts, maintaining the chatbot's focus purely on Linux topics.

Features
📄 PDF Command Reader: Parses a PDF containing Linux commands and descriptions.

🧠 RAG Framework: Retrieves the most relevant command information for any user query.

🛡️ Prompt Injection Protection: Detects and prevents malicious or off-topic prompts.

⚡ Fast, Lightweight: Designed to run locally or in small VMs with minimal setup.

🐧 Linux-Focused: Only answers about Linux commands — nothing else.

How It Works
Extracts all commands and explanations from a Linux Commands PDF.

Embeds the extracted data into an internal retriever.

When a user asks a question, the system retrieves the best matching command(s).

The chatbot answers strictly based on the retrieved content, rejecting unrelated requests.
