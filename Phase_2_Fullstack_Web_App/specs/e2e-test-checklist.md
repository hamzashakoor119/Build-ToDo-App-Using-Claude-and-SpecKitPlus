# End-to-End Manual Testing Checklist

**Purpose**: Verify all 6 user stories work correctly through the UI.
**Date**: 2025-12-29

## Prerequisites

- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:3000
- [ ] Database connected (Neon PostgreSQL)
- [ ] BETTER_AUTH_SECRET matches in both .env files

---

## US1: User Registration and Login

### Registration Flow

| Step | Action | Expected Result | Status |
|------|--------|-----------------|--------|
| 1 | Navigate to http://localhost:3000 | Redirects to /login page | ☐ |
| 2 | Click "Register" link | Shows registration form | ☐ |
| 3 | Enter email: test@example.com | Email input accepts value | ☐ |
| 4 | Enter password: password123 | Password input shows dots | ☐ |
| 5 | Enter confirm password: password123 | Shows "Passwords match" indicator | ☐ |
| 6 | Click "Register" button | Loading spinner appears | ☐ |
| 7 | Wait for completion | Redirects to dashboard | ☐ |

### Login Flow

| Step | Action | Expected Result | Status |
|------|--------|-----------------|--------|
| 1 | Log out (if logged in) | Redirects to /login | ☐ |
| 2 | Enter registered email | Email input accepts value | ☐ |
| 3 | Enter password | Password input accepts value | ☐ |
| 4 | Click "Login" button | Loading spinner appears | ☐ |
| 5 | Wait for completion | Redirects to dashboard | ☐ |
| 6 | Verify user name shown in header | Email/name displayed | ☐ |

### Logout Flow

| Step | Action | Expected Result | Status |
|------|--------|-----------------|--------|
| 1 | Click "Logout" button in header | Logging out... | ☐ |
| 2 | Wait for completion | Redirects to /login | ☐ |
| 3 | Try to access /dashboard directly | Redirects back to /login | ☐ |

### Error Cases

| Scenario | Action | Expected Result | Status |
|----------|--------|-----------------|--------|
| Wrong password | Login with wrong password | Shows error message | ☐ |
| Non-existent user | Login with unknown email | Shows error message | ☐ |
| Password mismatch | Register with different passwords | Shows validation error | ☐ |
| Short password | Register with <6 char password | Shows length warning | ☐ |

---

## US2: View Task List

| Step | Action | Expected Result | Status |
|------|--------|-----------------|--------|
| 1 | Login successfully | Dashboard shows | ☐ |
| 2 | View empty state | "No tasks yet" message | ☐ |
| 3 | After adding tasks | Tasks appear in list | ☐ |
| 4 | Active section | Shows incomplete tasks | ☐ |
| 5 | Completed section | Shows completed tasks | ☐ |
| 6 | Task displays title | Title visible | ☐ |
| 7 | Task displays description | Description visible | ☐ |
| 8 | Loading state | Spinner while fetching | ☐ |

---

## US3: Add New Task

| Step | Action | Expected Result | Status |
|------|--------|-----------------|--------|
| 1 | Find "Add Task" form | Form visible at top | ☐ |
| 2 | Enter title: "Buy groceries" | Title input accepts text | ☐ |
| 3 | See character counter | "X characters remaining" | ☐ |
| 4 | Enter description: "Milk, eggs" | Description textarea works | ☐ |
| 5 | Click "Add Task" button | Loading spinner appears | ☐ |
| 6 | Wait for completion | Task appears in list | ☐ |
| 7 | Form clears | Title and description empty | ☐ |
| 8 | Success message | Toast notification shown | ☐ |

### Validation Tests

| Scenario | Action | Expected Result | Status |
|----------|--------|-----------------|--------|
| Empty title | Submit with no title | Button disabled or error | ☐ |
| Long title | Enter 201+ characters | Counter shows warning | ☐ |
| Long description | Enter 1001+ characters | Counter shows warning | ☐ |
| Title only | Submit with just title | Task created successfully | ☐ |

---

## US4: Mark Task Complete

| Step | Action | Expected Result | Status |
|------|--------|-----------------|--------|
| 1 | Create a new task | Task in Active section | ☐ |
| 2 | Find checkbox on task | Checkbox visible, unchecked | ☐ |
| 3 | Click checkbox | Loading indicator | ☐ |
| 4 | Wait for completion | Task moves to Completed section | ☐ |
| 5 | Task shows strikethrough | Visual distinction | ☐ |
| 6 | Click checkbox again | Task toggles back | ☐ |
| 7 | Task moves to Active | Returns to active section | ☐ |

---

## US5: Update Task

| Step | Action | Expected Result | Status |
|------|--------|-----------------|--------|
| 1 | Find edit button on task | Pencil/Edit icon visible | ☐ |
| 2 | Click edit button | Modal opens | ☐ |
| 3 | Modal shows current values | Title/description pre-filled | ☐ |
| 4 | Edit title | Text changes | ☐ |
| 5 | See character counters | Remaining chars shown | ☐ |
| 6 | Edit description | Text changes | ☐ |
| 7 | Click "Save" button | Loading state | ☐ |
| 8 | Wait for completion | Modal closes | ☐ |
| 9 | Verify changes in list | Updated values shown | ☐ |

### Modal Behavior

| Scenario | Action | Expected Result | Status |
|----------|--------|-----------------|--------|
| Click outside modal | Click backdrop | Modal closes | ☐ |
| Press Escape | Press Esc key | Modal closes | ☐ |
| Cancel button | Click Cancel | Modal closes, no changes | ☐ |
| Mobile view | Open on small screen | Bottom sheet style | ☐ |

---

## US6: Delete Task

| Step | Action | Expected Result | Status |
|------|--------|-----------------|--------|
| 1 | Find delete button on task | Trash icon visible | ☐ |
| 2 | Click delete button | Confirmation appears | ☐ |
| 3 | Confirmation shows task title | Task identified | ☐ |
| 4 | Click Cancel | Dialog closes, task remains | ☐ |
| 5 | Click Delete again | Confirmation shows | ☐ |
| 6 | Click Confirm/Delete | Loading state | ☐ |
| 7 | Wait for completion | Task removed from list | ☐ |
| 8 | Verify task gone | Not visible anywhere | ☐ |

---

## Responsive Design Tests

Test on different screen sizes:

| Screen Size | Resolution | Test | Status |
|-------------|------------|------|--------|
| Mobile small | 320px | All features work | ☐ |
| Mobile large | 414px | All features work | ☐ |
| Tablet | 768px | Layout adjusts | ☐ |
| Desktop | 1024px+ | Full layout | ☐ |

### Mobile-Specific Tests

| Feature | Test | Expected Result | Status |
|---------|------|-----------------|--------|
| Header | Check logout button | Icon only (no text) | ☐ |
| Task buttons | Check edit/delete | Icon buttons | ☐ |
| Edit modal | Open edit modal | Bottom sheet style | ☐ |
| Form | Check add task form | Stacked layout | ☐ |

---

## Error Handling Tests

| Scenario | How to Trigger | Expected Result | Status |
|----------|----------------|-----------------|--------|
| Network offline | Disable network | User-friendly error | ☐ |
| API 500 error | Backend crash | "Something went wrong" | ☐ |
| Session expired | Wait for token expiry | "Session expired" | ☐ |
| Slow network | Throttle network | Loading indicators | ☐ |

---

## Persistence Tests

| Test | Steps | Expected Result | Status |
|------|-------|-----------------|--------|
| Page refresh | Add task, refresh page | Task still there | ☐ |
| Login/logout | Logout, login again | All tasks preserved | ☐ |
| Browser close | Close, reopen browser | Session maintained | ☐ |

---

## Test Summary

| User Story | Total Tests | Passed | Failed |
|------------|-------------|--------|--------|
| US1: Auth | 15 | ☐ | ☐ |
| US2: View | 8 | ☐ | ☐ |
| US3: Add | 8 | ☐ | ☐ |
| US4: Complete | 7 | ☐ | ☐ |
| US5: Update | 13 | ☐ | ☐ |
| US6: Delete | 8 | ☐ | ☐ |
| Responsive | 8 | ☐ | ☐ |
| Error Handling | 4 | ☐ | ☐ |
| Persistence | 3 | ☐ | ☐ |
| **Total** | **74** | ☐ | ☐ |

---

## Sign-Off

- [ ] All user stories functional
- [ ] Responsive design verified
- [ ] Error handling appropriate
- [ ] Data persists correctly
- [ ] Ready for deployment

**Tester**: _______________
**Date**: _______________
**Approved**: ☐ Yes ☐ No

---

## Notes

_Record any issues, observations, or recommendations here:_

