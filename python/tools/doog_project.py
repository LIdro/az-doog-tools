import json
import requests
import asyncio
from typing import Dict, Any, Optional, List
from python.helpers.tool import Tool, Response

class DoogProjectTool(Tool):
    """
    Tool for managing Doogarey projects.
    Handles project creation, listing, updating, and deletion within workspaces.
    """

    async def execute(self, **kwargs) -> Response:
        """Execute project operations based on the action specified."""
        
        action = self.args.get("action")
        if not action:
            return Response(message="Error: 'action' parameter is required", break_loop=False)

        try:
            if action == "create":
                return await self._create_project()
            elif action == "list":
                return await self._list_projects()
            elif action == "get":
                return await self._get_project()
            elif action == "update":
                return await self._update_project()
            elif action == "delete":
                return await self._delete_project()
            else:
                return Response(
                    message=f"Error: Unknown action '{action}'. Available actions: create, list, get, update, delete",
                    break_loop=False
                )
                
        except Exception as e:
            return Response(message=f"Error executing project action: {str(e)}", break_loop=False)

    async def _create_project(self) -> Response:
        """Create a new project."""
        name = self.args.get("name")
        workspace_id = self.args.get("workspace_id")
        
        if not name or not workspace_id:
            return Response(
                message="Error: Both 'name' and 'workspace_id' parameters are required for creating a project",
                break_loop=False
            )
        
        description = self.args.get("description", "")
        icon = self.args.get("icon", "📁")
        slug = self.args.get("slug", name.lower().replace(" ", "-"))
        
        api_url = self._get_api_url()
        
        try:
            response = requests.post(
                f"{api_url}/project/create",
                json={
                    "name": name,
                    "description": description,
                    "workspaceId": workspace_id,
                    "icon": icon,
                    "slug": slug
                },
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                project = response.json()
                return Response(
                    message=f"Successfully created project '{project['name']}' (ID: {project['id']}) in workspace {workspace_id}",
                    break_loop=False
                )
            else:
                return Response(
                    message=f"Error creating project: {response.status_code} - {response.text}",
                    break_loop=False
                )
                
        except requests.exceptions.RequestException as e:
            return Response(message=f"Network error creating project: {str(e)}", break_loop=False)

    async def _list_projects(self) -> Response:
        """List all projects in a workspace."""
        workspace_id = self.args.get("workspace_id")
        if not workspace_id:
            return Response(message="Error: 'workspace_id' parameter is required", break_loop=False)
        
        api_url = self._get_api_url()
        
        try:
            response = requests.get(
                f"{api_url}/project/list/{workspace_id}",
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                projects = response.json()
                if not projects:
                    return Response(message="No projects found in this workspace", break_loop=False)
                
                project_list = []
                for project in projects:
                    project_list.append(
                        f"- {project.get('icon', '📁')} {project['name']} (ID: {project['id']}) - {project.get('description', 'No description')}"
                    )
                
                return Response(
                    message=f"Found {len(projects)} project(s) in workspace:\n" + "\n".join(project_list),
                    break_loop=False
                )
            else:
                return Response(
                    message=f"Error listing projects: {response.status_code} - {response.text}",
                    break_loop=False
                )
                
        except requests.exceptions.RequestException as e:
            return Response(message=f"Network error listing projects: {str(e)}", break_loop=False)

    async def _get_project(self) -> Response:
        """Get details of a specific project."""
        project_id = self.args.get("project_id")
        workspace_id = self.args.get("workspace_id")
        
        if not project_id or not workspace_id:
            return Response(
                message="Error: Both 'project_id' and 'workspace_id' parameters are required",
                break_loop=False
            )
        
        api_url = self._get_api_url()
        
        try:
            response = requests.get(
                f"{api_url}/project/{project_id}?workspaceId={workspace_id}",
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                project = response.json()
                return Response(
                    message=f"Project Details:\n"
                           f"Name: {project['name']}\n"
                           f"ID: {project['id']}\n"
                           f"Icon: {project.get('icon', '📁')}\n"
                           f"Description: {project.get('description', 'None')}\n"
                           f"Workspace ID: {project['workspaceId']}\n"
                           f"Slug: {project.get('slug', 'N/A')}\n"
                           f"Created: {project.get('createdAt', 'Unknown')}",
                    break_loop=False
                )
            else:
                return Response(
                    message=f"Error getting project: {response.status_code} - {response.text}",
                    break_loop=False
                )
                
        except requests.exceptions.RequestException as e:
            return Response(message=f"Network error getting project: {str(e)}", break_loop=False)

    async def _update_project(self) -> Response:
        """Update project details."""
        project_id = self.args.get("project_id")
        workspace_id = self.args.get("workspace_id")
        
        if not project_id or not workspace_id:
            return Response(
                message="Error: Both 'project_id' and 'workspace_id' parameters are required",
                break_loop=False
            )
        
        name = self.args.get("name")
        description = self.args.get("description")
        icon = self.args.get("icon")
        slug = self.args.get("slug")
        
        if not any([name, description is not None, icon, slug]):
            return Response(
                message="Error: At least one of 'name', 'description', 'icon', or 'slug' must be provided",
                break_loop=False
            )
        
        api_url = self._get_api_url()
        
        update_data = {"workspaceId": workspace_id}
        if name:
            update_data["name"] = name
        if description is not None:
            update_data["description"] = description
        if icon:
            update_data["icon"] = icon
        if slug:
            update_data["slug"] = slug
        
        try:
            response = requests.put(
                f"{api_url}/project/{project_id}",
                json=update_data,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                project = response.json()
                return Response(
                    message=f"Successfully updated project '{project.get('name', project_id)}' (ID: {project_id})",
                    break_loop=False
                )
            else:
                return Response(
                    message=f"Error updating project: {response.status_code} - {response.text}",
                    break_loop=False
                )
                
        except requests.exceptions.RequestException as e:
            return Response(message=f"Network error updating project: {str(e)}", break_loop=False)

    async def _delete_project(self) -> Response:
        """Delete a project."""
        project_id = self.args.get("project_id")
        if not project_id:
            return Response(message="Error: 'project_id' parameter is required", break_loop=False)
        
        api_url = self._get_api_url()
        
        try:
            response = requests.delete(
                f"{api_url}/project/{project_id}",
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                return Response(
                    message=f"Successfully deleted project (ID: {project_id})",
                    break_loop=False
                )
            else:
                return Response(
                    message=f"Error deleting project: {response.status_code} - {response.text}",
                    break_loop=False
                )
                
        except requests.exceptions.RequestException as e:
            return Response(message=f"Network error deleting project: {str(e)}", break_loop=False)

    def _get_api_url(self) -> str:
        """Get the API URL from environment or use default."""
        return self.args.get("api_url", "http://localhost:3000")

    async def before_execution(self, **kwargs):
        self.log = self.agent.context.log.log(
            type="tool", 
            heading=f"{self.agent.agent_name}: Using Doogarey Project Tool", 
            content="", 
            kvps=self.args
        )

    async def after_execution(self, response: Response, **kwargs):
        self.agent.hist_add_tool_result(self.name, response.message)
        self.log.update(content=response.message)
