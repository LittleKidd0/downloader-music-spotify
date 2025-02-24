import os

def rename_mp3_to_m4a(directory):
    for file in os.listdir(directory):
        if file.endswith(".mp3"):
            old_path = os.path.join(directory, file)
            new_name = os.path.splitext(file)[0] + ".m4a"
            new_path = os.path.join(directory, new_name)
            os.rename(old_path, new_path)
            print(f"{file} -> {new_name}")

if __name__ == "__main__":
    directory = input("Enter the directory path: ")
    if os.path.isdir(directory):
        rename_mp3_to_m4a(directory)
    else:
        print("Invalid path.")
