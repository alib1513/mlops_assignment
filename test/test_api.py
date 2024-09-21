import requests, os
import time

HOST = os.getenv('FLASK_RUN_HOST', '0.0.0.0')  # Default to 0.0.0.0
PORT = os.getenv('FLASK_RUN_PORT', 5000)     # Default to port 5000
LOOP = int(os.getenv('LOOP', 1)) # Default to 1 which means no loop  
# Define the base URL of the API
BASE_URL = f'http://{HOST}:{PORT}'

IMAGE_FOLDER = "images"


# Function to send a task by uploading a file
def start_task(file_path):
    url = f"{BASE_URL}/start_task"
    files = {'file': open(file_path, 'rb')}
    
    try:
        response = requests.post(url, files=files)
        response.raise_for_status()  # Raise an error for bad responses
        task_id = response.json().get('task_id')  # Assuming the task ID is in the response
        print(f"Task started successfully. Task ID: {task_id}")
        return task_id
    except requests.exceptions.RequestException as e:
        print(f"Failed to start task: {e}")
        return None

# Function to check the task status and results
def get_task_result(task_id):
    url = f"{BASE_URL}/task_result/{task_id}"
    
    while True:
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            response = response.json()
            status = response.get('status')
            
            if status == 'SUCCESS':
                print(f"Task {task_id} completed. Here is the response:\n{response}")
                return
            elif status == 'FAILURE':
                print(f"Task {task_id} failed due to error: {response['error']}.")
                return
            else:
                print(f"Task {task_id} still in progress...")
                
            # Wait a bit before checking again
            time.sleep(2)
        except requests.exceptions.RequestException as e:
            print(f"Failed to retrieve task result: {e}")
            return

# Function to process all images in a folder
def process_images(image_folder, loop):
    # List all files in the image folder
    image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.lower().endswith(('png', 'jpg', 'jpeg'))]
    
    if not image_files:
        print("No images found in the folder.")
        return
    

    image_files *= loop

    print(f"Found {len(image_files)} image(s) to process.")
    
    task_ids = []
    # Loop through each image and process it
    for image_file in image_files:
        
        # Start a task by sending the image
        task_id = start_task(image_file)

        # If a task was successfully created, add it to the list
        if task_id:
            task_ids.append(task_id)
        
    # After sending all the requests, retrieve the results
    for task_id in task_ids:    
        get_task_result(task_id)



if __name__ == "__main__":
    # process images contained in IMAGE_FOLDER and LOOP over the images to 
    process_images(IMAGE_FOLDER, LOOP)

