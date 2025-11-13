# Initial Iteration Plan: Infrustructure Setup

Team: Team Yoink
Iteration Dates: Nov 7th, 2025 - Nov 14th, 2025 
Report Date: Nov 12th, 2025

## First-week Iteration
**Team Members**
1. Earl - Setting up the DB
2. Yohance - Log In/Out & Sign Up
3. Chris - UI Guidelines
4. Hirat - Post Items

***Iteration Goal***
Create the infrustructure of the web app by setting up login/logout, the databbase and some basic functionality like posting and being able to modifying the posts.

Work Completed 
1. Set up the DB (Earl)

    - Created a database where all items have a name, status,
    image url, location, description, and creation timestamp
        - Name: name of item
        - Status: current status of the item
        - Image URL: URL for image so it isn't stored locally
        - Description: information about the item
        - Creeation Time

    - POST/ item: post an item to platform
    - GET/ item: getting an item a user is intrested 
    - There was a bug were github had a hard time using the db already made.
      So we just deleted the db, then init the database again to fix it.
    Completetion time: 5 hours

2. Authenication (Yohance)
Tasks:

    - Implement basic authentication
    - Design and implement log in/out, and sign up functionalities.
        - Created core endpoints:
            GET /login - Log in or sign up page
                - User can either log in, or sign up. 
            GET /verify-user - verify the given username and password is valid
                - Involves hashing the given password and comparing it to the actual one
            GET /logout - Log out
                - Clear cookies and other related browser-stored user data
            POST /create-account - Create a new user instance in the DB
                - This entails hashing the password for security reasons
        - Completetion time: 8 hours

3. UI Guidelines (Chris)
    - Made Guidlines for how the UI and Login page should look like
    - Created images for the buttons. Specifically the bell, magnifying glass, and inbox
    - Created a basic html file for the main_page of the server. Still not finished with the complete layout
    Estimated Hours: 10 hours

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
        - Estimated Hours: 10 hours

Key Metrics:

Metric       Value
Total hours worked 33 hours
Tasks planned 4
Tasks completed 3.5
Complete rate 85%
Bugs 1(resolved)

Challenges:
Integration delays: due to some issues with the database

Next steps:
Chris: Will work on the search feature for the webpage
Hirat: will work on the modifying the post.
Yohance: will work on checking to see if the user is from IWU, and to hash the password.
Earl: Will work on seeing other users profiles

Team Feedback:
Chris: Contribute more code
Hirat: make sure to communicate with the team before going off to do other parts of the project
Yohance: good job helping with the database fixing that bug
Earl: nice on getting the database started