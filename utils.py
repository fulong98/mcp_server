import http.client
import json
import subprocess
import runpod
import os


API_KEY = "xxx"
API_BASE_URL = "https://rest.runpod.io/v1"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

def create_cpu_pod():
    """Create a CPU-only pod with specified parameters"""
    
    # Connect to RunPod API
    conn = http.client.HTTPSConnection("rest.runpod.io")
    
    # Pod configuration
    payload = json.dumps({
        "allowedCudaVersions": [
            "12.7"
        ],
        "cloudType": "SECURE",
        "computeType": "CPU",
        "containerDiskInGb": 10,
        "containerRegistryAuthId": "",
        "cpuFlavorIds": [
            "cpu3c"
        ],
        "cpuFlavorPriority": "availability",
        "dataCenterIds": [
            "EU-RO-1",
            "CA-MTL-1"
        ],
        "dataCenterPriority": "availability",
        "dockerEntrypoint": [],
        "dockerStartCmd": [],
        "env": {
            "ENV_VAR": "value"
        },
        "gpuCount": 1,
        "gpuTypeIds": [
            "NVIDIA GeForce RTX 4090"
        ],
        "gpuTypePriority": "availability",
        "imageName": "runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04",
        "interruptible": False,
        "locked": False,
        "minRAMPerGPU": 8,
        "minVCPUPerGPU": 2,
        "name": "my pod",
        "ports": [
            "8888/http",
            "22/tcp"
        ],
        "supportPublicIp": False,
        "vcpuCount": 2,
        "volumeInGb": 20,
        "volumeMountPath": "/workspace"
    })
    
    headers = {
        'Content-Type': "application/json",
        'Authorization': f"Bearer {API_KEY}"
    }
    
    print("Creating CPU pod with 2 vCPUs, 4GB RAM, and 5GB disk...")
    
    # Make the API request to create the pod
    conn.request("POST", "/v1/pods", payload, headers)
    res = conn.getresponse()
    data = res.read()
    
    # Check if the request was successful
    if res.status == 201:
        pod_data = json.loads(data.decode("utf-8"))
        pod_id = pod_data.get('id')
        print(f"Pod created successfully with ID: {pod_id}")
        return pod_id
    else:
        print(f"Failed to create pod. Status: {res.status}")
        print(f"Response: {data.decode('utf-8')}")
        return None

def get_pod_status(pod_id):
    """Get the current status of a pod"""
    
    conn = http.client.HTTPSConnection("rest.runpod.io")
    
    headers = {
        'Authorization': f"Bearer {API_KEY}"
    }
    
    conn.request("GET", f"/v1/pods/{pod_id}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    
    if res.status == 200:
        return json.loads(data.decode("utf-8"))
    else:
        print(f"Failed to get pod status. Status: {res.status}")
        print(f"Response: {data.decode('utf-8')}")
        return None

def terminate_pod(pod_id):
    """Terminate a pod"""
    
    conn = http.client.HTTPSConnection("rest.runpod.io")
    
    headers = {
        'Authorization': f"Bearer {API_KEY}"
    }
    
    conn.request("DELETE", f"/v1/pods/{pod_id}", headers=headers)
    res = conn.getresponse()
    
    if res.status == 200:
        print(f"Pod {pod_id} terminated successfully")
        return True
    else:
        data = res.read()
        print(f"Failed to terminate pod. Status: {res.status}")
        print(f"Response: {data.decode('utf-8')}")
        return False


def _create_pod_with_custom_image( entrypoint_cmd: list) -> str:
    """
    Create a RunPod CPU pod using  the specified entrypoint command.
    Returns the pod ID if successful, otherwise None.
    """
    conn = http.client.HTTPSConnection("rest.runpod.io")
    
    # Prepare the payload: CPU, minimal resources, container set to your custom image
    payload = json.dumps({
        "allowedCudaVersions": [
            "12.7"
        ],
        "dockerEntrypoint": entrypoint_cmd,  # The command that will run in the container
        "cloudType": "SECURE",
        "computeType": "CPU",
        "containerDiskInGb": 10,
        "containerRegistryAuthId": "",
        "cpuFlavorIds": [
            "cpu3c"
        ],
        "cpuFlavorPriority": "availability",
        "dataCenterIds": [
            "EU-RO-1",
            "CA-MTL-1"
        ],
        "dataCenterPriority": "availability",
        "dockerStartCmd": [],
        "env": {
            "ENV_VAR": "value"
        },
        "gpuCount": 1,
        "gpuTypeIds": [
            "NVIDIA GeForce RTX 4090"
        ],
        "gpuTypePriority": "availability",
        "imageName": "runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04",
        "interruptible": False,
        "locked": False,
        "minRAMPerGPU": 8,
        "minVCPUPerGPU": 2,
        "name": "my pod",
        "ports": [
            "8888/http",
            "22/tcp"
        ],
        "supportPublicIp": False,
        "vcpuCount": 2,
        "volumeInGb": 20,
        "volumeMountPath": "/workspace"
    })
    
    conn.request("POST", "/v1/pods", payload, headers)
    res = conn.getresponse()
    data = res.read()
    
    if res.status == 201:
        pod_data = json.loads(data.decode("utf-8"))
        pod_id = pod_data.get('id')
        print(f"Pod created with ID: {pod_id}")
        return pod_id
    else:
        print(f"Failed to create pod. Status: {res.status}")
        print("Response:", data.decode("utf-8"))
        return None




runpod.api_key = API_KEY

# Fetching all available endpoints
endpoints = runpod.get_endpoints()

# Displaying the list of endpoints
print(endpoints)