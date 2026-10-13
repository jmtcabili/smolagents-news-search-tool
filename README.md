# 📰 smolagents-news-search-tool

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white" alt="Python"></a>
  <a href="https://github.com/huggingface/smolagents"><img src="https://img.shields.io/badge/smolagents-1.13.0-yellow?logo=huggingface&logoColor=white" alt="smolagents"></a>
  <a href="https://aistudio.google.com/"><img src="https://img.shields.io/badge/Google_Gemini-2.5_Flash-4285F4?logo=google&logoColor=white" alt="Google Gemini"></a>
  <a href="https://gradio.app/"><img src="https://img.shields.io/badge/UI-Gradio_5-orange?logo=gradio&logoColor=white" alt="Gradio"></a>
  <a href="https://huggingface.co/learn/agents-course"><img src="https://img.shields.io/badge/HF_Course-Agents-yellow?logo=huggingface&logoColor=white" alt="HF Course"></a>
</p>

---

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
