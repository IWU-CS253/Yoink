# Initial Iteration Plan: Infrustructure Setup

Team: Team Yoink
Iteration Dates: Nov 7th, 2025 - Nov 14th, 2025 
Plan Date: Nov 7th, 2025

## First-week Iteration
**Team Members**
1. Earl - Setting up the DB
2. Yohance - Log In/Out & Sign Up
3. Chris - UI Guidelines
4. Hirat - Post Items

***Iteration Goal***
Create the infrustructure of the web app by setting up login/logout, the databbase and some basic functionality like posting and being able to modifying the posts.

Planned Tasks
1. Setting up the DB (Earl)

    - Create a database where all items have a name, status,
    image url, location, description, and creation timestamp
        - Name: name of item
        - Status: current status of the item
        - Image URL: URL for image so it isn't stored locally
        - Description: information about the item
        - Creeation Time

    - POST/ item: post an item to platform
    - GET/ item: getting an item a user is intrested 

2. Authenication (Yohance)
Tasks:

    - Implement basic authentication
    - Design and implement log in/out, and sign up functionalities.
        - Create core endpoints:
            GET /login - Log in or sign up page
                - User can either log in, or sign up. 
            GET /verify-user - verify the given username and password is valid
                - Involves hashing the given password and comparing it to the actual one
            GET /logout - Log out
                - Clear cookies and other related browser-stored user data
            POST /create-account - Create a new user instance in the DB
                - This entails hashing the password for security reasons
        - Estimated Hours: 2 hours

3. UI Guidelines (Chris)
    - Implement how the UI will look for the posted items
    - Each item should have an delete and edit button
    Estimated

4. Post Items (Hirat)
Tasks:

    - Implement basic functionality for posting items
    - Design and implement post items functionalities.
        - Create core endpoints:
            GET /create-item
                - Returns "create item" page with placeholders for the item's information (title, image, location, etc.)
            POST /create-item
                - Creates a new item record in the database
                - Image is posted as a url, which is obtained from Cloudinary.
        - Estimated Hours: 2 hours

**Tentative after this point**

## Second Week Iteration
- Tasks: Integrate all CRUD operations mentioned in user_stories.md, ensure cross-functionality with Cloudinary
- If time allows, work on user's configuration page.

## Third Week Iteration
- Tasks: Integrate the live chat, as well as other tasks revolving around this feature such as
blocking users, pinning conversations, deleting conversations, etc.
- If time allows, work on Notifications

# Key Metrics
Total estimated hours- 20 hours
Total Tasks Planned- 4
Team Capacity- 40 hours (10 hours/person)
Buffer Time- 20 hours

**Risks**
-   Issues while setting up database could delay integration but the whole team will try to have it solved by this weekend meetup.
-   Additional features might extend the work plan a little beyond the capacity.

**Success Criteria**
-   Web app is functional, in terms of being able to login and out.
-   App is able to display posted items and change/modify the posts.
-   At least 85% of the task is done by Nov 11, 2025.