Initial Iteration Plan: Adding more features
Team: Team Yoink Iteration Dates: Nov 17th, 2025 - Nov 23rd, 2025 Report Date: Nov 19th, 2025.

Second-week Iteration
Team Members

Chris - Setting up the search bar, documenting the code
Earl - Adding an user page and user blocking feature
Hirat - Modiying, deleting post and grid columns
Yohance - Secure login (password hasing, email specific signup)

Iteration Goal is to add some more features to be able to login securely, modify and delete posts, search items, and block any unwanted user.

Setting up the search bar, documenting the code (Chris)

Work Completed:
- Documented the whole code.
- Search bar works perfectly 

Problem:
- Making the search more flexible in terms of getting related items (which worked later on)

Things to do:
- 


User page and user blocking (Earl)

Work Completed:
- The user's profile page is complete. Users can now view other users' pages. There is a block button as well. 
- The blocking feature is not yet done. It's about 50% done with the button being functional, redirecting the user to the list items page

Problem:
- The way I began the implementations was not the best. I was going to add a column to hold a list representation of blocked user IDs. Now I'm going to attempt to achieve this functionality differently. 

Things to do:
- Edit the DB and create a table related to each user to hold the user IDs of the users they block.
- edit the route to the list items page (homepage) to not display things from the blocks users.  


Modiying, deleting post and grid columns (Hirat)

Work Completed:
- Added the delete and edit option on the posted items list. 
- Users can now edit and modify the existing posts
- Made the homepage more responsive in terms of the screen size with two columns for the posts

Problems:
- Had some github issues, mainly with the db file which was creating merge conflicts.

Things to do:
- Limit the title, description and contact info charracters, so that it doesn't create problem
- Make the posts details available only to logge in users.


Secure login (password hasing, email specific signup) (Yohance)

- security measures include ensuring passwords aren't saved in their raw form in the database, by hashing them on sign up. 
- Following log in attempts compare hashes between the stored password in the database, and the password given by the user, which is initially hashed before being compared. 
- ensuring only IWU students can log in and sign up by using an email-based authentication method, where a short-lived code is sent to the email the user tries to use to sign up. Afterwards, the user must input the right code, so it is confirmed they are actually an IWU student.

Most of the work is done (except for the blocking feature) as planned before. (90%)

Challenges: Github merge conflicts, adding the blocking feature

Next steps: Chris: will work to make search more flexible Hirat: will work on making the details available only to logged in users and limit characters for posts. Yohance: will work on unit testing. Earl: Will work on implementing the rest of the blocking feature.

Team Feedback: Chris: Good job having the searh bar working Hirat: check on edge cases and look into github issues Yohance: nice work checking on the login/ sign up but try not to wait till the last minute Earl: Good approach towards the blocking feature, but try to reach for help earlier if needed.