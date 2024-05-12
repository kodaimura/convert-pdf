import os
import fitz
from datetime import datetime
from zoneinfo import ZoneInfo

def separate_extension(file_name):
    base_name = os.path.splitext(file_name)[0]
    extension = os.path.splitext(file_name)[1]
    
    return base_name, extension


def is_skip_file(file_name):
    return file_name in [".gitignore", ".DS_Store"]

formatted_time = datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y-%m-%d-%H:%M:%S")

for root, dirs, files in  os.walk("input"):
    os.makedirs(f"output/{formatted_time}/{root[6:]}", exist_ok=True)
    for file_name in files:
        if (is_skip_file(file_name)): continue

        file_path = os.path.join(root, file_name)
        base_name, extension = separate_extension(file_name)
        doc = fitz.open(file_path)
        out = open(f"output/{formatted_time}/{root[6:]}/{base_name}.txt", "wb")
        for page in doc:
            text = page.get_text().encode("utf8")
            out.write(text)
            out.write(bytes((12,)))
out.close()

