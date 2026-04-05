import os
import time
import hashlib
import random
import google.generativeai as genai

# --- Configuration ---
API_KEY = "Your Gemini API Key"
MODEL_NAME = "gemini-2.0-flash"
PROMPTS = ["Write a poem.", "Write a haiku."]
# To stay under the 1500 free daily limit, we need roughly 1 request every 58 seconds.
MIN_SLEEP = 58 
MAX_SLEEP = 120

def generate():
    """Generates content using Gemini and saves output to organized text files."""
    
    # Initialize API
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel(MODEL_NAME)

    # Setup Directory Structure
    base_dir = os.path.dirname(__file__)
    # Create a unique session ID based on start time
    session_id = hashlib.sha256(str(time.time()).encode()).hexdigest()[:10]
    output_folder = os.path.join(base_dir, "responses", f"session_{session_id}")
    
    os.makedirs(output_folder, exist_ok=True)

    print(f"Starting session: {session_id}")
    print(f"Saving responses to: {output_folder}\n")

    for index, prompt in enumerate(PROMPTS):
        try:
            # Call Gemini API
            response = model.generate_content(prompt)
            timestamp = int(time.time())
            
            # Save the response
            file_name = f"resp_{index}_{timestamp}.txt"
            file_path = os.path.join(output_folder, file_name)
            
            with open(file_path, 'w', encoding="utf-8") as f:
                f.write(response.text)

            print(f"[{index + 1}/{len(PROMPTS)}] Prompt: {prompt[:30]}...")
            print(f"Response saved to {file_name}")

            # Rate Limiting Logic
            if index < len(PROMPTS) - 1:
                wait_time = random.randint(MIN_SLEEP, MAX_SLEEP)
                print(f"Sleeping for {wait_time}s to respect rate limits...\n")
                time.sleep(wait_time)

        except Exception as e:
            print(f"Error processing prompt '{prompt}': {e}")

def main():
    generate()

if __name__ == "__main__":
    main()
