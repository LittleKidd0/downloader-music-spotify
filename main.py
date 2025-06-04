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
    if system_ == "Windows":
        os.system("del /f /q data.json final.json datos2.json links.json datos3.json")
    else:
        os.system("rm -f data.json final.json datos2.json links.json datos3.json")

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

                                                                                    By: {Fore.YELLOW}LittleKidd0{Fore.RESET}
                                                                                    Date: 03-03-2025
"""
    print(logo)

def windows_download(dlink):
    print(dlink)
    webbrowser.open(dlink)
    time.sleep(4)
    if input("Download another track? (s/n): ").lower() == "s":
        remove_temp_files()
        track()
    else:
        remove_temp_files()
        main()

def download_links(file, delay=2):
    links = load_json(file)
    if links:
        for i, link in enumerate(links, 1):
            print(f"{i}/{len(links)}: {link}")
            webbrowser.open(link)
            time.sleep(delay)
        remove_temp_files()

def album():
    clear_console()
    display_logo()
    url_album = input("URL album (enter for come back): ")
    if url_album == "":
        peticiones()
    else:

        if url_album.startswith(("https://open.spotify.com/intl-es/album/","https://open.spotify.com/album")):
            run_node_module("album.js", url_album)
            run_node_module("album2.js")
            run_node_module("ordenamiento.js")
            os.makedirs('result', exist_ok=True)
            links = load_json('links.json')
            if system_ == "Windows":
                download_links('links.json', 3)
                if input("Download another album? (s/n): ").lower() == "s":
                    album()
                else:
                    main()
            elif system_ == "Linux" and links:
                for link in links:
                    os.system(f"wget '{link}' -P albumes/")
                run_node_module("ren.js albumes")
                remove_temp_files()
                if input("Download another album? (s/n): ").lower() == "s":
                    album()
                else:
                    remove_temp_files()
                    main()
            else:
                print("No links found.")
                remove_temp_files()
        else:
            print("Invalid URL. Please enter a valid Spotify URL.")
            time.sleep(2)
            album()
def playlist():
    print("Working!! 👷")
    time.sleep(2)
    main()
def track():
    clear_console()
    display_logo()
    url_track = input("URL track (enter for come back): ")
    if url_track == "":
        main()
    else:
        if url_track.startswith(("https://open.spotify.com/intl-es/track/", "https://open.spotify.com/track/")):
            run_node_module("pruebas.js", url_track)
            run_node_module("casi.js")
            dlink = load_json('final.json').get('dlink')
            name = load_json('data.json').get("song_name")
            if system_ == "Windows":
                windows_download(dlink)
            elif system_ == "Linux" and dlink and name:
                os.system(f"wget '{dlink}' -P result/")
                run_node_module("ren.js")
                remove_temp_files()
                if input("Download another track? (s/n): ").lower() == "s":
                    track()
                else:
                    remove_temp_files()
                    main()
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
                                [2] download only playlist- Working 👷
                                [3] download only album
                                [4] return
    """)
    try:
        option = int(input(">> "))
        if option == 1:
            track()
        elif option == 2:
            playlist()
        elif option == 3:
            album()
        elif option == 4:
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
#Hola!
