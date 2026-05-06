# Allure Integration & Reporting Guide

## Overview

This document outlines the complete Allure integration for automated testing with Selenium and pytest.

---

## ✅ Grid Items Covered

### 1. **Reporting** ✓

- **Allure Reports**: Comprehensive test execution reports with features, stories, and steps
- **HTML Reports**: pytest-html plugin for detailed HTML reports
- **Environment Properties**: `allure-results/environment.properties` with test environment metadata
- **Metadata**: Python version, OS, browser, test framework, and environment captured

### 2. **Automatic Screenshot Capture** ✓

- **Failure Screenshots**: Automatic screenshots on test failure via `pytest_runtest_makereport` hook
- **Manual Screenshots**: Screenshot attachment in Allure report via `attach_screenshot_to_allure()`
- **Screenshot Storage**: Organized in `screenshots/` directory with timestamps
- **Allure Attachment**: Screenshots attached with metadata to Allure reports

### 3. **Logging** ✓

- **File Logging**: Centralized logging to `logs/test_execution_*.log`
- **Console Logging**: Real-time log output during test execution
- **Structured Format**: Timestamp, logger name, level, and message
- **Log Levels**: DEBUG for file, INFO for console
- **Session Logging**: Test session start/end logging

---

## 📁 File Structure

```
FINAL_PROJECT/
├── conftest.py                          # Pytest configuration with hooks
├── pytest.ini                           # Pytest configuration for Allure
├── requirements.txt                     # Dependencies (allure-pytest included)
├── allure-results/                      # Allure report data
│   └── environment.properties           # Environment metadata
├── logs/                                # Test execution logs
│   └── test_execution_*.log
├── screenshots/                         # Failure screenshots
│   └── test_name_timestamp.png
├── tests/
│   ├── test_login.py                   # UI Login with Allure steps & screenshots
│   ├── test_notes_api.py               # API with Allure attachments (JSON)
│   ├── test_delete_note.py             # API delete with Allure steps & responses
│   ├── test_e2e.py                     # End-to-end with screenshots & API responses
│   └── ...other tests
├── utils/
│   ├── screenshot.py                   # Screenshot utility with Allure integration
│   ├── logger.py                       # Logging setup and configuration
│   └── wait_utils.py
└── pages/                               # Page objects
```

---

## 🔧 Core Components

### 1. **conftest.py** - Test Configuration & Hooks

```python
# Features:
- pytest_runtest_makereport: Captures screenshots on test failure
- Allure attachment: Failure screenshots attached with metadata
- Session logging: Test session lifecycle logging
- api_client fixture: Pre-authenticated API client
```

**Key Hook:**

```python
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Captures screenshot on failure
    # Attaches to Allure report
```

### 2. **utils/screenshot.py** - Screenshot Management

```python
Functions:
- take_screenshot(): Save screenshot with timestamp
- attach_screenshot_to_allure(): Attach screenshot to Allure report
```

### 3. **utils/logger.py** - Logging Configuration

```python
Functions:
- setup_logger(): Configure file and console handlers
Features:
- Structured logging format
- File and console output
- DEBUG level for file, INFO for console
```

### 4. **pytest.ini** - Pytest Configuration

```ini
[pytest]
addopts = -v --alluredir=allure-results --html=report.html --self-contained-html
testpaths = tests
log_cli = true
log_cli_level = INFO
log_file = logs/pytest.log
log_file_level = DEBUG
```

### 5. **allure-results/environment.properties** - Test Environment Metadata

```properties
Browser=Chrome
OS=Windows 11
Python=3.13.3
Pytest=9.0.3
Environment=QA
Framework=Pytest
```

---

## 📊 Test Examples with Allure Integration

### Example 1: UI Test with Screenshots

```python
@allure.feature("Authentication")
@allure.story("User Login")
def test_login(driver):
    with allure.step("Open login page"):
        login.open(config["base_url"])
        attach_screenshot_to_allure(driver, "Login Page")

    with allure.step("Login with credentials"):
        login.login(config["email"], config["password"])
        attach_screenshot_to_allure(driver, "After Login")
```

### Example 2: API Test with Response Attachments

```python
@allure.feature("Notes API")
def test_api_notes():
    with allure.step("Login via API"):
        res = api.login()
        allure.attach(str(res.json()), name="Login Response",
                     attachment_type=allure.attachment_type.JSON)
```

### Example 3: End-to-End with UI + API + Screenshots

```python
@allure.feature("End-to-End")
def test_ui_api_flow(driver):
    with allure.step("Create note via UI"):
        notes.create_note(title, "description")
        attach_screenshot_to_allure(driver, "Note Created")

    with allure.step("Verify via API"):
        response = api.get_notes().json()
        allure.attach(str(response), name="API Response",
                     attachment_type=allure.attachment_type.JSON)
```

---

## 🚀 Running Tests with Allure

### Basic Execution

```bash
pytest -v
```

### With Allure Report Generation

```bash
pytest -n 4 --alluredir=allure-results --html=report.html
```

### View Allure Report (requires allure-commandline)

```bash
allure serve allure-results
```

### View HTML Report

```bash
# Open report.html in browser
start report.html
```

---

## 📋 Allure Report Features

### 1. **Features & Stories**

- Tests organized by feature and story
- Hierarchical test structure
- Clear test categorization

### 2. **Steps**

- Test execution steps shown with timing
- Nested steps for complex workflows
- Step pass/fail status

### 3. **Attachments**

- **Screenshots**: Failure screenshots + manual attachments
- **API Responses**: JSON/TEXT attachments
- **Logs**: Test execution logs
- **Custom Data**: Any file or text data

### 4. **Timeline**

- Test execution timeline
- Duration per step
- Overall test duration

### 5. **Trends**

- Historical test trends
- Pass/fail rate tracking
- Performance analysis

### 6. **Environment Info**

- Browser: Chrome
- OS: Windows 11
- Python: 3.13.3
- Framework: Pytest + Selenium

---

## 📝 Logging Output

### File Log Location

`logs/test_execution_YYYYMMDD_HHMMSS.log`

### Console Output

```
2024-01-15 10:30:45 - test_login - INFO - Test started
2024-01-15 10:30:46 - test_login - DEBUG - Opening login page
2024-01-15 10:30:47 - test_login - DEBUG - Entering credentials
2024-01-15 10:30:48 - test_login - INFO - Login successful
```

---

## 🛠️ Customization Options

### Add Custom Allure Markers

```python
@allure.feature("Custom Feature")
@allure.story("Custom Story")
@allure.severity(allure.severity_level.CRITICAL)
def test_critical_feature():
    pass
```

### Add Custom Attachments

```python
allure.attach("custom data", name="Custom Name",
             attachment_type=allure.attachment_type.TEXT)
```

### Add Description

```python
@allure.description("This is a detailed test description")
def test_example():
    pass
```

---

## ✅ Grid Items Verification

| Item                         | Status | Implementation                   |
| ---------------------------- | ------ | -------------------------------- |
| Reporting                    | ✅     | Allure + HTML Reports            |
| Automatic Screenshot Capture | ✅     | pytest hook + Utils              |
| Logging                      | ✅     | Centralized to files + console   |
| Attachments                  | ✅     | Screenshots, logs, API responses |
| Environment Properties       | ✅     | environment.properties           |
| Test Organization            | ✅     | Features, stories, steps         |
| Performance Tracking         | ✅     | Step timing + duration           |

---

## 🎯 Best Practices

1. **Use Allure Features & Stories** for clear test organization
2. **Add Steps** for complex workflows
3. **Attach Screenshots** at key UI interactions
4. **Attach API Responses** for debugging
5. **Use Severity Markers** for test prioritization
6. **Keep Logs Organized** with consistent naming
7. **Review Reports Regularly** for trends and patterns

---

## 🔗 References

- [Allure Framework](https://docs.qameta.io/allure/)
- [allure-pytest Plugin](https://docs.qameta.io/allure-pytest/)
- [pytest Documentation](https://docs.pytest.org/)
- [Selenium Documentation](https://selenium.dev/)
