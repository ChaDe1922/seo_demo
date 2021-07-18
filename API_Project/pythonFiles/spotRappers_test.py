import unittest
from spotRappers import requestAuth, getArtistsRequest

class TestFileName(unittest.TestCase):
       def test_requestAuth(self):
              #Stubs
              CLIENT_ID = '744aee4ee39a4b6787e645452d1d36b4'
              CLIENT_SECRET = '7b72ec76041d4818b061e91ce613d780'
              AUTH_URL = 'https://accounts.spotify.com/api/token'
              
              auth_response, headers = requestAuth(CLIENT_ID, CLIENT_SECRET, AUTH_URL)
              
              #Test1
              self.assertNotEqual(CLIENT_ID, "" )
              self.assertNotEqual(CLIENT_SECRET, "" )
              self.assertNotEqual(AUTH_URL, "" )
              
              #Test2
              self.assertTrue(type(CLIENT_ID) == str)
              self.assertTrue(type(CLIENT_SECRET) == str)
              self.assertTrue(type(AUTH_URL) == str)
              
              self.assertNotEqual(auth_response, "" )
              self.assertNotEqual(headers, "" )
              
              self.assertEqual(auth_response.status_code, 200)
              
              self.assertTrue(type(headers) == dict)
              
       def test_getArtistsRequest(self):
              pass
              
if __name__ == '__main__':
       unittest.main()