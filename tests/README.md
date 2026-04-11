"""
# Test Suite Documentation

This directory contains comprehensive tests for the Music Recommender System.

## Test Structure

The test suite mirrors the source code structure:

### test_song.py
Tests for the `Song` dataclass:
- Song creation and initialization
- `from_dict()` class method
- String representation
- Different genres, moods, and attribute ranges

### test_user_preferences.py
Tests for the `UserProfile` dataclass:
- UserProfile creation and initialization
- `from_dict()` class method
- String representation with different acoustic preferences
- Different genres, moods, and energy levels

### test_scoring_algorithms.py
Tests for the scoring algorithms:
- `WeightedGenreScorer`: Tests for weighted combination scoring
- `SimpleGenreScorer`: Tests for simple genre/mood matching
- `EnergyFocusedScorer`: Tests for energy-prioritized scoring
- Cross-algorithm comparison tests

**Note:** Uses test classes for organizing related tests, but each algorithm has its own class for clarity.

### test_recommender.py
Tests for the `Recommender` class:
- Initialization with default and custom algorithms
- Recommendation ranking and sorting
- Algorithm switching at runtime
- Different user preferences and recommendations
- CSV loading and integration
- Explanations and edge cases

### conftest.py
Pytest configuration file with shared fixtures:
- `sample_songs`: Standard test song set
- `pop_user`: Pop music lover fixture
- `jazz_user`: Jazz music lover fixture
- `rock_user`: Rock music lover fixture
- `lofi_user`: Lofi music lover fixture

## Running Tests

Run all tests:
```bash
pytest
```

Run tests for a specific module:
```bash
pytest tests/test_song.py
pytest tests/test_user_preferences.py
pytest tests/test_scoring_algorithms.py
pytest tests/test_recommender.py
```

Run with verbose output:
```bash
pytest -v
```

Run with coverage report:
```bash
pytest --cov=src
```

Run specific test:
```bash
pytest tests/test_recommender.py::test_pop_fan_recommendations -v
```

## Test Categories

### Unit Tests
- Individual class instantiation and methods
- Data validation and type checking
- Algorithm scoring behavior

### Integration Tests
- Recommender with different songs and users
- CSV loading and processing
- Algorithm switching and comparison

### Edge Cases
- Empty recommendations (k=0)
- k larger than available songs
- Different user preferences affecting results
- Acoustic preference effects

## Coverage

The test suite aims for comprehensive coverage of:
- All public methods and functions
- Different user preference combinations
- Various songs and musical attributes
- Scoring algorithm behavior
- Integration between components
"""
