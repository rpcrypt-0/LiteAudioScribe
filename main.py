import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import pygame, os, threading, time
from dotenv import load_dotenv 
import ai_handler 

load_dotenv()
root = tk.Tk()
playlist = []
subtitles = [] 
paused = False
start_offset = 0 
is_dragging = False 
current_api_key = os.getenv("API_KEY")
if not current_api_key:
    current_api_key = simpledialog.askstring("API Key Required", "Please enter your Google Gemini API Key:")
    if not current_api_key:
        messagebox.showwarning("No Key", "Subtitle generator will be disabled until you restart and provide a key.")
pygame.mixer.init()
def get_current_time():
    if not pygame.mixer.music.get_busy() and not paused: return 0
    return start_offset + (pygame.mixer.music.get_pos() / 1000)

def time_to_sec(t_str):
    try:
        m, s, ms = map(int, t_str.replace('.', ':').split(':'))
        return m * 60 + s + (ms / 1000)
    except: return 0
def add_song():
    path = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
    if path:
        playlist.append(path)
        playlist_box.insert(tk.END, os.path.basename(path))
def play_music(start_at=0):
    global start_offset, paused
    try:
        if not playlist_box.curselection(): return
        path = playlist[playlist_box.curselection()[0]]
        
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(start=start_at)
        
        start_offset = start_at
        paused = False
        
        song_len = pygame.mixer.Sound(path).get_length()
        slider.config(to=song_len)
        update_loop()
    except Exception as e:
        print(e)

def toggle_pause():
    global paused
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True
def start_drag(event):
    global is_dragging
    is_dragging = True

def end_drag(event):
    global is_dragging
    is_dragging = False
    play_music(start_at=slider.get())
def generate_subtitles():
    
    if not current_api_key:
        messagebox.showerror("Error", "No API Key found. Please restart the app.")
        return

    def thread_task():
        try:
            if not playlist_box.curselection(): return
            path = playlist[playlist_box.curselection()[0]]
            transcribe_btn.config(text="Processing...", state=tk.DISABLED)
            subtitle_box.delete(1.0, tk.END)
            subtitle_box.insert(tk.END, "Loading audio. Please wait...\n")
            result_text = ai_handler.transcribe_audio(current_api_key, path)
            subtitle_box.delete(1.0, tk.END)
            subtitle_box.insert(tk.END, result_text)
            sync_subtitles() 
        except Exception as e:
            subtitle_box.insert(tk.END, f"Error: {e}")
        finally:
            transcribe_btn.config(text="Generate Subtitles", state=tk.NORMAL)
    threading.Thread(target=thread_task, daemon=True).start()

def sync_subtitles(event=None):
    global subtitles
    subtitles = []
    raw_text = subtitle_box.get("1.0", tk.END).strip().split('\n')
    for line in raw_text:
        if '|' in line:
            try:
                times, text = line.split(''|'', 1)
                start, end = times.split('-')
                subtitles.append({
                    'start': time_to_sec(start.strip()),
                    'end': time_to_sec(end.strip()),
                    'text': text.strip()
                })
            except: pass

def update_loop():
    if pygame.mixer.music.get_busy() or paused:
        curr_time = get_current_time()
        
        if not is_dragging:
            slider.set(curr_time)
        curr_str = time.strftime('%M:%S', time.gmtime(curr_time))
        total_str = time.strftime('%M:%S', time.gmtime(slider.cget('to')))
        time_label.config(text=f"{curr_str} / {total_str}")

        current_lyric = "---"
        for sub in subtitles:
            if sub['start'] <= curr_time <= sub['end']:
                current_lyric = sub['text']
                break
        lyric_label.config(text=current_lyric)
        
        root.after(100, update_loop)


root.title("AI Music Player")
root.geometry("900x550")
left_frame = tk.Frame(root, padx=20, pady=20)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
tk.Label(left_frame, text="Playlist", font=("Arial", 12, "bold")).pack(anchor="w")
playlist_box = tk.Listbox(left_frame, bg="black", fg="white", height=10)
playlist_box.pack(fill=tk.BOTH, expand=True, pady=5)
tk.Label(left_frame, text="Now Playing:", font=("Arial", 10, "bold")).pack(pady=(10,0))
lyric_container = tk.Frame(left_frame, height=80, bg="#e8e8e8")
lyric_container.pack(fill=tk.X, pady=5)
lyric_container.pack_propagate(False) 
lyric_label = tk.Label(lyric_container, text="---", font=("Helvetica", 10, "bold"), fg="#4285F4", bg="#e8e8e8", wraplength=380)
lyric_label.pack(expand=True, fill=tk.BOTH)
time_label = tk.Label(left_frame, text="00:00 / 00:00")
time_label.pack(anchor="e")
slider = tk.Scale(left_frame, from_=0, to=100, orient=tk.HORIZONTAL)
slider.pack(fill=tk.X, pady=5)
slider.bind("<Button-1>", start_drag)
slider.bind("<ButtonRelease-1>", end_drag)
controls = tk.Frame(left_frame)
controls.pack(pady=10)
tk.Button(controls, text="PLAY", bg="green", fg="white", width=8, command=lambda: play_music(0)).pack(side=tk.LEFT, padx=5)
tk.Button(controls, text="PAUSE", width=8, command=toggle_pause).pack(side=tk.LEFT, padx=5)
tk.Button(controls, text="STOP", bg="red", fg="white", width=8, command=lambda: pygame.mixer.music.stop()).pack(side=tk.LEFT, padx=5)
tk.Button(left_frame, text="+ Add Song", command=add_song).pack(fill=tk.X)
right_frame = tk.Frame(root, bg="#f0f0f0", padx=20, pady=20)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
tk.Label(right_frame, text="AI Subtitles", font=("Arial", 12, "bold"), bg="#f0f0f0").pack()
subtitle_box = tk.Text(right_frame, height=20, width=40, font=("Consolas", 9))
subtitle_box.pack(fill=tk.BOTH, expand=True, pady=10)
subtitle_box.bind('<KeyRelease>', sync_subtitles)
transcribe_btn = tk.Button(right_frame, text="Generate Subtitles", bg="#4285F4", fg="white", command=generate_subtitles)
transcribe_btn.pack(pady=5)
root.mainloop()