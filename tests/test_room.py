from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.room_service import room_manager

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_rooms():
    room_manager.rooms.clear()
    yield
    room_manager.rooms.clear()


# ── helpers ──────────────────────────────────────────────────────────────────


def create_room(name='Mission Room', max_users=4) -> dict:
    response = client.post('/rooms', json={'name': name, 'max_users': max_users})
    assert response.status_code == 200
    return response.json()


def join_room(room_code: str, display_name='Alice') -> dict:
    response = client.post(
        f'/rooms/{room_code}/join', json={'display_name': display_name}
    )
    assert response.status_code == 200
    return response.json()


# ── POST /rooms ───────────────────────────────────────────────────────────────


def test_create_room_defaults():
    data = create_room()
    assert data['name'] == 'Mission Room'
    assert data['max_users'] == 4
    assert data['active_users'] == 0
    assert 'room_code' in data


def test_create_room_custom():
    data = create_room(name='Apollo 1', max_users=8)
    assert data['name'] == 'Apollo 1'
    assert data['max_users'] == 8


def test_create_room_code_is_unique():
    room1 = create_room()
    room2 = create_room()
    assert room1['room_code'] != room2['room_code']


def test_create_room_max_users_too_high():
    response = client.post('/rooms', json={'max_users': 9})
    assert response.status_code == 422


def test_create_room_max_users_too_low():
    response = client.post('/rooms', json={'max_users': 0})
    assert response.status_code == 422


# ── GET /rooms/{room_code} ────────────────────────────────────────────────────


def test_get_room_info():
    room = create_room(name='Apollo 1')
    response = client.get(f'/rooms/{room["room_code"]}')
    assert response.status_code == 200
    data = response.json()
    assert data['room_code'] == room['room_code']
    assert data['name'] == 'Apollo 1'


def test_get_room_not_found():
    response = client.get('/rooms/INVALID')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Room not found!'


# ── POST /rooms/{room_code}/join ──────────────────────────────────────────────


def test_join_room():
    room = create_room()
    data = join_room(room['room_code'], display_name='Alice')
    assert data['room_code'] == room['room_code']
    assert data['active_users'] == 1
    assert 'participant_id' in data
    assert 'role' in data


def test_join_room_display_name_too_short():
    room = create_room()
    response = client.post(
        f'/rooms/{room["room_code"]}/join', json={'display_name': ''}
    )
    assert response.status_code == 422


def test_join_room_display_name_too_long():
    room = create_room()
    response = client.post(
        f'/rooms/{room["room_code"]}/join', json={'display_name': 'A' * 41}
    )
    assert response.status_code == 422


def test_join_room_not_found():
    response = client.post('/rooms/INVALID/join', json={'display_name': 'Alice'})
    assert response.status_code == 404
    assert response.json()['detail'] == 'Room not found!'


def test_join_room_active_users_increments():
    room = create_room(max_users=4)
    join_room(room['room_code'], display_name='Alice')
    join_room(room['room_code'], display_name='Bob')
    response = client.get(f'/rooms/{room["room_code"]}')
    assert response.json()['active_users'] == 2


def test_join_room_full():
    room = create_room(max_users=1)
    join_room(room['room_code'], display_name='Alice')
    response = client.post(
        f'/rooms/{room["room_code"]}/join', json={'display_name': 'Bob'}
    )
    assert response.status_code == 400


# ── GET /rooms ────────────────────────────────────────────────────────────────


def test_list_rooms_empty():
    response = client.get('/rooms')
    assert response.status_code == 200
    assert response.json() == []


def test_list_rooms_returns_room_details():
    room = create_room(name='Apollo 1', max_users=6)
    response = client.get('/rooms')
    assert response.status_code == 200

    entry = next(r for r in response.json() if r['room_code'] == room['room_code'])
    assert entry['name'] == 'Apollo 1'
    assert entry['max_users'] == 6
    assert entry['connected_users'] == 0
    assert entry['total_participants'] == 0
    assert entry['is_streaming'] is False
    assert entry['is_inactive'] is False
    assert 'last_activity_at' in entry


def test_list_rooms_reflects_joined_participants():
    room = create_room()
    join_room(room['room_code'], display_name='Alice')

    entry = next(r for r in client.get('/rooms').json() if r['room_code'] == room['room_code'])
    assert entry['connected_users'] == 1
    assert entry['total_participants'] == 1
    assert entry['is_inactive'] is False


# ── DELETE /rooms/inactive ────────────────────────────────────────────────────


def test_cleanup_inactive_rooms_removes_stale_empty_room():
    room = create_room()
    mission_room = room_manager.get_room(room['room_code'])
    mission_room.last_activity_at = datetime.now(timezone.utc) - timedelta(minutes=31)

    response = client.delete('/rooms/inactive')
    assert response.status_code == 200

    data = response.json()
    assert data['removed_count'] == 1
    assert data['removed_rooms'] == [room['room_code']]

    assert client.get(f'/rooms/{room["room_code"]}').status_code == 404


def test_cleanup_inactive_rooms_skips_recent_room():
    room = create_room()

    response = client.delete('/rooms/inactive')
    assert response.status_code == 200

    data = response.json()
    assert data['removed_count'] == 0
    assert data['removed_rooms'] == []

    assert client.get(f'/rooms/{room["room_code"]}').status_code == 200


def test_cleanup_inactive_rooms_skips_room_with_connected_users():
    room = create_room()
    join_room(room['room_code'], display_name='Alice')

    mission_room = room_manager.get_room(room['room_code'])
    mission_room.last_activity_at = datetime.now(timezone.utc) - timedelta(minutes=31)

    response = client.delete('/rooms/inactive')
    assert response.status_code == 200

    data = response.json()
    assert room['room_code'] not in data['removed_rooms']
    assert client.get(f'/rooms/{room["room_code"]}').status_code == 200


def test_cleanup_inactive_rooms_respects_timeout_minutes():
    room = create_room()
    mission_room = room_manager.get_room(room['room_code'])
    mission_room.last_activity_at = datetime.now(timezone.utc) - timedelta(minutes=5)

    response = client.delete('/rooms/inactive?timeout_minutes=10')
    assert response.status_code == 200
    assert room['room_code'] not in response.json()['removed_rooms']

    response = client.delete('/rooms/inactive?timeout_minutes=1')
    assert response.status_code == 200
    assert room['room_code'] in response.json()['removed_rooms']
