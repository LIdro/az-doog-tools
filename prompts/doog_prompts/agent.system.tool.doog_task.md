### doog_task:
Manages Doogarey tasks within projects
Create, list, update, assign, and track tasks through different stages
Core tool for task management and project execution in Doogarey
usage:
~~~json
{
    "thoughts": [
        "User wants to create a task for their project",
        "I'll create it with appropriate status and priority"
    ],
    "tool_name": "doog_task",
    "tool_args": {
        "action": "create",
        "title": "Design landing page",
        "project_id": "project-123",
        "description": "Create responsive landing page design",
        "status": "TODO",
        "priority": "HIGH",
        "user_email": "user@example.com",
        "position": 0
    }
}
~~~

Actions available:
- **create**: Create new task (requires: title, project_id, optional: description, status, priority, user_email, position, due_date)
- **list**: List tasks in project (requires: project_id)
- **get**: Get task details (requires: task_id)
- **update**: Update task (requires: task_id, optional: title, description, status, priority, user_email, position, due_date)
- **update_status**: Change task status (requires: task_id, status)
- **update_assignee**: Assign/unassign task (requires: task_id, optional: user_email)
- **update_priority**: Change task priority (requires: task_id, priority)
- **delete**: Delete task (requires: task_id)
- **get_attachments**: List task attachments (requires: task_id)

Valid status values: TODO, IN_PROGRESS, DONE
Valid priority values: LOW, MEDIUM, HIGH, URGENT