# Selenium Python Advanced Capstone — Notes App Automation

## Project Overview

This project is an end-to-end test automation framework for the Notes Application.  
It validates UI, API, and cross-layer synchronization while including parallel execution, reporting, CI/CD, and agentic automation techniques.

The framework is built to be scalable, stable, and industry-ready using modern QA best practices.


## Application Under Test

- UI: https://practice.expandtesting.com/notes/app  
- API: https://practice.expandtesting.com/notes/api/api-docs/

FINAL_PROJECT/
│
├── tests/ # Test cases (UI, API, E2E)
├── pages/ # Page Object Model (UI layer)
├── api/ # API client and endpoints
├── fixtures/ # WebDriver setup
├── utils/ # Utilities (waits, retry, logs)
├── config/ # Environment configuration
│
├── conftest.py # Pytest fixtures
├── pytest.ini # Pytest configuration
├── requirements.txt # Dependencies
├── Jenkinsfile # CI/CD pipeline

## Framework Architecture

---

## Testing Scope

### UI Testing
- Login validation (valid and invalid)
- Create note
- Delete note
- Empty input validation
- Instant UI update verification

### API Testing
- Authentication
- Get all notes
- Create note
- Delete note
- Response validation

### End-to-End Testing
- UI → API synchronization (data persistence)
- API → UI synchronization (create and delete)

### Non-Functional Testing
- API performance validation (< 2 seconds)

---

## Test Suite Coverage

- UI Tests ✔  
- API Tests ✔  
- E2E Tests ✔  
- Negative Tests ✔  
- Performance Tests ✔  

---

## Setup and Execution

### Clone Repository
git clone https://github.com/LahariMaredi/Notes-Testing-App.git

cd FINAL_PROJECT

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

### Run Tests (Serial)
pytest -v --html=report.html --self-contained-html


### Run Tests (Parallel)
pytest -n 4 --alluredir=allure-results

---
## Reporting

### Pytest HTML Report
pytest --html=report.html
### Allure Report
pytest --alluredir=allure-results
allure serve allure-results


Reports include:
- Execution summary  
- Step-level visibility  
- Failure diagnostics  
- API logs and attachments  

---

## CI/CD Integration (Jenkins)

### Pipeline Stages
1. Checkout source code  
2. Setup Python environment  
3. Install dependencies  
4. Execute tests in parallel  
5. Generate HTML and Allure reports  
6. Archive reports and logs  

Execution is automated through Jenkins pipeline.

---

## Parallel Execution
pytest -n 4

- Reduces execution time  
- Improves resource usage  
- Enables scalable test runs  

---

## Agentic Automation Enhancements

### Self-Healing Locators
Fallback locator strategy to handle DOM changes

### Auto-Retry Mechanism
pytest --reruns 2 --reruns-delay 2


Handles flaky UI failures

### Intelligent Waiting
Explicit waits with safe interaction methods (no hardcoded delays)

### Decision-Based Rerun Logic
Differentiates transient failures from real defects

---

## Key Design Principles

- Stable locators using `data-testid`  
- Page Object Model for maintainability  
- Clear separation of UI and API layers  
- Reusable utilities and fixtures  
- Scalable test architecture  

---

## Results

- All test cases passing  
- Stable execution with retry handling  
- Parallel execution implemented  
- CI/CD pipeline working  
- Detailed reporting available  

---

## Conclusion

This framework represents a complete automation lifecycle including requirement validation, UI and API automation, cross-layer consistency checks, performance validation, CI/CD integration, and resilient automation design.

It follows a production-ready QA approach focused on reliability, scalability, and maintainability.