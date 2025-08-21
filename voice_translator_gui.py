# voice_translator_gui.py

import tkinter as tk
from tkinter import ttk, scrolledtext
import sounddevice as sd
import queue
import numpy as np
import speech_recognition as sr
import pyttsx3
from googletrans import Translator
import threading
import time

# Initialize recognizer, translator, and TTS
recognizer = sr.Recognizer()
translator = Translator()
tts = pyttsx3.init()

audio_queue = queue.Queue()

# -------------------------
# Updated speak_text() function
# -------------------------
def speak_text(text, lang='en'):
    """
    Speaks the text aloud.
    lang: 'en' for English, 'es' for Spanish
    """
    # Set the appropriate voice for English or Spanish
    voices = tts.getProperty('voices')
    if lang == 'es':
        # Try to find a Spanish voice
        for voice in voices:
            if "Spanish" in voice.name or "es" in voice.id.lower():
                tts.setProperty('voice', voice.id)
                break
    else:
        # Default English voice
        for voice in voices:
            if "English" in voice.name or "en" in voice.id.lower():
                tts.setProperty('voice', voice.id)
                break

    tts.say(text)
    tts.runAndWait()

# -------------------------
# Other functions (unchanged)
# -------------------------
def record_audio(duration=5, chunk=1024):
    """
    Records audio from microphone and returns concatenated np array
    """
    audio_buffer = []

    def callback(indata, frames, time_info, status):
        if status:
            print(status, flush=True)
        audio_queue.put(indata.copy())

    with sd.InputStream(channels=1, samplerate=16000, blocksize=chunk, callback=callback):
        start_time = time.time()
        while time.time() - start_time < duration:
            try:
                data = audio_queue.get(timeout=1)
                audio_buffer.append(data)
            except queue.Empty:
                pass

    if audio_buffer:
        audio_np = np.concatenate(audio_buffer, axis=0).flatten()
        return (audio_np * 32767).astype('int16')
    return None

def recognize_and_translate(lang_code, display_widget):
    """
    Recognize speech in selected language and translate it.
    lang_code: 'en' or 'es'
    """
    display_widget.insert(tk.END, f"\nListening in {lang_code}...\n")
    display_widget.see(tk.END)
    audio_data = record_audio(duration=5)
    if audio_data is None:
        display_widget.insert(tk.END, "No audio detected.\n")
        return

    audio_obj = sr.AudioData(audio_data.tobytes(), 16000, 2)
    try:
        if lang_code == 'en':
            src = 'en-US'
            dest = 'es'
        else:
            src = 'es-ES'
            dest = 'en'

        text = recognizer.recognize_google(audio_obj, language=src)
        display_widget.insert(tk.END, f"You said ({lang_code}): {text}\n")
        display_widget.see(tk.END)

        translation = translator.translate(text, src=lang_code, dest=dest).text
        display_widget.insert(tk.END, f"Translation ({dest}): {translation}\n")
        display_widget.see(tk.END)

        # Speak translation
        speak_text(translation, lang=dest)

    except sr.UnknownValueError:
        display_widget.insert(tk.END, "Could not understand audio.\n")
        display_widget.see(tk.END)

# -------------------------
# GUI Setup
# -------------------------
def start_translation(display_widget, lang_var):
    # Run in separate thread to avoid freezing GUI
    t = threading.Thread(target=recognize_and_translate, args=(lang_var.get(), display_widget))
    t.start()

root = tk.Tk()
root.title("Live Voice Translator")

# Language selection
lang_var = tk.StringVar(value='en')
lang_label = ttk.Label(root, text="Select input language:")
lang_label.pack(pady=5)

lang_dropdown = ttk.Combobox(root, textvariable=lang_var, values=['en', 'es'], state="readonly")
lang_dropdown.pack(pady=5)
lang_dropdown.set('en')  # default English

# Start button
start_btn = ttk.Button(root, text="Start", command=lambda: start_translation(output_text, lang_var))
start_btn.pack(pady=10)

# Output display
output_text = scrolledtext.ScrolledText(root, width=60, height=15)
output_text.pack(pady=10)

root.mainloop()
