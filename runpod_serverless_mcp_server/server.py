import asyncio
import logging
import os
import json
import requests
from typing import Dict, Any, List, Optional

from mcp.server.fastmcp import FastMCP, Context

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("runpod_mcp_server")

# Environment variables and configuration
RUNPOD_API_KEY = "xxx"
RUNPOD_ENDPOINT_ID = os.environ.get("RUNPOD_ENDPOINT_ID", "p1abozuh79miw9")  # Default endpoint ID
MAX_EXECUTION_TIME = int(os.environ.get("MAX_EXECUTION_TIME", "30"))  # Maximum execution time in seconds

# Create an MCP server with proper metadata
mcp = FastMCP(
    "RunPod Executor",
    # description="Execute Python code on RunPod infrastructure",
    # version="1.0.0",
    # dependencies=["requests>=2.25.0"]
)

@mcp.tool()
async def execute_python_code(code: str) -> str:
    """
    Execute Python code on RunPod and return the results.
    
    Args:
        code: The Python code to execute
        
    Returns:
        The output of the execution including stdout, stderr, and return code
    """
    if not RUNPOD_API_KEY:
        return "Error: RunPod API key not set. Please set the RUNPOD_API_KEY environment variable."
    
    # Log the execution request
    logger.info(f"Executing code on endpoint: {RUNPOD_ENDPOINT_ID}")
    
    # Define the API endpoint URL
    api_url = f"https://api.runpod.ai/v2/{RUNPOD_ENDPOINT_ID}/runsync"
    
    # Define the headers for the API request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {RUNPOD_API_KEY}"
    }
    
    # Define the payload with the code to execute
    payload = {
        "input": {
            "code": code
        }
    }
    
    try:
        logger.info("Sending request to RunPod API...")
        
        # Make the API request
        response = requests.post(api_url, headers=headers, json=payload, timeout=MAX_EXECUTION_TIME+5)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response JSON
            result = response.json()
            logger.info(f"Code execution completed successfully. Status: {result.get('status')}")
            
            # Extract execution details
            execution_time_ms = result.get("executionTime", 0)
            execution_time_s = execution_time_ms / 1000
            delay_time_ms = result.get("delayTime", 0)
            delay_time_s = delay_time_ms / 1000
            
            output = result.get("output", {})
            stdout = output.get("stdout", "")
            stderr = output.get("stderr", "")
            return_code = output.get("return_code", -1)
            
            # Format the response in a nice way
            result_message = f"Code execution completed in {execution_time_s:.2f} seconds (delayed {delay_time_s:.2f} seconds).\n\n"
            
            if stdout:
                result_message += "--- OUTPUT ---\n"
                result_message += f"{stdout}\n"
            
            if stderr:
                result_message += "--- ERRORS ---\n"
                result_message += f"{stderr}\n"
            
            result_message += f"--- RETURN CODE ---\n{return_code}"
            return result_message
        else:
            error_info = response.text
            logger.error(f"RunPod API error: {response.status_code} - {error_info}")
            return f"Error: Request failed with status code {response.status_code}.\n{error_info}"
    except requests.exceptions.Timeout:
        logger.error(f"RunPod API timeout after {MAX_EXECUTION_TIME} seconds")
        return f"Error: Request timed out after {MAX_EXECUTION_TIME} seconds. Your code may be taking too long to execute."
    except Exception as e:
        logger.error(f"Error during code execution: {e}")
        return f"Error: An exception occurred while executing code: {str(e)}"

@mcp.tool()
async def check_runpod_status() -> str:
    """
    Check the status of the RunPod connection and endpoint.
    
    Returns:
        A status report of the RunPod connection
    """
    if not RUNPOD_API_KEY:
        return "Error: RunPod API key not set. Please set the RUNPOD_API_KEY environment variable."
    
    # Define the API endpoint URL for a simple health check
    api_url = f"https://api.runpod.ai/v2/{RUNPOD_ENDPOINT_ID}/health"
    
    # Define the headers for the API request
    headers = {
        "Authorization": f"Bearer {RUNPOD_API_KEY}"
    }
    
    try:
        # Make the API request
        response = requests.get(api_url, headers=headers, timeout=10)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response JSON
            result = response.json()
            
            # Extract status details
            status = result.get("status", "Unknown")
            
            return f"""
RunPod Status:
- Endpoint ID: {RUNPOD_ENDPOINT_ID}
- Status: {status}
- API Connection: Successful
- Max Execution Time: {MAX_EXECUTION_TIME} seconds
"""
        else:
            error_info = response.text
            logger.error(f"Health check failed: {response.status_code} - {error_info}")
            return f"Error: Health check failed with status code {response.status_code}.\n{error_info}"
    except Exception as e:
        logger.error(f"Error checking endpoint health: {e}")
        return f"Error: An exception occurred while checking RunPod status: {str(e)}"



if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')