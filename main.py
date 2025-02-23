import json
import os
import time
import webbrowser
from colorama import Fore
import platform

system_ = platform.system()

def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

def remove_temp_files():
    os.system("rm -f data.json final.json datos2.json links.json")

def load_json(file_name):
    try:
        with open(file_name, 'r', encoding='utf8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Failed to load {file_name}.")
        return None

def run_node_module(script, *args):
    os.system(f"node ./modulos/{script} {' '.join(args)}")

def display_logo():
    logo = f"""{Fore.GREEN}
██████╗  ██████╗ ██╗    ██╗███╗   ██╗██╗      ██████╗  █████╗ ██████╗ ███████╗██████╗     ███╗   ███╗██╗   ██╗███████╗██╗ ██████╗    ███████╗██████╗  ██████╗ ████████╗██╗███████╗██╗   ██╗
██╔══██╗██╔═══██╗██║    ██║████╗  ██║██║     ██╔═══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗    ████╗ ████║██║   ██║██╔════╝██║██╔════╝    ██╔════╝██╔══██╗██╔═══██╗╚══██╔══╝██║██╔════╝╚██╗ ██╔╝
██║  ██║██║   ██║██║ █╗ ██║██╔██╗ ██║██║     ██║   ██║███████║██║  ██║█████╗  ██████╔╝    ██╔████╔██║██║   ██║███████╗██║██║         ███████╗██████╔╝██║   ██║   ██║   ██║█████╗   ╚████╔╝ 
██║  ██║██║   ██║██║███╗██║██║╚██╗██║██║     ██║   ██║██╔══██║██║  ██║██╔══╝  ██╔══██╗    ██║╚██╔╝██║██║   ██║╚════██║██║██║         ╚════██║██╔═══╝ ██║   ██║   ██║   ██║██╔══╝    ╚██╔╝  
██████╔╝╚██████╔╝╚███╔███╔╝██║ ╚████║███████╗╚██████╔╝██║  ██║██████╔╝███████╗██║  ██║    ██║ ╚═╝ ██║╚██████╔╝███████║██║╚██████╗    ███████║██║     ╚██████╔╝   ██║   ██║██║        ██║   
╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝    ╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚═╝ ╚═════╝    ╚══════╝╚═╝      ╚═════╝    ╚═╝   ╚═╝╚═╝        ╚═╝{Fore.RESET}

                                                                                    By: {Fore.YELLOW}vixho69{Fore.RESET}
                                                                                 update: 20-02-2025
"""
    print(logo)

def windows_download(dlink):
    webbrowser.open(dlink)
    if input("Download another track? (s/n): ").lower() == "s":
        remove_temp_files()
        track()
    else:
        remove_temp_files()
        main()

def album():
    clear_console()
    display_logo()
    url_album = input("URL album: ")
    if url_album.startswith("https://open.spotify.com"):
        run_node_module("album.js", url_album)
        run_node_module("album2.js")
        run_node_module("ordenamiento.js")
        os.makedirs('result', exist_ok=True)
        links = load_json('links.json')
        if system_ == "Windows":
            windows_download(dlink)
        elif system_ == "Linux" and dlink and name:
            os.system(f"wget '{dlink}' -P result/")
            run_node_module("ren.js")
        else:
            if links:
                for link in links:
                    os.system(f"wget '{link}' -P result/")
            remove_temp_files()
            run_node_module("ren.js")
            if input("Download another album? (s/n): ").lower() == "s":
                album()
            else:
                main()
    else:
        print("Invalid URL. Please enter a valid Spotify URL.")
        time.sleep(2)
        album()
def track():
    clear_console()
    display_logo()
    url_track = input("URL track: ")
    if url_track.startswith("https://open.spotify.com"):
        run_node_module("pruebas.js", url_track)
        run_node_module("casi.js")
        dlink = load_json('final.json').get('dlink')
        name = load_json('data.json').get("song_name")
        if system_ == "Windows":
            windows_download(dlink)
        elif system_ == "Linux" and dlink and name:
            os.system(f"wget '{dlink}' -P result/")
            run_node_module("ren.js")
        else:
            print("Song name or download link not found.")
        remove_temp_files()
        track()
    else:
        print("URL not recognized.")
        time.sleep(2)
        track()

def peticiones():
    clear_console()
    display_logo()
    print("""
                                [1] download only track
                                [2] download only album
                                [3] return
    """)
    try:
        option = int(input(">> "))
        if option == 1:
            track()
        elif option == 2:
            album()
        elif option == 3:
            main()
        else:
            print("Invalid option...")
            time.sleep(2)
            peticiones()
    except ValueError:
        print("Please enter a valid number.")
        time.sleep(2)
        peticiones()

def main():
    clear_console()
    display_logo()
    print("""
                                [1] downloader music spotify. web spotisongdownloader.to
                                [2] creator page
                                [3] Exit.
    """)
    try:
        option = int(input(">> "))
        if option == 1:
            peticiones()
        elif option == 2:
            webbrowser.open("https://github.com/LittleKidd0")
        elif option == 3:
            clear_console()
            print("Bye!")
            os._exit(0)
        else:
            print("Invalid option.")
            time.sleep(2)
            main()
    except ValueError:
        print("Please enter a valid number.")
        time.sleep(2)
        main()

if __name__ == "__main__":
    main()
