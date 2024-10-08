# Project Overview
it's flask based social media platform

## Frameworks to be used
These are the mandatory frameworks on which the project has to be built.
 - Flask for application code
 - Jinja2 templates + Bootstrap for HTML generation and styling
 - SQLite for data storage

# Project Setup

This guide covers the setup for the complete development environment including flask and all the flask libraries used.

## Prerequisites

Ensure you have Python installed on your machine.

## Installation Steps

First, clone the repository to your local machine and navigate into the project directory.

### Create a virtual environment
#### for macOS/Linux
```bash
python3 -m venv .venv
```
#### for Windows
```bash
py -3 -m venv .venv
```
Produat Engineer

Product Engineer
### Activate the virtual environment
#### for macOS/Linux
```bash
.venv/bin/activate
```
#### for Windows
```bash
.venv\Scripts\activate
```

### Install the dependencies
```bash
pip install -r requirements.txt
```

### Run the Flask application
```bash
py run.py
```