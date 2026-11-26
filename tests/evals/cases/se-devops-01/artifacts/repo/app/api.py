import os
PORT = int(os.environ.get("API_PORT", "8080"))
if __name__ == "__main__":
    print(f"API ready on port {PORT}")
