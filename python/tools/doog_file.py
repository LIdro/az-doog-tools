import json
import requests
import asyncio
from typing import Dict, Any, Optional, List
from python.helpers.tool import Tool, Response

class DoogFileTool(Tool):
    """
    Tool for managing Doogarey files and attachments.
    Handles file listing, uploading, and task attachment management.
    """

    async def execute(self, **kwargs) -> Response:
        """Execute file operations based on the action specified."""
        
        action = self.args.get("action")
        if not action:
            return Response(message="Error: 'action' parameter is required", break_loop=False)

        try:
            if action == "list":
                return await self._list_files()
            elif action == "upload":
                return await self._upload_file()
            elif action == "attach_to_task":
                return await self._attach_file_to_task()
            elif action == "add_url_to_task":
                return await self._add_url_to_task()
            elif action == "remove_task_attachment":
                return await self._remove_task_attachment()
            elif action == "get_task_attachments":
                return await self._get_task_attachments()
            else:
                return Response(
                    message=f"Error: Unknown action '{action}'. Available actions: list, upload, attach_to_task, add_url_to_task, remove_task_attachment, get_task_attachments",
                    break_loop=False
                )
                
        except Exception as e:
            return Response(message=f"Error executing file action: {str(e)}", break_loop=False)

    async def _list_files(self) -> Response:
        """List all files for the current user."""
        api_url = self._get_api_url()
        
        try:
            response = requests.get(
                f"{api_url}/files/list",
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                files = response.json()
                if not files:
                    return Response(message="No files found", break_loop=False)
                
                file_list = []
                for file in files:
                    size_info = f" ({file.get('size', 'unknown')} bytes)" if file.get('size') else ""
                    file_list.append(
                        f"- {file['name']} (ID: {file['id']}) - Type: {file.get('mimeType', 'unknown')}{size_info}"
                    )
                
                return Response(
                    message=f"Found {len(files)} file(s):\n" + "\n".join(file_list),
                    break_loop=False
                )
            else:
                return Response(
                    message=f"Error listing files: {response.status_code} - {response.text}",
                    break_loop=False
                )
                
        except requests.exceptions.RequestException as e:
            return Response(message=f"Network error listing files: {str(e)}", break_loop=False)

    async def _upload_file(self) -> Response:
        """Upload a file."""
        file_path = self.args.get("file_path")
        file_name = self.args.get("file_name")
        
        if not file_path and not file_name:
            return Response(
                message="Error: Either 'file_path' or 'file_name' parameter is required for uploading",
                break_loop=False
            )
        
        api_url = self._get_api_url()
        
        # Note: This is a simplified implementation
        # In a real scenario, you'd need to handle multipart form data
        return Response(
            message="File upload functionality requires multipart form data handling which is not implemented in this simplified version. Please use the web interface for file uploads.",
            break_loop=False
        )

    async def _attach_file_to_task(self) -> Response:
        """Attach a file to a task."""
        task_id = self.args.get("task_id")
        file_id = self.args.get("file_id")
        
        if not task_id or not file_id:
            return Response(
                message="Error: Both 'task_id' and 'file_id' parameters are required",
                break_loop=False
            )
        
        api_url = self._get_api_url()
        
        try:
            response = requests.post(
                f"{api_url}/tasks/{task_id}/attachments/file",
                json={"fileId": file_id},
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                attachment = response.json()
                return Response(
                    message=f"Successfully attached file to task {task_id}",
                    break_loop=False
                )
            else:
                return Response(
                    message=f"Error attaching file to task: {response.status_code} - {response.text}",
                    break_loop=False
                )
                
        except requests.exceptions.RequestException as e:
            return Response(message=f"Network error attaching file to task: {str(e)}", break_loop=False)

    async def _add_url_to_task(self) -> Response:
        """Add a URL attachment to a task."""
        task_id = self.args.get("task_id")
        url = self.args.get("url")
        name = self.args.get("name")
        
        if not task_id or not url:
            return Response(
                message="Error: Both 'task_id' and 'url' parameters are required",
                break_loop=False
            )
        
        if not name:
            name = url  # Use URL as name if not provided
        
        api_url = self._get_api_url()
        
        try:
            response = requests.post(
                f"{api_url}/tasks/{task_id}/attachments/url",
                json={"url": url, "name": name},
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                attachment = response.json()
                return Response(
                    message=f"Successfully added URL '{name}' to task {task_id}",
                    break_loop=False
                )
            else:
                return Response(
                    message=f"Error adding URL to task: {response.status_code} - {response.text}",
                    break_loop=False
                )
                
        except requests.exceptions.RequestException as e:
            return Response(message=f"Network error adding URL to task: {str(e)}", break_loop=False)

    async def _remove_task_attachment(self) -> Response:
        """Remove an attachment from a task."""
        task_id = self.args.get("task_id")
        attachment_id = self.args.get("attachment_id")
        
        if not task_id or not attachment_id:
            return Response(
                message="Error: Both 'task_id' and 'attachment_id' parameters are required",
                break_loop=False
            )
        
        api_url = self._get_api_url()
        
        try:
            response = requests.delete(
                f"{api_url}/tasks/{task_id}/attachments/{attachment_id}",
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                return Response(
                    message=f"Successfully removed attachment from task {task_id}",
                    break_loop=False
                )
            else:
                return Response(
                    message=f"Error removing attachment: {response.status_code} - {response.text}",
                    break_loop=False
                )
                
        except requests.exceptions.RequestException as e:
            return Response(message=f"Network error removing attachment: {str(e)}", break_loop=False)

    async def _get_task_attachments(self) -> Response:
        """Get all attachments for a task."""
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
                    
                    if attachment_type == 'url':
                        attachment_list.append(
                            f"- 🔗 {attachment['name']} (ID: {attachment['id']}) - URL: {attachment.get('url', 'N/A')}"
                        )
                    else:
                        attachment_list.append(
                            f"- 📁 {attachment['name']} (ID: {attachment['id']}) - Type: {attachment.get('mimeType', 'unknown')}{size_info}"
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
            heading=f"{self.agent.agent_name}: Using Doogarey File Tool", 
            content="", 
            kvps=self.args
        )

    async def after_execution(self, response: Response, **kwargs):
        self.agent.hist_add_tool_result(self.name, response.message)
        self.log.update(content=response.message)
