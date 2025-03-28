import requests
import time
import base64

# API Key (Do not share publicly)
API_KEY = "eHVoYWlyYWhtZWQ5OTBAZ21haWwuY29t:LflFsmt7dMBsHPQw0z_PB"

# Encode API Key for authentication
BASE64_AUTH = base64.b64encode(API_KEY.encode()).decode()

# API Headers
headers = {
    "Authorization": f"Basic {BASE64_AUTH}",
    "Content-Type": "application/json"
}

# Check API Credit Balance
response = requests.get("https://api.d-id.com/credits", headers=headers)
print("API Test Response:", response.text)

# Avatar Image URL (Stored in Dropbox)
IMAGE_URL = "https://www.dropbox.com/scl/fi/t33ipleexy7j64u0m0zw9/IMG_3226.jpg?rlkey=tiqkqixzuusciannnaf0uhgxy&raw=1"

# Text-to-Speech Script
SCRIPT_TEXT = (
    "Hi everyone! I'm Zuhair Ahmed, and I'm thrilled to present my AI-driven voice and animation "
    "synchronization project. I've integrated Microsoft Azure's text-to-speech technology with "
    "D-ID's avatar animation tools, and you can find all the details in my GitHub repository. "
    "I've also included a short demo video where I give a quick overview of the project, and briefly touch on why I'm interested in joining the AIA team, contributing to your AI roadmap. "
    "I'm committed to this field for the long haul, and I'm excited to be part of a company with such ambitious plans for the future."
)

# API request payload for generating the video
data = {
    "source_url": IMAGE_URL,
    "script": {
        "type": "text",
        "input": SCRIPT_TEXT,
        "provider": {
            "type": "microsoft",
            "voice_id": "en-IN-ArjunNeural",
            "voice_config": {"style": "Cheerful"}
        }
    }
}

# Send request to D-ID API
response = requests.post("https://api.d-id.com/talks", json=data, headers=headers)

# Check API response
if response.status_code in [200, 201]:
    result = response.json()
    talk_id = result.get("id")
    if not talk_id:
        print("Error: No `talk_id` found. Full Response:", result)
        exit()
    print(f"Video request sent. Talk ID: {talk_id}")
else:
    print("API Error:", response.text)
    exit()

# Wait for video processing
print("Waiting for video processing...")
time.sleep(10)

# Check video status
video_status_url = f"https://api.d-id.com/talks/{talk_id}"
while True:
    status_response = requests.get(video_status_url, headers=headers)
    status_data = status_response.json()
    
    if status_data.get("status") == "done":
        video_url = status_data.get("result_url")
        print(f"Video is ready: {video_url}")
        break
    elif status_data.get("status") == "failed":
        print("Video generation failed.")
        exit()
    else:
        print("Processing... waiting 5 more seconds.")
        time.sleep(5)

# Download the generated video
response = requests.get(video_url, stream=True)
if response.status_code == 200:
    with open("output2.mp4", "wb") as file:
        for chunk in response.iter_content(chunk_size=1024):
            file.write(chunk)
    print("Video saved as output2.mp4")
else:
    print("Failed to download video:", response.status_code)
