# Doogarey Tools Integration for Agent Zero

## Overview
This document describes the integration of Doogarey productivity tools into Agent Zero, creating a custom AI assistant for the Doogarey platform. The integration allows users to manage workspaces, projects, tasks, and files through natural language conversation.

## Integration Architecture

### Components Added
1. **Python Tool Implementations** (in `/python/tools/`)
   - `doog_workspace.py` - Workspace management
   - `doog_project.py` - Project management  
   - `doog_task.py` - Task management
   - `doog_file.py` - File and attachment management

2. **Prompt Files** (in `/prompts/doog_prompts/`)
   - `agent.system.tool.doog_workspace.md` - Workspace tool documentation
   - `agent.system.tool.doog_project.md` - Project tool documentation
   - `agent.system.tool.doog_task.md` - Task tool documentation
   - `agent.system.tool.doog_file.md` - File tool documentation
   - Modified core prompt files for Doogarey context

3. **Updated Tool Registry**
   - Modified `agent.system.tools.md` to include doog tools

## File Structure
```
agent-zero/
├── python/tools/
│   ├── doog_workspace.py     # NEW: Workspace management tool
│   ├── doog_project.py       # NEW: Project management tool
│   ├── doog_task.py          # NEW: Task management tool
│   ├── doog_file.py          # NEW: File management tool
│   └── [existing tools...]
├── prompts/doog_prompts/     # MODIFIED: Custom prompt set for Doogarey
│   ├── agent.system.tool.doog_workspace.md  # NEW
│   ├── agent.system.tool.doog_project.md    # NEW
│   ├── agent.system.tool.doog_task.md       # NEW
│   ├── agent.system.tool.doog_file.md       # NEW
│   ├── agent.system.tools.md                # MODIFIED: Added doog tools
│   ├── agent.system.main.role.md            # MODIFIED: Doogarey role
│   ├── agent.system.main.communication.md   # MODIFIED: Project-focused communication
│   ├── agent.system.main.solving.md         # MODIFIED: Project-focused problem solving
│   ├── agent.system.main.tips.md            # MODIFIED: Doogarey best practices
│   ├── agent.system.main.environment.md     # MODIFIED: Integration context
│   └── [other existing prompts...]
```

## Tool Capabilities

### Workspace Tool (`doog_workspace`)
- Create new workspaces for project organization
- List user's workspaces
- Get workspace details
- Update workspace information
- Delete workspaces
- Manage workspace members (invite/remove)

### Project Tool (`doog_project`)
- Create projects within workspaces
- List projects in a workspace
- Get project details
- Update project information
- Delete projects

### Task Tool (`doog_task`)
- Create tasks within projects
- List tasks in a project
- Get task details
- Update task information
- Change task status (TODO → IN_PROGRESS → DONE)
- Assign/unassign tasks
- Set task priority levels
- Delete tasks
- Manage task attachments

### File Tool (`doog_file`)
- List user files
- Attach files to tasks
- Add URL attachments to tasks
- Remove task attachments
- Get task attachment lists

## API Integration
The tools connect to the Doogarey API through HTTP requests. The API URL is configurable through the `api_url` parameter in tool arguments, defaulting to `http://localhost:3000`.

### Multi-Tenant Support
The integration is designed to work with Doogarey's multi-tenant architecture through the bridge service, allowing different organizations to use their own isolated Agent Zero instances.

## Updating Agent Zero with Doog Tools

### When Agent Zero Updates Are Released

1. **Backup Current Integration**
   ```bash
   # Create backup of custom tools and prompts
   cp -r python/tools/doog* /backup/tools/
   cp -r prompts/doog_prompts /backup/prompts/
   ```

2. **Update Agent Zero Core**
   ```bash
   # Pull latest Agent Zero changes
   git fetch origin
   git merge origin/main  # or appropriate branch
   ```

3. **Restore Doog Tools**
   ```bash
   # Restore tool implementations
   cp /backup/tools/doog* python/tools/
   
   # Restore custom prompts
   cp -r /backup/prompts/doog_prompts prompts/
   ```

4. **Check for Conflicts**
   - Review any changes to base tool classes in `python/helpers/tool.py`
   - Update doog tools if base class interface changes
   - Check for changes in prompt structure or includes

5. **Test Integration**
   - Verify all doog tools load correctly
   - Test basic workspace/project/task operations
   - Confirm API connectivity and authentication

### Maintaining Compatibility

#### Tool Class Updates
If the base `Tool` class in `python/helpers/tool.py` changes:
1. Review the changes in the base class
2. Update doog tool implementations to match new interface
3. Test tool execution and response handling

#### Prompt System Changes
If the prompt system structure changes:
1. Review changes to `agent.system.tools.md` structure
2. Update doog tool inclusions if needed
3. Adapt prompt files to new format requirements

#### New Agent Zero Features
When new features are added to Agent Zero:
1. Evaluate if they benefit Doogarey use cases
2. Consider integrating new capabilities with doog tools
3. Update prompts to leverage new features for productivity

## Configuration

### Environment Setup
The tools require the Doogarey API to be accessible. Configure the API URL through:
1. Tool arguments: `"api_url": "https://your-doogarey-instance.com"`
2. Environment variables (can be added to future versions)
3. Configuration files (can be implemented as needed)

### Prompt Selection
To use Doogarey-customized prompts:
1. In Agent Zero settings, select `doog_prompts` as the prompt directory
2. This will use the Doogarey-focused role, communication, and tool set
3. Fall back to default prompts for any missing files

## Development Guidelines

### Adding New Doog Tools
1. Create tool implementation in `python/tools/doog_[toolname].py`
2. Follow existing pattern: inherit from `Tool`, implement `execute()` method
3. Add corresponding prompt file in `prompts/doog_prompts/agent.system.tool.doog_[toolname].md`
4. Update `prompts/doog_prompts/agent.system.tools.md` to include new tool

### Tool Implementation Standards
- Use consistent error handling and response format
- Include comprehensive action validation
- Provide helpful error messages for users
- Support configurable API URL
- Follow existing logging and history patterns

### Testing New Integrations
1. Test basic tool functionality in isolation
2. Test integration with Agent Zero framework
3. Verify prompt formatting and tool discovery
4. Test complete workflows (workspace → project → tasks)
5. Validate multi-tenant scenarios if applicable

## Troubleshooting

### Common Issues
1. **Tool not found**: Check tool file is in `python/tools/` and properly named
2. **Prompt not loading**: Verify prompt file exists and is included in `tools.md`
3. **API connection issues**: Check API URL configuration and network connectivity
4. **Permission errors**: Verify API authentication and user permissions

### Debug Steps
1. Check Agent Zero logs for tool loading errors
2. Verify API responses using direct HTTP requests
3. Test tool execution with minimal parameters
4. Review prompt formatting and JSON structure

## Future Enhancements

### Potential Improvements
1. **Enhanced Authentication**: Integrate with Doogarey's auth system
2. **Real-time Updates**: WebSocket integration for live project updates
3. **Advanced Workflows**: Multi-step project templates and automation
4. **Team Collaboration**: Enhanced multi-user coordination features
5. **Analytics Integration**: Project progress tracking and reporting

### Scalability Considerations
1. **Caching**: Implement response caching for frequently accessed data
2. **Batch Operations**: Support bulk operations for large projects
3. **Rate Limiting**: Handle API rate limits gracefully
4. **Error Recovery**: Robust retry and recovery mechanisms

This integration transforms Agent Zero into a powerful Doogarey productivity assistant while maintaining compatibility with the core Agent Zero framework and facilitating easy updates as both systems evolve.