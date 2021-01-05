# I keep getting the error of ModuleNotFoundError: No module named 'blog' even though it found it...
# I do not know why it keep happening. Will come back later to figure it out.
import blog
import unittest
class TestRoutes(unittest.TestCase):
    def test_about(self):
        tester = blog.test_client(self)



if __name__ == '__main__':
    unittest.main()