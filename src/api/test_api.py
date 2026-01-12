import requests
import time

def test_api():
    url = "http://127.0.0.1:8000/query"
    health_url = "http://127.0.0.1:8000/health"
    
    print("Waiting for API to be healthy...")
    for _ in range(10):
        try:
            r = requests.get(health_url)
            if r.status_code == 200:
                print("API is ready!")
                break
        except requests.exceptions.ConnectionError:
            time.sleep(2)
    else:
        print("API failed to start.")
        return

    payload = {"query": "Tell me about Stanford University."}
    print(f"\nSending payload: {payload}")
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("\nResponse:")
        print(response.json())
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_api()
