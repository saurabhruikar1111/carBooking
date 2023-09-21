from django.test import SimpleTestCase
from unittest import skip

@skip("Skipping dummy test case")
class Testdummy(SimpleTestCase):
    def test_dummy(self):
        assert 1==2