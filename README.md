# Social Network App

A Django-based application to manage a social network.

## Features

- User registration
- User login/logout
- User profile management
- Friend management (add, remove, accept/reject requests)
- User search

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/signup/` | POST | Create a new user |
| `/api/login/` | POST | Login a user and obtain JWT tokens |
| `/api/token/refresh/` | POST | Refresh JWT token |
| `/api/profile/` | GET | Retrieve user profile |
| | PUT/PATCH | Update user profile |
| `/api/friends/` | GET | List user's friends |
| `/api/add-friend/` | POST | Send a friend request |
| `/api/update-friend-request/` | POST | Accept or reject a friend request |
| `/api/remove-friend/` | POST | Remove a friend |
| `/api/search/` | GET | Search for users |
| `/api/friend-requests/` | GET | List pending friend requests |

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up the database: `python manage.py migrate`
4. Run the development server: `python manage.py runserver`

## Usage

1. Register a new user account
2. Log in with your credentials
3. Update your profile information
4. Search for friends and send friend requests
5. Accept or reject incoming friend requests
6. View your friend list
7. Remove friends if needed

## To do list
- [ ] Pagination for search, friend requests and friends list 

## App Screenshots

Signup 
![Screenshot from 2024-09-06 10-29-46](https://github.com/user-attachments/assets/f4149124-9ac8-49c3-a476-e586bcd621ea)

Login
![Screenshot from 2024-09-06 10-29-51](https://github.com/user-attachments/assets/1d97e7c0-d612-44a9-a007-cb854c12e908)


Friends List
![Screenshot from 2024-09-06 10-10-30](https://github.com/user-attachments/assets/c80f1486-f891-4f2c-aa8e-808da4d813cd)

Friend Request List
![Screenshot from 2024-09-06 10-10-37](https://github.com/user-attachments/assets/2f5111ff-b455-4c4f-a514-7f6b321a2565)


Search Friends
![Screenshot from 2024-09-06 10-30-53](https://github.com/user-attachments/assets/0357b66a-abd2-48c1-91ca-e58deba06c65)


