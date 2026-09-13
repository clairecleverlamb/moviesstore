from django.test import TestCase
from django.urls import reverse


class AboutPageTests(TestCase):
    def test_about_page_explains_the_store(self):
        response = self.client.get(reverse('home.about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'About GT Movies Store')
        self.assertContains(response, 'Purpose')
        self.assertContains(response, 'web application')

    def test_home_page_links_to_about(self):
        response = self.client.get(reverse('home.index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'GT Movie Store')
        self.assertContains(response, reverse('home.about'))
