import pytest
from datetime import datetime, timedelta
from src.validators.task_validator import TaskValidator

@pytest.fixture
def validator(): return TaskValidator()

def test_title_cannot_be_none(validator): assert validator.is_title_valid(None) == False
def test_title_cannot_be_empty(validator): assert validator.is_title_valid("") == False
def test_title_cannot_be_whitespace(validator): assert validator.is_title_valid("   ") == False
def test_due_date_cannot_be_none(validator): assert validator.is_due_date_valid(None) == False
def test_due_date_cannot_be_in_past(validator):
    assert validator.is_due_date_valid(datetime.utcnow() - timedelta(days=1)) == False

def test_title_max_length(validator): 
    assert validator.is_title_valid("a" * 101) == False

def test_due_date_too_far(validator): 
    assert validator.is_due_date_valid(datetime.utcnow() + timedelta(days=732)) == False

def test_priority_invalid_type(validator): 
    assert validator.is_priority_valid("1") == False

def test_priority_invalid_range(validator): 
    assert validator.is_priority_valid(5) == False

def test_priority_valid(validator): 
    assert validator.is_priority_valid(2) == True

def test_validate_all_valid(validator):
    assert validator.validate("Good", datetime.utcnow() + timedelta(days=5), 1) == []

def test_validate_errors(validator):
    errors = validator.validate("", datetime.utcnow() - timedelta(days=1), 5)
    assert len(errors) == 3
