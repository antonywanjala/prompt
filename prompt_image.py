import os
import sys
import time
import random
from google import genai


def titles(local_paths):
    api_key = "Your API Key"
    client = genai.Client(api_key=api_key)

    data = []

    path_counter = 0

    for path in local_paths:
        myfile = client.files.upload(file=path)
        file_name = myfile.name
        myfile = client.files.get(name=file_name)
        task_three = "Extract the titles from the articles in the image."
        prompt = task_three
        result = None
        result_text = None
        try:
            result = client.models.generate_content(
                model="Google Gemini Model Name",
                contents=[
                    myfile,
                    "\n\n",
                    prompt,
                ],
            )
            result_text = result.text
            data.append(result_text)
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("When \'client.models.generate_content\' was instantiated, it resulted in the following error:")
            readout_one = str(exc_type)
            readout_two = str(fname)
            readout_three = str(exc_tb.tb_lineno)
            response_text_error_readout = readout_one + " " + readout_two + " " + readout_three
            print(f"{response_text_error_readout=}")
            # When the script encounters an error it goes ahead and continues to the next path in the list of user-provided-local-paths as the next line suggests
            continue

        # It goes ahead and deletes all the previously-uploaded files attached to the user's profile
        for f in client.files.list():
            client.files.delete(name=f.name)
            print("  ", f.name + " has been deleted.")

        if len(local_paths) > 1:
            total_pause_time = random.randint(5, 60)
            print(f"Sleep time: {total_pause_time}")
            print(f"Completed interval number {path_counter}")
            if result is not None:
                print(f"Response: {result_text}")
            elif result is None:
                print(f"No viable response.")
            time.sleep(total_pause_time)
            path_counter += 1

    return data


# As you can see, Gemini can extract information from PDFs and PNGs (among other file types) as of the time of this writing
paths = ["image.pdf", "image.png"]
titles(paths)
sys.exit()
