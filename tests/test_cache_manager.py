import unittest
from src.services.project_scanner.cache_manager import CacheManager


class TestCacheManager(unittest.TestCase):
    """Test cases for CacheManager."""

    def setUp(self) -> None:
        """Set up a new CacheManager instance before each test."""
        self.cache_manager = CacheManager()

    def test_initial_state(self):
        """Test that the cache is initially empty."""
        self.assertIsNone(self.cache_manager.get(), "Cache should be empty initially.")

    def test_set_and_get(self):
        """Test setting and retrieving cached data."""
        test_data = {"key": "value"}
        self.cache_manager.set(test_data)
        self.assertEqual(self.cache_manager.get(), test_data, "Cache should return the correct data.")

    def test_clear_cache(self):
        """Test clearing the cache."""
        test_data = "temporary data"
        self.cache_manager.set(test_data)
        self.cache_manager.clear()
        self.assertIsNone(self.cache_manager.get(), "Cache should be empty after clearing.")

    def test_overwrite_cache(self):
        """Test overwriting cached data."""
        first_data = "first data"
        second_data = "second data"
        self.cache_manager.set(first_data)
        self.assertEqual(self.cache_manager.get(), first_data, "Cache should return the first data.")
        self.cache_manager.set(second_data)
        self.assertEqual(self.cache_manager.get(), second_data, "Cache should return the second data.")

    def test_refresh_cache(self):
        """Test refreshing the cache with new data."""
        old_data = {"old": "data"}
        new_data = {"new": "data"}
        self.cache_manager.set(old_data)
        self.assertEqual(self.cache_manager.get(), old_data, "Cache should initially hold the old data.")
        self.cache_manager.set(new_data)
        self.assertEqual(self.cache_manager.get(), new_data, "Cache should update with the new data.")


if __name__ == "__main__":
    unittest.main()
