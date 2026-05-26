import os
import sys
import time
import random
import traceback
from google import genai


def titles(local_paths):
    api_key = "Your API Key"
    client = genai.Client(api_key=api_key)
    
    data = []
    prompt = "Extract the titles from the articles in the image."

    for index, path in enumerate(local_paths, start=1):
        print(f"\n--- Processing file {index}/{len(local_paths)}: {path} ---")
        
        try:
            # Upload the file
            myfile = client.files.upload(file=path)
            
            # Generate content using the uploaded file reference
            result = client.models.generate_content(
                model="gemini-2.5-flash",  # Updated to a standard current model name
                contents=[myfile, "\n\n", prompt],
            )
            
            print(f"Response: {result.text}")
            data.append(result.text)

        except Exception as e:
            print("When 'client.models.generate_content' was instantiated, it resulted in the following error:")
            # Extracts line number and file name elegantly
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)
            print(f"Error Details: {exc_type.__name__} in {fname} at line {exc_tb.tb_lineno}")
            continue

        finally:
            # Safely cleanup ONLY the file uploaded in this iteration
            try:
                if 'myfile' in locals():
                    client.files.delete(name=myfile.name)
                    print(f"Cleaned up remote file: {myfile.name}")
            except Exception as cleanup_error:
                print(f"Failed to delete remote file: {cleanup_error}")

        # Handle pacing between multiple files
        if len(local_paths) > 1 and index < len(local_paths):
            total_pause_time = random.randint(5, 60)
            print(f"Completed interval number {index}. Sleeping for {total_pause_time}s...")
            time.sleep(total_pause_time)

    return data


if __name__ == "__main__":
    paths = ["image.pdf", "image.png"]
    titles(paths)
    sys.exit()
