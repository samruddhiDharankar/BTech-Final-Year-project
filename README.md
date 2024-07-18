# BTech Final Year Project

A web application designed to manage and analyze digital evidence for forensic purposes.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Features](#features)
- [Technologies Used](#technologies-used)
  
## Installation

### Prerequisites
- Python
- pip

### Steps
1. Install Flask:
    ```sh
    pip install flask
    ```
2. Install MySQL:
    ```sh
    pip install flask-mysqldb
    ```
3. Navigate to the project directory.
4. Set environment variables:
    ```sh
    set FLASK_APP=app.py
    set FLASK_ENV=development
    set FLASK_DEBUG=1
    ```
5. Run the application:
    ```sh
    flask run
    ```
6. Open the provided URL in your browser.

## Usage

- Ensure the debug mode is enabled for proper CSS functionality.
- Copy the URL from the command line output and paste it into your browser to access the app.
  ![](static/css/images/cmd-running.png)

## Screenshots

### 1. Login Page
![Login Page](static/css/images/screenshots/Login.png)

### 2. Load Case Page
![Load Case Page](static/css/images/screenshots/loadCase.png)

### 3. New Case Page
![New Case Page](static/css/images/screenshots/newCase.png)

### 4. Overview
![Overview](static/css/images/screenshots/overview.png)

### 5. Finding New Entry
![Finding New Entry](static/css/images/screenshots/newFindingEntry.png)

### 6. Evidence Repo
![Evidence Repo](static/css/images/screenshots/submitEviRepo.png)

### 7. Analysis
![Analysis](static/css/images/screenshots/analysis.png)

### 8. Memory View
![Memory View](static/css/images/screenshots/memView.png)

### 9. Hex View
![Hex View](static/css/images/screenshots/hexView.png)

## Features

- User authentication and case management.
- Digital evidence storage and analysis.
- Memory and hex view functionalities.

## Technologies Used

- Flask
- MySQL
- HTML/CSS
- JavaScript
