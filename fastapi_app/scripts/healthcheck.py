import httpx
import sys

def healthcheck(url="http://localhost:8000/healthcheck"):
    """
    Checks the health of the application by sending a GET request to the specified URL.
    
    Args:
        url (str): The URL to check the health of the application.
        
    Returns:
        int: 0 if the application is healthy; 1 if the application is unhealthy or an error occurred.
    """
    try:
        # Sending a GET request to the provided URL
        response = httpx.get(url)
        
        # Checking if the response status is 200 (OK)
        if response.status_code == 200:
            print("Healthy")  # Indicates that the application is running properly
            return 0
        else:
            # In case of a different status code, indicate that the application is unhealthy
            print(f"Unhealthy - status code: {response.status_code}")
            return 1
    except Exception as e:
        # Handle exceptions, informing about the error during the request execution
        print(f"Healthcheck failed: {str(e)}")
        return 1
    
if __name__ == "__main__":
    # Runs the healthcheck function and exits with the appropriate code
    exit(healthcheck())
