#!/usr/bin/env python3
"""
Simple test script to verify the task_store implementation.
Run this to ensure Redis connection works and basic operations succeed.
"""

import os
import sys

# Set environment variables if not already set (for testing)
if 'REDIS_HOST' not in os.environ:
    os.environ['REDIS_HOST'] = 'localhost'
if 'REDIS_PORT' not in os.environ:
    os.environ['REDIS_PORT'] = '6379'

from task_store import task_store

def test_task_store():
    print("Testing TaskStore implementation...\n")

    # Test 1: Set and get
    print("Test 1: Set and get task_id")
    test_stt_id = "test-uuid-12345"
    test_task_id = "celery-task-67890"

    task_store.set_task_id(test_stt_id, test_task_id)
    retrieved_task_id = task_store.get_task_id(test_stt_id)

    assert retrieved_task_id == test_task_id, f"Expected {test_task_id}, got {retrieved_task_id}"
    print(f"✓ Successfully stored and retrieved task_id: {retrieved_task_id}\n")

    # Test 2: Check exists
    print("Test 2: Check if task exists")
    exists = task_store.exists(test_stt_id)
    assert exists, "Task should exist"
    print(f"✓ Task exists check: {exists}\n")

    # Test 3: Get non-existent task
    print("Test 3: Get non-existent task")
    non_existent = task_store.get_task_id("non-existent-uuid")
    assert non_existent is None, f"Expected None, got {non_existent}"
    print(f"✓ Non-existent task returns None\n")

    # Test 4: Get all tasks
    print("Test 4: Get all active tasks")
    all_tasks = task_store.get_all_tasks()
    assert test_stt_id in all_tasks, "Test task should be in all_tasks"
    print(f"✓ Found {len(all_tasks)} active task(s)\n")

    # Test 5: Delete task
    print("Test 5: Delete task")
    deleted = task_store.delete_task(test_stt_id)
    assert deleted, "Delete should return True"
    exists_after_delete = task_store.exists(test_stt_id)
    assert not exists_after_delete, "Task should not exist after deletion"
    print(f"✓ Task successfully deleted\n")

    # Test 6: TTL extension
    print("Test 6: TTL extension")
    task_store.set_task_id(test_stt_id, test_task_id)
    extended = task_store.extend_ttl(test_stt_id)
    assert extended, "TTL extension should succeed"
    print(f"✓ TTL successfully extended\n")

    # Cleanup
    task_store.delete_task(test_stt_id)

    print("=" * 50)
    print("All tests passed! ✓")
    print("=" * 50)

if __name__ == "__main__":
    try:
        test_task_store()
    except Exception as e:
        print(f"✗ Test failed: {e}")
        sys.exit(1)
