import json
import requests
import asyncio
from typing import Dict, Any, Optional, List
from python.helpers.tool import Tool, Response

class DoogTaskTool(Tool):
    """
    Tool for managing Doogarey tasks.
    Handles task creation, listing, updating, status changes, and deletion within projects.
    """

    async def execute(self, **kwargs) -> Response:
        """Execute task operations based on the action specified."""
        
        action = self.args.get("action")
        if not action:
            return Response(message="Error: 'action' parameter is required", break_loop=False)

        try:
            if action == "create":
                return await self._create_task()
            elif action == "list":
                return await self._list_tasks()
            elif action == "get":
                return await self._get_task()
            elif action == "update":
                return await self._update_task()
            elif action == "update_status":
                return await self._update_task_status()
            elif action == "update_assignee":
                return await self._update_task_assignee()
            elif action == "update_priority":
                return await self._update_task_priority()
            elif action == "delete":
                return await self._delete_task()
            elif action == "get_attachments":
                return await self._get_task_attachments()
            else:
                return Response(
                    message=f"Error: Unknown action '{action}'. Available actions: create, list, get, update, update_status, update_assignee, update_priority, delete, get_attachments",
                    break_loop=False
                )
        except Exception as e:
            return Response(message=f"Error executing task action: {str(e)}", break_loop=False)

    async def _create_task(self) -> Response:
        """Create a new task."""
        title = self.args.get("title")
        project_id = self.args.get("project_id")
        
        if not title or not project_id:
            return Response(
                message="Error: Both 'title' and 'project_id' parameters are required for creating a task",
                break_loop=False
            )
        
        description = self.args.get("description", "")
        status = self.args.get("status", "TODO")
        priority = self.args.get("priority", "MEDIUM")
        user_email = self.args.get("user_email", "")
        position = self.args.get("position", 0)
        due_date = self.args.get("due_date")
        
        # Validate status and priority
        valid_statuses = ["TODO", "IN_PROGRESS", "DONE"]
        valid_priorities = ["LOW", "MEDIUM", "HIGH", "URGENT"]
        
        if status not in valid_statuses:
            return Response(
                message=f"Error: Invalid status '{status}'. Valid statuses: {', '.join(valid_statuses)}",
                break_loop=False
            )
        
        if priority not in valid_priorities:
            return Response(
                message=f"Error: Invalid priority '{priority}'. Valid priorities: {', '.join(valid_priorities)}",
                break_loop=False
            )
        
        api_url = self._get_api_url()
        
        task_data = {
            "title": title,
            "description": description,
            "projectId": project_id,
            "userEmail": user_email,
            "status": status,
            "priority": priority,
            "position": int(position)
        }
        
        if due_date:
            task_data["dueDate"] = due_date
        
        try:
            response = requests.post(
                f"{api_url}/task/create",
                json=task_data,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                task = response.json()
                return Response(
                    message=f"Successfully created task '{task['title']}' (ID: {task['id']}) in project {project_id}",
                    break_loop=False
                )
            else:
                return Response(
                    message=f"Error creating task: {response.status_code} - {response.text}",
                    break_loop=False
                )
                
        except requests.exceptions.RequestException as e:
            return Response(message=f"Network error creating task: {str(e)}", break_loop=False)

    async def _list_tasks(self) -> Response:
        """List all tasks in a project."""
        project_id = self.args.get("project_id")
        if not project_id:
            return Response(message="Error: 'project_id' parameter is required", break_loop=False)
        
        api_url = self._get_api_url()
        
        try:
            response = requests.get(
                f"{api_url}/task/list?projectId={project_id}",
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                task_data = response.json()
                
                # Handle the response structure which includes columns
                all_tasks = []
                
                if isinstance(task_data, dict) and 'columns' in task_data:
                    # Extract tasks from columns
                    for column in task_data.get('columns', []):
                        all_tasks.extend(column.get('tasks', []))
                    
                    # Add archived and planned tasks if they exist
                    all_tasks.extend(task_data.get('archivedTasks', []))
                    all_tasks.extend(task_data.get('plannedTasks', []))
                elif isinstance(task_data, list):
                    # Direct list of tasks
                    all_tasks = task_data
                
                if not all_tasks:
                    return Response(message="No tasks found in this project", break_loop=False)
                
                task_list = []
                for task in all_tasks:
                    status_emoji = {"TODO": "📋", "IN_PROGRESS": "🔄", "DONE": "✅"}.get(task.get('status', 'TODO'), "📋")
                    priority_emoji = {"LOW": "🔵", "MEDIUM": "🟡", "HIGH": "🟠", "URGENT": "🔴"}.get(task.get('priority', 'MEDIUM'), "🟡")
                    
                    assignee = task.get('assigneeName') or task.get('userEmail', 'Unassigned')
                    
                    task_list.append(
                        f"- {status_emoji} {priority_emoji} {task['title']} (ID: {task['id']}) - Assigned to: {assignee}"
                    )
                
                return Response(
                    message=f"Found {len(all_tasks)} task(s) in project:\n" + "\n".join(task_list),
                    break_loop=False
                )
            else:
                return Response(
                    message=f"Error listing tasks: {response.status_code} - {response.text}",
                    break_loop=False
                )
                
        except requests.exceptions.RequestException as e:
            return Response(message=f"Network error listing tasks: {str(e)}", break_loop=False)

    async def _get_task(self) -> Response:
        """Get details of a specific task."""
        task_id = self.args.get("task_id")
        if not task_id:
            return Response(message="Error: 'task_id' parameter is required", break_loop=False)
        
        api_url = self._get_api_url()
        
        try:
            response = requests.get(
                f"{api_url}/task/{task_id}",
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                task = response.json()
                assignee = task.get('assigneeName') or task.get('userEmail', 'Unassigned')
                
                return Response(
                    message=f"Task Details:\n"
                           f"Title: {task['title']}\n"
                           f"ID: {task['id']}\n"
                           f"Description: {task.get('description', 'None')}\n"
                           f"Status: {task['status']}\n"
                           f"Priority: {task['priority']}\n"
                           f"Project ID: {task['projectId']}\n"
                           f"Assigned to: {assignee}\n"
                           f"Due Date: {task.get('dueDate', 'Not set')}\n"
                           f"Position: {task.get('position', 0)}\n"
                           f"Created: {task.get('createdAt', 'Unknown')}",
                    break_loop=False
                )
            else:
                return Response(
                    message=f"Error getting task: {response.status_code} - {response.text}",
                    break_loop=False
                )
                
        except requests.exceptions.RequestException as e:
            return Response(message=f"Network error getting task: {str(e)}", break_loop=False)

    async def _update_task(self) -> Response:
        """Update task details."""
        task_id = self.args.get("task_id")
        if not task_id:
            return Response(message="Error: 'task_id' parameter is required", break_loop=False)
        
        # Get the fields that can be updated
        title = self.args.get("title")
        description = self.args.get("description")
        status = self.args.get("status")
        priority = self.args.get("priority")
        user_email = self.args.get("user_email")
        position = self.args.get("position")
        due_date = self.args.get("due_date")
        
        if not any([title, description is not None, status, priority, user_email is not None, position is not None, due_date]):
            return Response(
                message="Error: At least one field must be provided for update (title, description, status, priority, user_email, position, due_date)",
                break_loop=False
            )
        
        # Validate status and priority if provided
        if status:
            valid_statuses = ["TODO", "IN_PROGRESS", "DONE"]
            if status not in valid_statuses:
                return Response(
                    message=f"Error: Invalid status '{status}'. Valid statuses: {', '.join(valid_statuses)}",
                    break_loop=False
                )
        
        if priority:
            valid_priorities = ["LOW", "MEDIUM", "HIGH", "URGENT"]
            if priority not in valid_priorities:
                return Response(
                    message=f"Error: Invalid priority '{priority}'. Valid priorities: {', '.join(valid_priorities)}",
                    break_loop=False
                )
        
        api_url = self._get_api_url()
        
        # Build update data
        update_data = {}
        if title:
            update_data["title"] = title
        if description is not None:
            update_data["description"] = description
        if status:
            update_data["status"] = status
        if priority:
            update_data["priority"] = priority
        if user_email is not None:
            update_data["userEmail"] = user_email
        if position is not None:
            update_data["position"] = int(position)
        if due_date:
            update_data["dueDate"] = due_date
        
        try:
            response = requests.put(
                f"{api_url}/task/{task_id}/update",
                json=update_data,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                task = response.json()
                return Response(
                    message=f"Successfully updated task '{task.get('title', task_id)}' (ID: {task_id})",
                    break_loop=False
                )
            else:
                return Response(
                    message=f"Error updating task: {response.status_code} - {response.text}",
                    break_loop=False
                )
                
        except requests.exceptions.RequestException as e:
            return Response(message=f"Network error updating task: {str(e)}", break_loop=False)

    async def _update_task_status(self) -> Response:
        """Update task status."""
        task_id = self.args.get("task_id")
        status = self.args.get("status")
        
        if not task_id or not status:
            return Response(
                message="Error: Both 'task_id' and 'status' parameters are required",
                break_loop=False
            )
        
        # Update using the general update method
        self.args["action"] = "update"
        return await self._update_task()

    async def _update_task_assignee(self) -> Response:
        """Update task assignee."""
        task_id = self.args.get("task_id")
        user_email = self.args.get("user_email")
        
        if not task_id:
            return Response(message="Error: 'task_id' parameter is required", break_loop=False)
        
        # user_email can be None to unassign
        self.args["action"] = "update"
        return await self._update_task()

    async def _update_task_priority(self) -> Response:
        """Update task priority."""
        task_id = self.args.get("task_id")
        priority = self.args.get("priority")
        
        if not task_id or not priority:
            return Response(
                message="Error: Both 'task_id' and 'priority' parameters are required",
                break_loop=False
            )
        
        # Update using the general update method
        self.args["action"] = "update"
        return await self._update_task()

    async def _delete_task(self) -> Response:
        """Delete a task."""
        task_id = self.args.get("task_id")
        if not task_id:
            return Response(message="Error: 'task_id' parameter is required", break_loop=False)
        
        api_url = self._get_api_url()
        
        try:
            # For tasks, we might need to update status to DELETED rather than actual deletion
            response = requests.put(
                f"{api_url}/task/{task_id}/update",
                json={
                    "status": "DELETED",
                    "title": "Deleted Task",
                    "description": "",
                    "position": 0,
                    "priority": "LOW",
                    "userEmail": ""
                },
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                return Response(
                    message=f"Successfully deleted task (ID: {task_id})",
                    break_loop=False
                )
            else:
                return Response(
                    message=f"Error deleting task: {response.status_code} - {response.text}",
                    break_loop=False
                )
                
        except requests.exceptions.RequestException as e:
            return Response(message=f"Network error deleting task: {str(e)}", break_loop=False)

    async def _get_task_attachments(self) -> Response:
        """Get attachments for a task."""
        task_id = self.args.get("task_id")
        if not task_id:
            return Response(message="Error: 'task_id' parameter is required", break_loop=False)
        
        api_url = self._get_api_url()
        
        try:
            response = requests.get(
                f"{api_url}/tasks/{task_id}/attachments",
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                attachments = response.json()
                if not attachments:
                    return Response(message="No attachments found for this task", break_loop=False)
                
                attachment_list = []
                for attachment in attachments:
                    attachment_type = attachment.get('type', 'unknown')
                    size_info = f" ({attachment.get('size', 'unknown')} bytes)" if attachment.get('size') else ""
                    
                    attachment_list.append(
                        f"- {attachment['name']} (Type: {attachment_type}{size_info}) - Created: {attachment.get('createdAt', 'Unknown')}"
                    )
                
                return Response(
                    message=f"Task attachments ({len(attachments)}):\n" + "\n".join(attachment_list),
                    break_loop=False
                )
            else:
                return Response(
                    message=f"Error getting task attachments: {response.status_code} - {response.text}",
                    break_loop=False
                )
                
        except requests.exceptions.RequestException as e:
            return Response(message=f"Network error getting task attachments: {str(e)}", break_loop=False)

    def _get_api_url(self) -> str:
        """Get the API URL from environment or use default."""
        return self.args.get("api_url", "http://localhost:3000")

    async def before_execution(self, **kwargs):
        self.log = self.agent.context.log.log(
            type="tool", 
            heading=f"{self.agent.agent_name}: Using Doogarey Task Tool", 
            content="", 
            kvps=self.args
        )

    async def after_execution(self, response: Response, **kwargs):
        self.agent.hist_add_tool_result(self.name, response.message)
        self.log.update(content=response.message)
