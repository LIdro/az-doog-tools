### doog_file:
Manages Doogarey files and task attachments
List files, attach files/URLs to tasks, manage task attachments
Essential for organizing project resources and task documentation
usage:
~~~json
{
    "thoughts": [
        "User wants to attach a file to their task",
        "I'll use the file tool to attach it"
    ],
    "tool_name": "doog_file",
    "tool_args": {
        "action": "attach_to_task",
        "task_id": "task-123",
        "file_id": "file-456"
    }
}
~~~

Actions available:
- **list**: List all user files
- **upload**: Upload file (requires: file_path or file_name) - Limited implementation
- **attach_to_task**: Attach file to task (requires: task_id, file_id)
- **add_url_to_task**: Add URL attachment to task (requires: task_id, url, optional: name)
- **remove_task_attachment**: Remove attachment from task (requires: task_id, attachment_id)
- **get_task_attachments**: List all task attachments (requires: task_id)