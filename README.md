---
title: First Agent Template
emoji: ⚡
colorFrom: pink
colorTo: yellow
sdk: gradio
sdk_version: 5.15.0
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

# Huggingface Agents Course

This repository started as a clone of the Huggingface space for their AI Agents course. Initial changes were to reconfigure the CodeAgent to use an OpenAI model to avoid the monthly quota on the Huggingface direct inference. You will need to use an environment variable for "OPENAI_API_KEY" and ensure that the associated OpenAI project has access to the model specified for the LiteLLMModel.