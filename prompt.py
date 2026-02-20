import os
import random
import sys
import google.generativeai as genai
import time
import hashlib


def generate():
    # Fill this with as many prompts as you need
    test_prompts = ["Write a poem.", "Write a haiku."]
    # If you want the script to run for an entire day free of charge, be sure to implement a sleep-schedule so that you aren't taxing Gemini's servers and, in addition, so that you honor Gemini's 1500 (free) request daily limit
    rest_range = [random.randint(58, 120) for _ in range(1501)]

    rest_range_index = 0

    dirname = os.path.dirname(__file__)

    # You'll be needing an API Key as well
    api_key = "Your Gemini API Key"
    genai.configure(api_key=api_key)

    # Replace this with your model of choice
    model_name = "gemini-2.0-flash"
    model = genai.GenerativeModel(str(model_name))

    sha256 = hashlib.sha256()
    current_time = str(time.time())
    file_hash = current_time.encode('utf-8')

    sha256.update(file_hash)

    response_local_path_hash = sha256.hexdigest()

    prompt_counter = 0

    for prompt in test_prompts:
        response = model.generate_content(prompt)
        time_api_was_called = str(time.time())

        rest_range_index += 1

        response_local_path = os.path.join(dirname, "responses")

        if not os.path.exists(response_local_path):
            os.mkdir(response_local_path)

        response_local_path = os.path.join(response_local_path, "responses_" + str(response_local_path_hash))

        if not os.path.exists(response_local_path):
            os.mkdir(response_local_path)

        response_local_path = os.path.join(response_local_path, "response_" + str(response_local_path_hash) + "_" + str(time_api_was_called) + ".txt")

        with open(response_local_path, 'w', encoding="utf-8") as file:
            file.write(str(response.text))
            file.close()

        if len(test_prompts) > 1:
            total_pause_time = rest_range[rest_range_index]
            print(f"Sleep time: {total_pause_time}")
            print(f"Completed interval number {prompt_counter}")
            print(f"Response: {response.text}")
    
            time.sleep(total_pause_time)
            prompt_counter += 1


def main(argv):
    generate()


if __name__ == "__main__":
    main(sys.argv)
    sys.exit()



