### doog_project:
Manages Doogarey projects within workspaces
Create, list, update, delete projects for organizing tasks and work
Essential for structuring work within Doogarey workspaces
usage:
~~~json
{
    "thoughts": [
        "User wants to create a project for their marketing campaign",
        "I need to create it in their workspace"
    ],
    "tool_name": "doog_project",
    "tool_args": {
        "action": "create",
        "name": "Marketing Campaign Q1",
        "workspace_id": "workspace-123",
        "description": "Q1 marketing campaign project",
        "icon": "📊",
        "slug": "marketing-q1"
    }
}
~~~

Actions available:
- **create**: Create new project (requires: name, workspace_id, optional: description, icon, slug)
- **list**: List projects in workspace (requires: workspace_id)
- **get**: Get project details (requires: project_id, workspace_id)
- **update**: Update project (requires: project_id, workspace_id, optional: name, description, icon, slug)
- **delete**: Delete project (requires: project_id)