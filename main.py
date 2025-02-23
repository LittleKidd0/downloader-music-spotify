import json
import os
import time
import webbrowser
from colorama import Fore
import platform

system_ = platform.system()

os.system("cls" if os.name == "nt" else "clear")

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

print(logo, """
                                    [1] downloader music spotify. web spotisongdownloader.to
                                    [2] creator page
                                    [3] Exit.
""")

def windows(dlink):
    webbrowser.open(dlink)
    print()
    input1 = input("Do you want to download a track again? (s/n): ")
    if input1.lower() == "s":
        os.system("rm data.json & rm final.json & rm datos2.json")
        track()
    elif input1.lower() == "n":
        os.system("rm data.json & rm final.json & rm datos2.json")
        main()
    else:
        print("Invalid input. Returning to the main menu.")
        main()

def album():
    os.system("cls" if os.name == "nt" else "clear")
    print(logo)
    
    url_album = input("URL album: ")

    if url_album.strip() and url_album.startswith("https://open.spotify.com"):
        os.system(f"node ./modulos/album.js {url_album}")
        time.sleep(1)
        os.system("node ./modulos/album2.js")
        time.sleep(1)
        os.system("node ./modulos/ordenamiento.js")

        os.makedirs('result', exist_ok=True)

        with open('links.json', 'r', encoding='utf8') as f:
            download_links = json.load(f)

        for link in download_links:
            os.system(f"wget '{link}' -P result/")
        os.system("rm links.json & rm datos2.json & rm final.json")
        os.system("node ./modulos/ren.js")
        time.sleep(1)
        again = input("¿Do you want to download another album? (s/n): ")
        
        if again.lower() == 's':
            os.system("rm links.json & rm datos2.json & rm final.json")
            album()
        else:
            main()
    else:
        print("Invalid URL. Please enter a valid Spotify URL.")

def track():
    os.system("cls" if os.name == "nt" else "clear")
    print(logo)
    url_track = input("URL track: ")

    if url_track.strip() and url_track.startswith("https://open.spotify.com"):
        os.system(f"node ./modulos/pruebas.js {url_track}")
        os.system(f"node ./modulos/casi.js")

        with open('final.json', 'r') as file:
            json_data = json.load(file)
            dlink = json_data.get('dlink')
        with open("data.json", "r") as file2:
            json_data2 = json.load(file2)
            name = json_data2.get("song_name")
            if system_ == "Windows":
                windows(dlink)
            elif system_ == "Linux":
                if name and dlink:
                    os.system(f"wget '{dlink}' -P result/")
                    os.system("node ./modulos/ren.js")
                else:
                    print("Song name or download link not found.")
            input1 = input("Do you want to download a track again? (s/n): ")
            if input1.lower() == "s":
                os.system("rm data.json & rm final.json & rm datos2.json")
                track()
            elif input1.lower() == "n":
                os.system("rm data.json & rm final.json & rm datos2.json")
                main()
            else:
                print("Invalid input. Returning to the main menu.")
                main()
    else:
        print("URL is not recognized.")
        time.sleep(2)
        track()

def peticiones():
    os.system("cls" if os.name == "nt" else "clear")
    print(logo, """
                                    [1] download only track
                                    [2] download only album
                                    [3] return
""")
    try:
        input2 = int(input(">> "))
        if input2 == 1:
            track()
        elif input2 == 2:
            album()
        elif input2 == 3:
            main()
        else:
            print("invalid option...")
            time.sleep(2)
            peticiones()
    except ValueError:
        print("Please enter a valid number.")
        time.sleep(2)
        peticiones()

def main():
    os.system("cls" if os.name == "nt" else "clear")
    print(logo, """
                                    [1] downloader music spotify. web spotisongdownloader.to
                                    [2] creator page
                                    [3] Exit.
""")
    try:
        opciones = int(input(">> "))
        if opciones == 1:
            peticiones()
        elif opciones == 2:
            webbrowser.open("https://github.com/LittleKidd0")
        elif opciones == 3:
            os.system("cls" if os.name == "nt" else "clear")
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

main()
