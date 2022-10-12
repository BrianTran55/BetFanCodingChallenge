import unittest
import gorest
import requests
#import json

class MyTestCase(unittest.TestCase):
    testGoRest = gorest.GoRest()

    #Test part 1: Retrieve page 3 of the list of all users.
    def test_a_retrieve_page_three(self):
        #call our created function to store the third
        #page of users from gorest
        pageThree = self.testGoRest.get_page_three()

        #Check that the request's status code is 200 because
        #that signals a successful request with no errors
        self.assertEqual(pageThree.status_code, 200)
        #Check that our request returned the 3rd page of users
        self.assertEqual(pageThree.json(), requests.get('https://gorest.co.in/public/v2/users?page=3').json())

    #Test part 3: Sort the retrieved user list by name.
    def test_b_sort_users(self):
        #call our created function to store the sorted
        #page 3 users
        sortedNames = self.testGoRest.sort_user_list()

        #get the users from page 3 and sort them so that
        #we can check that our function successfully sorts
        #the users by name
        compareNames = requests.get('https://gorest.co.in/public/v2/users?page=3').json()
        compareNames.sort(key = lambda json: json['name'])
        self.assertEqual(sortedNames, compareNames)


    #Test part 5: Update that user's name to a new value and use the correct http method to save it.
    def test_c_update_name(self):
        #store the response after updating the last user's name
        updateName = self.testGoRest.update_last_user_name()
        #check that the response code was 200, representing
        #a successful update
        self.assertEqual(updateName.status_code, 200)
        #Check that the name of the response is Sally Smith
        #because that is what we wanted to change it to
        self.assertEqual(updateName.json()['name'], 'Sally Smith')

    # Test part 6: Delete that user
    def test_d_delete_last_user(self):
        # Store response for deleting the last user
        deleteLast = self.testGoRest.delete_last_user()

        # Check that the reponse code was 204, representing
        # a successful delete
        self.assertEqual(deleteLast.status_code, 204)

        # check that that user no longer exists
        # We will try to get that user and the response code
        # should be 404
        deletedUrl = 'https://gorest.co.in/public/v2/users/' + str(self.testGoRest.lastUserId)
        tryToGetDeleted = requests.get(deletedUrl)

        self.assertEqual(tryToGetDeleted.status_code, 404)


    #Test part 7: Attempt to retrieve a nonexistent user with ID 5555. Log the resulting http response code.
    def test_e_retrieve_nonexisiting_user(self):
        #Store the response for trying to retrieve a nonexistent user
        tryToGetNonexisting = self.testGoRest.retrieve_non_existing()

        #Check that the returned status code is 404 because that is
        #what trying to get a user that is not in the system should return
        self.assertEqual(tryToGetNonexisting.status_code, 404)

