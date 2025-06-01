### doog_workspace:
Manages Doogarey workspaces for project collaboration
Create, list, update, delete workspaces and manage members
Essential for organizing projects and team collaboration in Doogarey
usage:
~~~json
{
    "thoughts": [
        "User wants to create a new workspace for their project",
        "I need to use the doog_workspace tool to create it"
    ],
    "tool_name": "doog_workspace",
    "tool_args": {
        "action": "create",
        "name": "My New Workspace",
        "description": "A workspace for my project"
    }
}
~~~

Actions available:
- **create**: Create new workspace (requires: name, optional: description)
- **list**: List all user's workspaces
- **get**: Get workspace details (requires: workspace_id)  
- **update**: Update workspace (requires: workspace_id, optional: name, description, user_email)
- **delete**: Delete workspace (requires: workspace_id)
- **get_members**: List workspace members (requires: workspace_id)
- **invite_member**: Invite user to workspace (requires: workspace_id, user_email)
- **remove_member**: Remove user from workspace (requires: workspace_id, user_email)