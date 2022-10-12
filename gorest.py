import requests
import json
import logging

#REST basics
#PUT, GET, POST, DELETE

#Bet Fanatics Coding Challenge
#1. Retrieve page 3 of the list of all users.
#2. Using a logger, log the total number of pages from the previous request.
#3. Sort the retrieved user list by name.
#4. After sorting, log the name of the last user.
#5. Update that user's name to a new value and use the correct http method to save it.
#6. Delete that user.
#7. Attempt to retrieve a nonexistent user with ID 5555. Log the resulting http response code.
#8 Write unit tests for all code, mocking out calls to the actual API service.

class GoRest:
    def __init__(self):
        # Personal authorization token from gorest website
        self.token = 'aca1c63e89fb06b3dd05b3d5ef3d7a516fb6892896774873bf441c4764baa31f'
        # logger
        logging.basicConfig(
            level=logging.INFO,
            format="{asctime} {levelname:<8} {message}",
            style='{',
            filename='FanaticsCodingChallengeLog.log',
            filemode='w'
        )
        #Store the list of users from page 3
        self.pageThreeUsers = ''
        #Store sorted list of users from page 3
        self.sortedNames = ''
        #Store the last user and their ID after sorting
        self.lastUser = ''
        self.lastUserId = ''
        # Request methods PUT, POST, PATCH, DELETE needs access token
        # which needs to be passed with "Authorization" header as Bearer token.
        self.headers = {'Authorization': 'Bearer aca1c63e89fb06b3dd05b3d5ef3d7a516fb6892896774873bf441c4764baa31f'}
        #What we will set the new name of the person we update to
        self.newName = {'name': 'Sally Smith'}

    # 1. Retrieve page 3 of the list of all users.
    def get_page_three(self):
        self.pageThreeUsers = requests.get('https://gorest.co.in/public/v2/users?page=3')
        # 2. Using a logger, log the total number of pages from the previous request.
        pages = self.pageThreeUsers.headers['x-pagination-total']
        logging.info('Total number of pages from the previous request: %s' % pages)
        return self.pageThreeUsers

    # 3. Sort the retrieved user list by name.
    def sort_user_list(self):
        self.sortedNames = self.pageThreeUsers.json()

        #Log list of users before sorting
        logging.info('Page 3 users before sorting')
        for person in self.sortedNames:
            logging.info('%s' % person['name'])

        #sorts the list of users on page 3 bu the values of their
        #name key
        self.sortedNames.sort(key = lambda json: json['name'])

        #Log list of users after sorting
        logging.info('Page 3 users after sorting')
        for person in self.sortedNames:
            logging.info('%s' % person['name'])

        # 4. After sorting, log the name of the last user.
        self.lastUser = self.sortedNames[len(self.sortedNames) - 1]['name']
        logging.info('The last user after sorting is: %s' % self.lastUser)

        return self.sortedNames

    #5. Update that user's name to a new value and use the correct http method to save it.
    def update_last_user_name(self):
        #gets the id of the last user after we've sorted it
        self.lastUserId = self.sortedNames[len(self.sortedNames) - 1]['id']
        updateUrl = 'https://gorest.co.in/public/v2/users/' + str(self.lastUserId)
        update = requests.put(updateUrl, data=self.newName, headers=self.headers)
        return update

    # 6. Delete that user.
    def delete_last_user(self):
        deleteUrl = 'https://gorest.co.in/public/v2/users/' + str(self.lastUserId)
        delete = requests.delete(deleteUrl, headers=self.headers)
        return delete

    # 7. Attempt to retrieve a nonexistent user with ID 5555. Log the resulting http response code.
    def retrieve_non_existing(self):
        nonExistingUser = requests.get('https://gorest.co.in/public/v2/users/5555')
        logging.info("The response code when trying to GET a non-existing user is: %s", str(nonExistingUser.status_code))
        return nonExistingUser


