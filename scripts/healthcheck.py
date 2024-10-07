import httpx

def healthcheck():
    try:
        response = httpx.get("http://localhost:8000/healthcheck")
        if response.status_code == 200:
            print("Healthy")
            return 0
        else:
            print(f"Unhealthy - status code: {response.status_code}")
            return 1
    except Exception as e:
        print(f"Healthcheck failed: {str(e)}")
        return 1
    
if __name__ == "__main__":
    exit(healthcheck())