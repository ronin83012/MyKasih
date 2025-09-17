import os
import time
import threading
import ctypes

# For playing beep sound on Windows
try:
    import winsound
    def beep():
        winsound.Beep(1000, 200)
except ImportError:
    def beep():
        print('\a', end='', flush=True)

disarmed = False

def get_desktop_path():
    buf = ctypes.create_unicode_buffer(260)
    ctypes.windll.shell32.SHGetFolderPathW(None, 0x10, None, 0, buf)
    return buf.value

desktop_path = get_desktop_path()

def listen_for_disarm():
    global disarmed
    while not disarmed:
        user_input = input()
        if user_input.strip().lower() == "disarm":
            disarmed = True
            print("\n💥 Bomb disarmed! No more files will be created.")

def create_bombs():
    count = 0
    while not disarmed:
        for i in range(5, 0, -1):
            if disarmed:
                break
            print(f"\r⏳ Creating next bomb in: {i} seconds ", end='')
            beep()
            time.sleep(1)
        if disarmed:
            break

        filename = f"Bomb{'' if count == 0 else count}.txt"
        filepath = os.path.join(desktop_path, filename)
        try:
            with open(filepath, 'w') as file:
                file.write("This is da bomb!.\n")
                file.write("BOOM!")
            print(f"\r💣 File '{filename}' created on Desktop.               ")
        except IOError as e:
            print(f"\nError creating file '{filename}': {e}")
        count += 1

if __name__ == "__main__":
    listener_thread = threading.Thread(target=listen_for_disarm)
    listener_thread.daemon = True
    listener_thread.start()

    create_bombs()
