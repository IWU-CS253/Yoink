# Iteration Report - Week 4 

## Team Members
- Yohance
- Hirat
- Chris
- Earl

## 1. Responsibilities & Completed Work

### Yohance
- Add rate limiting by user id
    - Created a decorator in utils.py to allow limiting users' requests
    - Rate-limited important endpoints in items.py and users.py
- Add rate limiting by identifier (email)
    - Created a decorator in utils.py to allow limiting users' requests based on the email in the request data
    - Rate-limited OTP generation endpoint in users.py so user's find it a lot more difficult to abuse our email client
- Allow only logged in users to perform certain CRUD operations
    - Created a decorator in utils.py to allow restricting certain endpoints to only logged in users
- Organize backend by splitting up the code into different files
    - Used flask [blueprints](https://flask.palletsprojects.com/en/stable/blueprints/) to organize all endpoints across 3 files under the routes folder
    - Moved utility functions from app.py to utils.py, to keep only core logic in app.py

Tech Stack Used:
Backend: app.py, items.py, users.py, auth.py, utils.py 

### Hirat
- Improve the Home page styling to make the website more visually appealing
    - Reorganized the navigation bar items layout at layout.html. Item related links in the left ("Home" and "Post item"), and user related links in the right ("My items", "Blocked users", and "Log out").
- Create and add a favicon for the website
    -  Created an icon for the app 
    -  Created and implemented favicon based off of the app icon
- Create and add a default image for posts with no pictures at items_list.html.
- Improve the style of cards in the main page at items_list.html
- Improved the style of "edit" and "delete" buttons for every item in the "My Items" page at my_items.html

Tech Stack Used:
Backend: app.py, items.py, users.py, auth.py, utils.py 

### Chris
- Update search endpoint so users wouldn't be able to see posts of people they have blocked
    - This involved adding logic at the search endpoint in items.py
- Set up the unit tests and Github Actions, so unit tests run on every push
    - This involved creating and constructing a yml file at .github/workflows/python_test.yml   
- Created and added 5 unit tests to cover all basic operations
    -   Unit tests run as a Github Action, and their details are at Unittest.py
    -   
Tech Stack Used:
Backend: .github/workflows/python_test.yml, Unittest.py

### Earl
- Fixed Blocked Users Functionality
    - Modified routes for blocked_users, unblock_users, and items_list in app.py
    - Implemented logic so users cannot see posts from people who have blocked them
    - Updated database schema to include a blocked_by column to track who has blocked the current user

- Profile Pictures Decision
    -  Decided with the team not to implement user-uploaded profile pictures, as it would add more overhead than we can afford
    - Will use the default Yoink photo for all users' profile photos

- Accessibility Assessment
    - Evaluated website accessibility and navigation
    - Found that the site is already sufficiently understandable and navigable with minimal changes needed

Tech Stack Used:
Backend: users.py, items.py
Frontend: Various templates and pages to verify accessibility
Database: schema.sql - Schema changes

## 3. Planned but Incomplete Work
All planned features were implemented on time. We were all able to implement our featues on time, and even started on next week's work.

## 4. Challenges and Roadblocks

### Technical Issues
- Yohance: Understanding how to add rate limiting for users. Web tutorials and blogs helped a lot.
- Hirat: None
- Chris: Understand unit tests and how to create a robust set up
- Earl: Understand flow of information across different APIs, pages, and database.

## 5. Design Adjustments

### Changes to Original Design
- Users won't be able to upload profile pictures. This could be a future to add in the future, but is not crucial given our scope.

### Architecture Decisions
- Every function/endpoint should be grouped by category into its own file
    -   For example, all item related endpoints are under routes/items.py, same for user and auth related endpoints.

## 6. Key Learnings

### Yohance
- Understanding how to secure endpoints from bad actors who may abuse them is critical.

### Hirat
- Styles are important, and they are crucial for giving the impression of a robust and well-rounded application.

### Chris
- Unit tests help the development process by allowing developers to spot flaws and introduced errors as early as possible.

### Earl
- Understanding how the flow of information is crucial for building/updating new featues. Documentation is important for the same reasons.

## 7. Final Week Plan

### Objectives
- Wrap up development, by spotting the last few flaws in our code, and improve overall styles.

### Task Assignments

At this point, we are done with our project features. All that is missing is improving a few trivial things around the app. Examples of this tasks are visual styles and ensuring all functionalities work.

### Timeline
- By the end Monday, December 8th, we expect to have the final iteration of our project done. This means we will have all of the documentation in place, as well as any other missing bug/feature.

### Preparation for Demo/Presentation
- Materials to prepare:
    - Presentation Slides: Everyone in the group
- Coordinate when to meet up to practice our presentation: Yohance
