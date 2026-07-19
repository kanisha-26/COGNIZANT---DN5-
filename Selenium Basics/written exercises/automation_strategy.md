# Hands-On 3 – Test Automation Process and Framework Types

## Task 1

### 1. Criteria for Automating Test Cases

**1. Repeated Execution**
If a test case is executed many times, it is better to automate it.

Application:
The POST /api/courses/ API is tested regularly, so automation is useful.

---

**2. Regression Testing**

Regression test cases are good candidates for automation because they are executed after every code change.

Application:
The POST API should always be checked after changes.

---

**3. Stable Features**

Features that do not change frequently can be automated.

Application:
The course creation API does not change often, so it is suitable for automation.

---

**4. Data-Driven Testing**

If the same test is executed with different inputs, automation saves time.

Application:
The POST API can be tested with different course names and course codes.

---

**5. Time Saving**

Automation reduces manual effort for repetitive testing.

Application:
Instead of testing the POST API manually every time, the script can complete it in a few seconds.

---

### 2. Manual or Automation

| Test Case | Decision | Reason |
|------------|----------|--------|
| Regression testing of CRUD APIs | Automate | Executed after every code change |
| Exploratory testing | Manual | Human observation is required |
| Performance testing | Automate | Many users must be simulated |
| Login page testing | Automate | Repeated frequently |
| Swagger documentation check | Manual | Mainly a content review |
| Smoke testing after deployment | Automate | Quick verification after every deployment |

---

### 3. Automation ROI

Automation ROI means checking whether the time spent developing automation is worth the time saved later.

Automation Time = 4 hours

Manual Time = 30 minutes

4 hours = 240 minutes

240 ÷ 30 = 8

The automation starts saving time after about **8 test runs**.

After the 10th run, maintenance effort is needed, but automation is still useful because it reduces repeated manual work.

---

### 4. Flaky Test

A flaky test is a test that sometimes passes and sometimes fails without any code changes.

Example:

A Selenium test fails because the page takes longer to load.

Ways to reduce flaky tests:

- Use Explicit Wait instead of Thread Sleep.
- Use stable locators like ID or Name.
- Keep test data consistent.

---

# Task 2

## Framework Types

### Linear Framework

Description:
Test cases are written one after another in a single script.

Advantage:
Easy to understand.

Disadvantage:
Not reusable.

Example:
Small project with only a few test cases.

---

### Modular Framework

Description:
The application is divided into different modules.

Advantage:
Reusable code.

Disadvantage:
Needs better planning.

Example:
Separate modules for Login, Course and Student pages.

---

### Data-Driven Framework

Description:
Test data is stored in Excel, CSV or JSON files.

Advantage:
Same script can run with different data.

Disadvantage:
Managing test data takes extra effort.

Example:
Testing login with multiple usernames and passwords.

---

### Keyword-Driven Framework

Description:
Test steps are controlled using predefined keywords.

Advantage:
Non-technical users can prepare test cases.

Disadvantage:
Framework setup is more complex.

Example:
Keywords like Login, Click, Enter Text and Logout.

---

### Hybrid Framework

Description:
Hybrid framework combines two or more framework types.

Advantage:
Flexible and reusable.

Disadvantage:
Takes more time to develop.

Example:
Use Page Objects with Data-Driven testing.

---

## Recommended Framework

I would recommend a Hybrid Framework.

Reason:

- Login steps can be reused.
- Multiple user credentials can be tested easily.
- It is suitable for both small and large projects.
- It is commonly used in real projects.

---

## Hybrid Framework Folder Structure

```
CourseManagementAutomation

│

├── pages

├── tests

├── testdata

├── utilities

├── config

├── reports

├── screenshots

└── requirements.txt
```