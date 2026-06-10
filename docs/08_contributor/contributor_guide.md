# Contributor Guide

## Welcome

This project is focused on safe, compute-aware local AI systems for consumer hardware.

## Contributor Areas

### AI Benchmarking

Skills:

- Python
- Ollama
- llama.cpp
- Hugging Face
- PyTorch
- pandas
- matplotlib

Tasks:

- Run benchmarks
- Test models
- Record results
- Validate datasets

### Linux Systems

Skills:

- Linux
- Bash
- systemd
- Docker
- package managers

Tasks:

- Build local AI assistant prototype
- Test system commands
- Create setup scripts

### Security

Skills:

- Linux permissions
- sudoers
- AppArmor
- SELinux
- threat modeling

Tasks:

- Build privilege broker
- Create risk classifier
- Test unsafe commands
- Improve safety policy

### Backend

Skills:

- Python
- Go
- FastAPI
- SQLite
- REST APIs

Tasks:

- Build APIs
- Connect benchmark, assistant, broker, and logs

### Research Writing

Skills:

- Academic writing
- LaTeX
- literature review
- experiment design

Tasks:

- Write papers
- Create figures
- Edit methodology
- Prepare submissions

## Contribution Rules

1. Do not add unsafe code.
2. Do not bypass permissions.
3. Do not hide command execution.
4. Document all experiments.
5. Include hardware and software versions.
6. Avoid exaggerated claims.
7. Keep results reproducible.
8. Use pull requests for major changes.

## First Good Issues

- Add more prompts to `prompts.json`
- Test benchmark runner on another machine
- Improve CSV schema
- Add GPU tracking
- Add graph generation
- Add risk rules to broker policy
- Improve README
