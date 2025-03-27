import runpod
from pydantic import BaseModel
import subprocess



class CodeInput(BaseModel):
    code: str

def handler(event):
    """ RunPod handler function """
    input_data = event.get("input", {})
    code = input_data.get("code", "")
    
    try:
        result = subprocess.run(
            ["python3", "-c", code], 
            capture_output=True, 
            text=True, 
            timeout=5
        )
        
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {"error": "Execution timed out"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})