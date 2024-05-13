import os
import fitz
from datetime import datetime
from zoneinfo import ZoneInfo

def separate_extension(file_name) -> tuple[str, str]:
    base_name = os.path.splitext(file_name)[0]
    extension = os.path.splitext(file_name)[1]
    
    return base_name, extension

def is_skip_file(file_name) -> bool:
    return file_name in [".gitignore", ".DS_Store"]

def write_text(output_path: str, text: str) -> None:
    out = open(output_path, "wb")
    out.write(text.encode("utf8"))
    out.close()

def extract_text_from_pdf(file_path: str) -> str:
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text(sort=True) + "\n"

    return text

def convert_file(input_path: str, output_path: str) -> None:
    text = extract_text_from_pdf(input_path)
    write_text(output_path, text)


def convert_process(input_root: str, output_root: str) -> None:
    log = open(f"{output_root}/convert.log", "w")
    for root, dirs, files in os.walk(input_root):
        output_dir = f"{output_root}/{root[6:]}"
        os.makedirs(output_dir, exist_ok=True)
        for file_name in files:
            if (is_skip_file(file_name)): continue
            base_name, extension = separate_extension(file_name)
            input_path = os.path.join(root, file_name)
            output_path = f"{output_dir}/{base_name}.txt"

            if (extension != ".pdf"):
                log.write(f"SKIP: {input_path}" + "\n")
                continue

            try:
                convert_file(input_path, output_path)
            except Exception as e:
                log.write(f"FAIL: {input_path} error: {e}" + "\n")
    log.close()

def convert() -> None:
    input_root = "input"
    output_root = f"output/{datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y-%m-%d-%H:%M:%S")}"
    os.makedirs(output_root, exist_ok=True)
    convert_process(input_root, output_root)

convert()