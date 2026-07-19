# Hands-On 2 – SDLC vs TDLC, V-Model and Agile QA

## Task 1

### 1. V-Model

```
Requirements                Acceptance Testing

      ↓                            ↑

System Design              System Testing

      ↓                            ↑

Architecture Design      Integration Testing

      ↓                            ↑

Module Design              Unit Testing

            ↓

          Coding
```

---

### 2. SDLC and TDLC Mapping

| SDLC Phase | TDLC Phase | Test Artifact |
|------------|------------|---------------|
| Requirements | Acceptance Testing | Acceptance Test Plan |
| System Design | System Testing | System Test Cases |
| Architecture Design | Integration Testing | Integration Test Cases |
| Module Design | Unit Testing | Unit Test Cases |
| Coding | Testing Execution | Source Code |

---

### 3. Entry and Exit Criteria

#### Unit Testing

Entry Criteria
- Module should be developed.
- Code should be ready.

Exit Criteria
- Unit test cases should pass.
- No major defects.

---

#### Integration Testing

Entry Criteria
- Unit testing should be completed.
- Modules should be integrated.

Exit Criteria
- Integration test cases should pass.
- Data should flow correctly between modules.

---

#### System Testing

Entry Criteria
- Complete application should be available.
- Integration testing should be completed.

Exit Criteria
- All system test cases should pass.
- No critical defects.

---

#### Acceptance Testing

Entry Criteria
- System testing should be completed.
- Application should be ready for users.

Exit Criteria
- User accepts the application.
- All business requirements are satisfied.

---

### 4. QA Involvement in V-Model

1. QA can review the requirements before development starts to identify missing or unclear requirements.

2. QA can review the system design and prepare test cases before coding begins.

---

# Task 2

## 1. Problems in Waterfall Model

1. Bugs are found very late.
2. Fixing bugs takes more time and cost.
3. Changes in requirements are difficult after development.

---

## 2. QA Role in Agile

### Sprint Planning

QA understands the requirements and prepares acceptance criteria.

### Daily Stand-up

QA discusses testing progress and reports any blockers.

### Sprint Review

QA checks whether completed features work correctly.

### Retrospective

QA shares issues faced during testing and suggests improvements.

---

## 3. Shift-Left Testing

### Requirement Review

QA reviews requirements before development starts.

### Test Case Preparation

QA writes test cases before coding.

### Static Code Analysis

Developers check code quality using analysis tools before testing.

### API Contract Testing

API request and response formats are checked before integrating different modules.

---

## 4. Acceptance Criteria (Given – When – Then)

### Scenario 1 – Create Course Successfully

Given the college admin is on the Create Course page

When valid course details are entered and submitted

Then the course should be created successfully.

---

### Scenario 2 – Duplicate Course Code

Given a course with the same course code already exists

When the admin submits the same course code

Then an error message should be displayed.

---

### Scenario 3 – Missing Required Fields

Given the course creation page is open

When required fields are left empty and submitted

Then validation messages should be displayed.