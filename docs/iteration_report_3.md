# Iteration Plan 3: Touch Ups


Team: Team Yoink 

Iteration Dates: Break - Dec 1st, 2025

Plan Date: Nov 24th, 2025

# Completed


1. User blocking and unblocking (Earl)
   - Added a new column to the users table so that we can store blocked users
   - Edited the route to the list items page (homepage) to not display things from the blocks users or the current logged in user.  
   - Implemented a feature to unblock people as well
- Tech Stack: front/backend
  - blocked_users_list.html, user_profile.html
  - app.py: route to block and unblock users. Also fixed the list 
  items route to not display posts to their owners. 

2. Modifying, deleting post and grid columns (Hirat)
   - Limited the title, description and contact info characters, so that it doesn't create problems
   - Made the posts details available only to users who are logged in.
- Tech Stack: frontend
  - items_edit.html, items_new.html 

3. Secure login (password hashing, email specific signup) (Yohance)
   - Paid key detail to security measures include ensuring passwords aren't saved in their raw form in the database, by hashing them on sign up. 
   - Following log in attempts compare hashes between the stored password in the database, and the password given by the user, which is initially hashed before being compared. 
   - Ensuring only IWU students can log in and sign up by using an email-based authentication method, where a short-lived code is sent to the email the user tries to use to sign up. Afterwards, the user must input the right code, so it is confirmed they are actually an IWU student.
- Tech Stack: front/backend
  - otp_registration.html, register.html, login.html
  - app.py: routes for registering and logging in. 

4. Search Bar Functionality (Chris)
   - Implemented functionality that allows users to search up items.
   - Added functionality that allows users to search up other users as well.
- Tech Stack: front/backend
  - items_list.html
  - app.py: route to search which includes sql queries. 
  
*We have successfully accomplished our main goals for last week. Now we are going to focus more on fixing bugs in our site and making 
sure our code is clean and readable. One thing that should be noted is that we collectively decided to wait for unit testing. It was Yohance 
task for last week, but he ended up being tasked with something different that was of higher priority.*

Team Feedback: 
- Chris: Good job for making the search bar more functional
- Hirat: Nice work for adding limits to text inputs
- Yohance: Very nice work with your security implementations 
- Earl: I think I did good work with my implementation of the block and unblock feature


## Third-week Iteration

1. Earl - Assessing accessibility/ allowing users to upload profile pictures
    - We currently have profile pictures that currently just displays 
   lorem ipsum images. I now have to make it where users can upload profile photos when they register. This
   pfp shows when on a user profile or blocked users list. 
    - I also too will be working on some accessibility within the website making it 
   more understandable and navigable. 
    - I will also jump in and help with unit testing when he finishes up.
- Tech Stack: frontend (mainly)/backend
  - blocked_users_list.html and user_profile.html (and others for accessibility)
  - app.py: unit test
  
2. Yohance - Code Clean-up/ Refactoring.
    - Working on cleaning up & slightly refactoring our codebase by breaking up app.py (backend) into multiple files. 
    - Utilizing flask blueprints which allow you to organize your app in modular components. This makes the code more organized and 
    easy to maintain. 
    - This week he Yohance will be working mostly on the backend. He will also jump in and help with unit testing when he finishes up.
- Tech Stack: backend
  - restructuring the codebase to make it more organized

3. Chris - Getting started with unit tests
    - Will get us started on unit testing
    - Although Chris is getting us started, we all will jump in eventually and help when we are done with our 
   current task.
- Tech Stack: backend
  - working with all html files making sure they are well commented
  - unit testing, app.py: commenting
  
4. Hirat - Working on the front end making the site more appealing
    - Will be working more closely with th front end, making our website look 
   more professional and visually appealing. 
    - Hirat will also jump in and help us with unit testing when he finishes up. 
- Tech Stack: frontend (mainly)/backend
  - working in all html files changing styling of need be
  - unit testing. 

#  
Next steps: Implementing unit test, fixing accessibility, cleaning up code, and 
designing a better user interface. 
