# Hands-On 1 – QA Concepts
## Task 1
### 1. Unit Testing
Unit testing is used to test a single function or method.
Example:
Test the create course function and check whether the course is created correctly.
Type: Functional Testing
### 2. Integration Testing
Integration testing checks whether two or more modules work together properly.
Example:
Add a course using the API and check whether the data is stored in the database.
Type: Functional Testing
### 3. System Testing
System testing checks the complete application.
Example:
Create a course, view it, update it and delete it. All the features should work properly.
Type: Functional Testing
### 4. User Acceptance Testing (UAT)
This testing is done by the end user before using the application.
Example:
The college administrator checks whether all the course management features are working correctly.
Type: Functional Testing
---
## Functional and Non-Functional Testing
The above test cases are Functional Testing because they check whether the application is working correctly.
Example for Non-Functional Testing:
Performance Testing
Check whether the Course Management API responds quickly when many users use it at the same time.
---
## Black Box Testing and White Box Testing
Black Box Testing means testing the application without seeing the source code. Only the input and output are checked.
White Box Testing means testing the application by looking at the source code and program logic.
QA Testers usually perform Black Box Testing.
Developers usually perform White Box Testing.
---
## Test Cases for POST /api/courses/

| Test Case ID | Description | Preconditions | Test Steps | Expected Result | Actual Result | Pass/Fail |
|---------------|-------------|---------------|------------|-----------------|---------------|-----------|
| TC01 | Create a new course | API is running | Send POST request with valid course details | Course should be created successfully | | |
| TC02 | Create course without course name | API is running | Send POST request without course name | Validation error should be displayed | | |
| TC03 | Create duplicate course | Course already exists | Send same course details again | Duplicate course should not be created | | |

---

# Task 2

## Defect Lifecycle

New

↓

Assigned

↓

Open

↓

Fixed

↓

Retest

↓

Verified

↓

Closed

Rejected – The issue is not a valid defect.

Deferred – The defect will be fixed in a future release.

---

## Severity and Priority

### a) POST /api/courses/ returns 500 Internal Server Error

Severity: Critical

Priority: P1

Reason:
The API is not working and users cannot create courses.

### b) Course names longer than 150 characters are truncated

Severity: Medium

Priority: P2

Reason:
The application works but part of the data is lost.

### c) Typo in Swagger documentation

Severity: Low

Priority: P4

Reason:
Only the documentation is affected.

### d) Login sometimes returns 401 even with correct credentials

Severity: High

Priority: P1

Reason:
Users cannot log in properly every time.

---

## Defect Report

Defect ID: DEF001

Title: POST /api/courses/ returns 500 Internal Server Error

Environment: Windows 11, Chrome Browser, Django Application

Build Version: 1.0

Severity: Critical

Priority: P1

Steps to Reproduce:
1. Start the application.
2. Open the Course Management API.
3. Send a POST request with valid course details.
4. Check the response.

Expected Result:
Course should be created successfully.

Actual Result:
The API returns 500 Internal Server Error.

Attachment:
Screenshot of the 500 error.

---

## Difference Between Severity and Priority

Severity tells how much the defect affects the application.

Priority tells how quickly the defect should be fixed.

Example:

A spelling mistake on the home page has low severity because it does not affect the application. But if the page is going to be shown in a client meeting, it becomes high priority because it should be fixed before the meeting.