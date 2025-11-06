Sign in/Sign Up
-----------------------
As an user (IWU Student), I want to be able to create an account/sign in, so that I can have a profile to post or request items.

 - Priority: 10/10
 - Estimate: 6 hours
 - Confirmation:

   1. Given I am on the sign up page with a new (IWU) email. When I submit a strong password, then I receive a confirmation email.
   2. When I try to use an existing email again, then I see "Email Already In Use" and no account created.
   3. When I try to enter 1234 as password, I see a clear message like, "Password Must be 8 at least 8 char, includes letter and numbers".
   4. When I enter an invalid email address including non IWU email, then I see an error message saying, "Email must be valid" and the form doesn't submit.
   5. Given my account exists and when I enter a wrong password, I see "Account Email or Password is Incorrect".
   6. Given I am on the sign in page, when I enter my account email and password, I see that I am able to sign in and later I can check data at the backend as an admin.
   7. Given I am on the login page, when I select "Remember Me", when I close or reopen the browser, then I am still logged in until the remember me duration ends.

Log Out
-----------------------
As an user (IWU Student), I want to be able to log out so that I can safely close my profile.

 - Priority: 10/10
 - Estimate: 4 hours
 - Confirmation:

   1. Given I am logged in, when I click logout, then I am redirected to the login page and I am no longer authenticated to the profile.
   2. Given I am logged in and when I click logout, my profile closes and then any subsequent access to /me  fails with 401 until I log back in.
   3. Given I am logged out from the dashboard and when I hit the browser back button to return to the dashboard, then I see the login page.

Post Items
-----------------------
As a user I want to be able to post items (that I no longer need) so that others can see and take those.

 - Priority: 10/10
 - Estimate: 4 hours
 - Confirmation:

   1. Given I am on my dashboard, when I click post from the navbar, I see I am redirected to the "create post" page where I can fill out the details (including pictures) of the items, and when I hit submit then I see the items go live and I receive a pop-up notification saying "item successfully listed".
   2. Given my items are listed on the profile, when I want to modify the items, I can select modify and then be able to change details of the items.

Search Items
-----------------------
As a user I want to be able to search items so that I can filter through all items easier.

 - Priority: 10/10
 - Estimate: 2 hours
 - Confirmation:

   1. User clicks on search bar
   2. User types a keyword
   3. User clicks on a "search" button
   4. System displays items that match the given keyword

Update Posted Items
-----------------------
As a user, I want to be able to update any of my posted items, so their details are accurate

 - Priority: 10/10
 - Estimate: 1 hour
 - Confirmation: 

   1. User clicks on "My products" in navbar
   2. User is redirected to the "my products" page
   3. User sees a list of all of their products
   4. User can update any by clicking on a "update" button next to the item

Delete Posted Items
-----------------------
As a user, I want to be able to delete any of my posted items, so they're not live anymore

 - Priority: 10/10
 - Estimate: 30 minutes
 - Confirmation: 

   1. User clicks on "My products" in navbar
   2. User is redirected to the "my products" page
   3. User sees a list of all of their products
   4. User can delete any by clicking on a trash can icon next to the item title

View Recent Items
-----------------------
As a user, I want to view the most recent items in the main page, so I can quickly see what's been added lately

 - Priority: 10/10
 - Estimate: 1 hour
 - Confirmation:
    
   1. User navigates to the main page
   2. Page shows the most recent items, which the user can scroll through


Message Forum
-----------------------
As a user, I want to chat with item owners, so I can ask questions about the item, or I can arrange a time and place to pick up/retrieve the item

 - Priority: 10/10
 - Estimate: 9 hours
 - Confirmation:

   1. There should be a dedicated page for messages
   2. User should be able to click on a person's profile, and given the option to message them
   3. Ensure the messages are saved, even if the user goes to a different page or closes the application

Notifications
-----------------------
As a user, I want to be able to receive email notifications when someone interested in one of my items messages me for the first time

 - Priority: 8/10
 - Estimate: 6 hours
 - Confirmation:

   1. Alert the user to allow push notifications on their phone
   2. User should be able to click on the notification, and take them to the liked item

Wishlist
-----------------------
As a user I want to be able to favorite or save specific items so that I don't have to search for them again.

 - Priority: 7/10
 - Estimate: 5 hours
 - Confirmation:

   1. Dedicated page where people can save their favorite item
   2. Ensure that the page only saves the item the user wants on their wishlist
   3. When scrolling through the page, ensure there's a button the user can press to favorite their item.
   4. Users should be able to go to the dedicated wishlist page, to go see the item they favor for later.

Pinned Messages
-----------------------
As a user I want to be able to pin conversations so that I don't lose sight of important conversations.

 - Priority: 6/10
 - Estimate: 3 hours
 - Confirmation:

   1. Ensure there is a button that resembles the pin button
   2. Ensure that the message stays at the top of the messages when pinned
   3. Ensure that the user can unpin the message when finished

Item Visibility
-----------------------
As a finder, or giver, I want to have a page where I can see all items and their current status, so I know which ones are still live or claimed.

 - Priority: 10/10
 - Estimate: 4 hours
 - Confirmation:

   1. Ensure there is a page dedicated to each user (finder or seeker) that displays all of their listed items (if any).
   2. Ensure that there is a button that marks an item as retrieved for the seeker.
   3. Ensure that the status of the item is updated after the user marks the item as retrieved.
   4. Ensure that no other item is affected by this action or in other words, make sure the specified item is the ONLY item marked as retrieved.
   5. Make sure the page correctly shows retrieved and live items.

Deleting Conversations
-----------------------
As a user, I want to be able to delete conversations so that I can declutter my inbox.

 - Priority: 8/10
 - Estimate: 2 hours
 - Confirmation:

   1. Given that the user is on the page that displays their conversations, if there are any conversations the user wants to delete, they should be able to swipe right and delete the conversation.
   2. After deleting the conversation, it should be removed from the user's inbox.
   3. All other conversations should remain as they are.
   4. the final view for the user should correctly show all other conversations besides the deleted one.

Blocking Users
-----------------------
As a user, I want to be able to block users in the event where I feel uncomfortable so that I can prevent harassment.

 - Priority: 8/10
 - Estimate: 5 hours
 - Confirmation:

   1. Given that the user is on the page that displays their conversations, if there are any users they want to block, they should be able to tap on a block button within the conversation.
   2. After blocking the user, the blocked user should be removed from the other user's inbox along with the conversation.
   3. the blocked user should not be allowed to have further contact with the user who initiated the block.
   4. All other conversations and users should remain as they are, maintaining their connection with the user.
   5. the final view for the user should correctly show all other current conversations and users besides the blocked user/conversation.

User Configurations/ Settings
-----------------------
As a user, I want to have a configurations page, where I can modify my public username, and disable/enable email notifications, so I can protect my identity and have more privacy

 - Priority: 6/10
 - Estimate: 7 hours
 - Confirmation:

   1. Have a page dedicated to displaying the user's settings with different options the user can choose from. Ex: notification settings, and privacy settings
   2. Ensure the different settings are represented by different types of buttons so we can make sure those settings are met.
   3. Test different combinations of settings to make sure expectations are met.