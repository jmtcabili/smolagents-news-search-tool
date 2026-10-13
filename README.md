---
title: First Agent Template
emoji: ⚡
colorFrom: pink
colorTo: yellow
sdk: gradio
sdk_version: 5.23.1
app_file: app.py
pinned: false
tags:
- smolagents
- agent
- smolagent
- tool
- agent-course
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

# AI News Agent (Prototype)

A prototype AI agent powered by Google Gemini and Hugging Face's [`smolagents`](https://github.com/huggingface/smolagents), based on the template from the **[Hugging Face Agents Course](https://huggingface.co/learn/agents-course)**.

## Overview

The agent is implemented as a `CodeAgent` with a Gradio UI interface. It uses Google Gemini (via `LiteLLMModel`) to reason through tasks, run Python code snippets, and call custom tools.

### What's Added: `news_search` Tool

In addition to the default tools from the course template (`final_answer`, `web_search`, and `visit_webpage`), this prototype adds a custom **`news_search`** tool:

- **Targeted Multi-Outlet RSS Search:** Collects recent articles on tech and AI companies (such as Anthropic, OpenAI, or Google) across selected outlets (e.g. *The Guardian*, *TechCrunch*, *The Verge*, *Ars Technica*, *CNBC*).
- **URL Decoding & Content Extraction:** Resolves Google News RSS links and uses clean web extraction (`trafilatura`) to filter out navigation menus, ads, and boilerplate.
- **Resilient Fallback:** Gracefully falls back to headline snippets when articles are behind strict paywalls or bot protection.
- **Structured Synthesis:** The agent analyzes the returned article text and generates a 3-bullet point summary per article.

## Getting Started

1. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   Create a `.env` file in the root directory:
   ```env
   GEMINI_KEY=your_gemini_api_key
   ```

3. **Run the agent:**
   ```bash
   python app.py
   ```
