import pytest
from datetime import datetime
from src.services.task_service import TaskService, TaskRepository, NotificationService, Task

@pytest.fixture
def mock_repo(mocker):
    return mocker.Mock(spec=TaskRepository)

@pytest.fixture
def mock_notifier(mocker):
    return mocker.Mock(spec=NotificationService)

@pytest.fixture
def service(mock_repo, mock_notifier):
    return TaskService(mock_repo, mock_notifier)

@pytest.fixture
def sample_task():
    return Task(id=1, title="Test", priority=1, due_date=datetime.utcnow(), creator_id=10)

# ================= 1. create_task =================
def test_create_task_happy_path(service, mock_repo):
    mock_repo.save.return_value = Task(id=1, title="Test", priority=1, due_date=datetime.utcnow(), creator_id=10)
    result = service.create_task("Test", 1, datetime.utcnow(), 10)
    assert result.id == 1

def test_create_task_edge_case(service, mock_repo):
    with pytest.raises(ValueError, match="Title cannot be empty"):
        service.create_task("   ", 1, datetime.utcnow(), 10)
    mock_repo.save.assert_not_called()

def test_create_task_mock_verification(service, mock_repo):
    due = datetime.utcnow()
    service.create_task("New Task", 2, due, 42)
    mock_repo.save.assert_called_once()
    saved_task = mock_repo.save.call_args[0][0]
    assert saved_task.title == "New Task"
    assert saved_task.creator_id == 42

# ================= 2. assign_task =================
def test_assign_task_happy_path(service, mock_repo, mock_notifier, sample_task):
    mock_repo.get_by_id.return_value = sample_task
    mock_repo.update.return_value = sample_task
    result = service.assign_task(1, 99)
    assert result.assignee_id == 99

def test_assign_task_edge_case(service, mock_repo, mock_notifier):
    mock_repo.get_by_id.return_value = None
    with pytest.raises(ValueError, match="Task 1 not found"):
        service.assign_task(1, 99)
    mock_notifier.send_assignment_notification.assert_not_called()

def test_assign_task_mock_verification(service, mock_repo, mock_notifier, sample_task):
    mock_repo.get_by_id.return_value = sample_task
    service.assign_task(1, 99)
    mock_repo.update.assert_called_once_with(sample_task)
    mock_notifier.send_assignment_notification.assert_called_once_with(1, 99)

# ================= 3. get_tasks_by_assignee =================
def test_get_tasks_happy_path(service, mock_repo, sample_task):
    mock_repo.get_by_assignee.return_value = [sample_task]
    result = service.get_tasks_by_assignee(99)
    assert len(result) == 1
    assert result[0].id == 1

def test_get_tasks_edge_case(service, mock_repo):
    with pytest.raises(ValueError, match="Invalid assignee ID"):
        service.get_tasks_by_assignee(-1)
    mock_repo.get_by_assignee.assert_not_called()

def test_get_tasks_mock_verification(service, mock_repo):
    service.get_tasks_by_assignee(42)
    mock_repo.get_by_assignee.assert_called_once_with(42)

# ================= 4. change_status =================
def test_change_status_happy_path(service, mock_repo, mock_notifier, sample_task):
    mock_repo.get_by_id.return_value = sample_task
    mock_repo.update.return_value = sample_task
    result = service.change_status(1, "DONE")
    assert result.status == "DONE"

def test_change_status_edge_case(service, mock_repo, mock_notifier, sample_task):
    mock_repo.get_by_id.return_value = sample_task
    with pytest.raises(ValueError, match="Invalid status"):
        service.change_status(1, "INVALID_STATUS")
    mock_repo.update.assert_not_called()
    mock_notifier.send_status_change_notification.assert_not_called()

def test_change_status_mock_verification(service, mock_repo, mock_notifier, sample_task):
    mock_repo.get_by_id.return_value = sample_task
    service.change_status(1, "IN_PROGRESS")
    mock_repo.update.assert_called_once_with(sample_task)
    mock_notifier.send_status_change_notification.assert_called_once_with(1, "IN_PROGRESS")