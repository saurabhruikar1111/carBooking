from django.test import TestCase,Client
from django.urls import reverse

class TestViews(TestCase):
    
    client = Client()
    def test_project_user_get(self):
        response = self.client.get(reverse("user-view"))
        
        self.assertEqual(response.status_code,201)
            
    def test_project_user_post_missing_data(self):
        response = self.client.post(reverse("user-view"),content_type="application/json")

        self.assertEquals(response.status_code,400)
        
    def test_project_post(self):
        data = {"username":"saurabh","password":"1234"}
        response = self.client.post(reverse("user-view"), data=data, content_type="application/json")
        
        response = self.assertEqual(response.status_code,201)
        
    def test_project_post_wrong_keyname(self):
        data = {"usernaclear":"saurabh","password":"1234"}
        response = self.client.post(reverse("user-view"), data=data, content_type="application/json")
        
        response = self.assertEqual(response.status_code,400)
        
        
        