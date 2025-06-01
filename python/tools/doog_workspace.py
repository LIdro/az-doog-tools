import json
import requests
import asyncio
from typing import Dict, Any, Optional, List
from python.helpers.tool import Tool, Response

class DoogWorkspaceTool(Tool):
    """
    Tool for managing Doogarey workspaces.
    Handles workspace creation, listing, updating, and member management.
    """

    async def execute(self, **kwargs) -> Response:
        """Execute workspace operations based on the action specified."""
        
        action = self.args.get("action")
        if not action:
            return Response(message="Error: 'action' parameter is required", break_loop=False)

        try:
            if action == "create":
                return await self._create_workspace()
            elif action == "list":
                return await self._list_workspaces()
            elif action == "get":
                return await self._get_workspace()
            elif action == "update":
                return await self._update_workspace()
            elif action == "delete":
                return await self._delete_workspace()
            elif action == "get_members":
                return await self._get_workspace_members()
            elif action == "invite_member":
                return await self._invite_workspace_member()
            elif action == "remove_member":
                return await self._remove_workspace_member()
            else:
                return Response(
                    message=f"Error: Unknown action '{action}'. Available actions: create, list, get, update, delete, get_members, invite_member, remove_member",
                    break_loop=False
                )
                
        except Exception as e:
            return Response(message=f"Error executing workspace action: {str(e)}", break_loop=False)

    async def _create_workspace(self) -> Response:
        """Create a new workspace."""
        name = self.args.get("name")
        if not name:
            return Response(message="Error: 'name' parameter is required for creating a workspace", break_loop=False)
        
        description = self.args.get("description", "")
        
        # Get API URL from environment or use default
        api_url = self._get_api_url()
        
        try:
            response = requests.post(
                f"{api_url}/workspace/create",
                json={"name": name, "description": description},
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                workspace = response.json()
                return Response(
                    message=f"Successfully created workspace '{workspace['name']}' (ID: {workspace['id']})",
                    break_loop=False
                )
            else:
                return Response(
                    message=f"Error creating workspace: {response.status_code} - {response.text}",
                    break_loop=False
                )
                
        except requests.exceptions.RequestException as e:
            return Response(message=f"Network error creating workspace: {str(e)}", break_loop=False)

    async def _list_workspaces(self) -> Response:
        """List all workspaces for the current user."""
        api_url = self._get_api_url()
        
        try:
            response = requests.get(
                f"{api_url}/workspace/list",
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                workspaces = response.json()
                if not workspaces:
                    return Response(message="No workspaces found", break_loop=False)
                
                workspace_list = []
                for ws in workspaces:
                    workspace_list.append(
                        f"- {ws['name']} (ID: {ws['id']}) - Owner: {ws.get('ownerEmail', 'Unknown')}"
                    )
                
                return Response(
                    message=f"Found {len(workspaces)} workspace(s):\n" + "\n".join(workspace_list),
                    break_loop=False
                )
            else:
                return Response(
                    message=f"Error listing workspaces: {response.status_code} - {response.text}",
                    break_loop=False
                )
                
        except requests.exceptions.RequestException as e:
            return Response(message=f"Network error listing workspaces: {str(e)}", break_loop=False)

    async def _get_workspace(self) -> Response:
        """Get details of a specific workspace."""
        workspace_id = self.args.get("workspace_id")
        if not workspace_id:
            return Response(message="Error: 'workspace_id' parameter is required", break_loop=False)
        
        api_url = self._get_api_url()
        
        try:
            response = requests.get(
                f"{api_url}/workspace/{workspace_id}",
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                workspace = response.json()
                return Response(
                    message=f"Workspace Details:\n"
                           f"Name: {workspace['name']}\n"
                           f"ID: {workspace['id']}\n"
                           f"Description: {workspace.get('description', 'None')}\n"
                           f"Owner: {workspace.get('ownerEmail', 'Unknown')}\n"
                           f"Created: {workspace.get('createdAt', 'Unknown')}",
                    break_loop=False
                )
            else:
                return Response(
                    message=f"Error getting workspace: {response.status_code} - {response.text}",
                    break_loop=False
                )
                
        except requests.exceptions.RequestException as e:
            return Response(message=f"Network error getting workspace: {str(e)}", break_loop=False)

    async def _update_workspace(self) -> Response:
        """Update workspace details."""
        workspace_id = self.args.get("workspace_id")
        if not workspace_id:
            return Response(message="Error: 'workspace_id' parameter is required", break_loop=False)
        
        name = self.args.get("name")
        description = self.args.get("description")
        user_email = self.args.get("user_email")
        
        if not name and description is None:
            return Response(message="Error: Either 'name' or 'description' must be provided", break_loop=False)
        
        api_url = self._get_api_url()
        
        update_data = {}
        if name:
            update_data["name"] = name
        if description is not None:
            update_data["description"] = description
        
        try:
            response = requests.put(
                f"{api_url}/workspace/{workspace_id}",
                json=update_data,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                workspace = response.json()
                return Response(
                    message=f"Successfully updated workspace '{workspace['name']}' (ID: {workspace['id']})",
                    break_loop=False
                )
            else:
                return Response(
                    message=f"Error updating workspace: {response.status_code} - {response.text}",
                    break_loop=False
                )
                
        except requests.exceptions.RequestException as e:
            return Response(message=f"Network error updating workspace: {str(e)}", break_loop=False)

    async def _delete_workspace(self) -> Response:
        """Delete a workspace."""
        workspace_id = self.args.get("workspace_id")
        if not workspace_id:
            return Response(message="Error: 'workspace_id' parameter is required", break_loop=False)
        
        api_url = self._get_api_url()
        
        try:
            response = requests.delete(
                f"{api_url}/workspace/{workspace_id}",
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                return Response(
                    message=f"Successfully deleted workspace (ID: {workspace_id})",
                    break_loop=False
                )
            else:
                return Response(
                    message=f"Error deleting workspace: {response.status_code} - {response.text}",
                    break_loop=False
                )
                
        except requests.exceptions.RequestException as e:
            return Response(message=f"Network error deleting workspace: {str(e)}", break_loop=False)

    async def _get_workspace_members(self) -> Response:
        """Get members of a workspace."""
        workspace_id = self.args.get("workspace_id")
        if not workspace_id:
            return Response(message="Error: 'workspace_id' parameter is required", break_loop=False)
        
        api_url = self._get_api_url()
        
        try:
            response = requests.get(
                f"{api_url}/workspace-user/list/{workspace_id}",
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                members = response.json()
                if not members:
                    return Response(message="No members found in this workspace", break_loop=False)
                
                member_list = []
                for member in members:
                    member_list.append(
                        f"- {member['userName']} ({member['userEmail']}) - Role: {member.get('role', 'member')}"
                    )
                
                return Response(
                    message=f"Workspace members ({len(members)}):\n" + "\n".join(member_list),
                    break_loop=False
                )
            else:
                return Response(
                    message=f"Error getting workspace members: {response.status_code} - {response.text}",
                    break_loop=False
                )
                
        except requests.exceptions.RequestException as e:
            return Response(message=f"Network error getting workspace members: {str(e)}", break_loop=False)

    async def _invite_workspace_member(self) -> Response:
        """Invite a member to a workspace."""
        workspace_id = self.args.get("workspace_id")
        user_email = self.args.get("user_email")
        
        if not workspace_id or not user_email:
            return Response(
                message="Error: Both 'workspace_id' and 'user_email' parameters are required",
                break_loop=False
            )
        
        api_url = self._get_api_url()
        
        try:
            response = requests.post(
                f"{api_url}/workspace-user/{workspace_id}/invite",
                json={"userEmail": user_email},
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                member = response.json()
                return Response(
                    message=f"Successfully invited {user_email} to workspace",
                    break_loop=False
                )
            else:
                return Response(
                    message=f"Error inviting member: {response.status_code} - {response.text}",
                    break_loop=False
                )
                
        except requests.exceptions.RequestException as e:
            return Response(message=f"Network error inviting member: {str(e)}", break_loop=False)

    async def _remove_workspace_member(self) -> Response:
        """Remove a member from a workspace."""
        workspace_id = self.args.get("workspace_id")
        user_email = self.args.get("user_email")
        
        if not workspace_id or not user_email:
            return Response(
                message="Error: Both 'workspace_id' and 'user_email' parameters are required",
                break_loop=False
            )
        
        api_url = self._get_api_url()
        
        try:
            response = requests.delete(
                f"{api_url}/workspace-user/{workspace_id}/user/{user_email}",
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                return Response(
                    message=f"Successfully removed {user_email} from workspace",
                    break_loop=False
                )
            else:
                return Response(
                    message=f"Error removing member: {response.status_code} - {response.text}",
                    break_loop=False
                )
                
        except requests.exceptions.RequestException as e:
            return Response(message=f"Network error removing member: {str(e)}", break_loop=False)

    def _get_api_url(self) -> str:
        """Get the API URL from environment or use default."""
        # This should be configurable based on the environment
        # For now, we'll use a default that can be overridden
        return self.args.get("api_url", "http://localhost:3000")

    async def before_execution(self, **kwargs):
        self.log = self.agent.context.log.log(
            type="tool", 
            heading=f"{self.agent.agent_name}: Using Doogarey Workspace Tool", 
            content="", 
            kvps=self.args
        )

    async def after_execution(self, response: Response, **kwargs):
        self.agent.hist_add_tool_result(self.name, response.message)
        self.log.update(content=response.message)
