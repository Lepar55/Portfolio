import google.generativeai as genai
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
import base64
import asyncio
import cv2
import io
import threading

API_KEY = "AIzaSyBm3YrcpEBKF40_g2AJp6437EDJr5gCUTA"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

class ImageQAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Q&A")
        self.root.geometry("650x750")
        self.root.configure(bg="#2E3440")

        style = ttk.Style()
        style.configure("TFrame", background="#2E3440")
        style.configure("TLabel", background="#2E3440", foreground="white", font=("Arial", 12))
        style.configure("TButton", font=("Arial", 12, "bold"), padding=5)
        style.map("TButton", background=[("active", "#88C0D0")])

        self.btn_load = ttk.Button(root, text="📂 Load Image", command=self.load_image)
        self.btn_load.pack(pady=10)

        self.btn_camera = ttk.Button(root, text="📸 Start Camera", command=self.start_camera)
        self.btn_camera.pack(pady=10)

        self.btn_stop_camera = ttk.Button(root, text="🛑 Stop Camera", command=self.stop_camera, state=tk.DISABLED)
        self.btn_stop_camera.pack(pady=10)

        self.img_label = ttk.Label(root)
        self.img_label.pack()

        self.question_label = ttk.Label(root, text="Enter your question:")
        self.question_label.pack(pady=5)

        self.question_entry = tk.Text(root, height=3, width=60, font=("Arial", 12))
        self.question_entry.pack()

        self.btn_ask = ttk.Button(root, text="🔎 Ask", command=self.ask_question)
        self.btn_ask.pack(pady=10)

        self.answer_label = ttk.Label(root, text="Answer:")
        self.answer_label.pack(pady=5)

        self.answer_text = tk.Text(root, height=10, width=70, font=("Arial", 12), bg="#3B4252", fg="white")
        self.answer_text.pack()

        self.image_path = None
        self.cap = None
        self.running = False

    def load_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if self.image_path:
            image = Image.open(self.image_path)
            image.thumbnail((200, 200))
            photo = ImageTk.PhotoImage(image)
            self.img_label.config(image=photo)
            self.img_label.image = photo

    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.update_answer_text("Unable to access the camera.")
            return
        
        self.running = True
        self.btn_camera.config(state=tk.DISABLED)
        self.btn_stop_camera.config(state=tk.NORMAL)
        self.update_camera()

    def stop_camera(self):
        self.running = False
        if self.cap:
            self.cap.release()
        self.cap = None
        self.btn_camera.config(state=tk.NORMAL)
        self.btn_stop_camera.config(state=tk.DISABLED)

    def update_camera(self):
        if self.running:
            ret, frame = self.cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(frame_rgb)
                image.thumbnail((400, 400))
                photo = ImageTk.PhotoImage(image)
                self.img_label.config(image=photo)
                self.img_label.image = photo
            self.root.after(10, self.update_camera)

    def ask_question(self):
        threading.Thread(target=self.ask_question_async).start()

    def ask_question_async(self):
        question = self.question_entry.get("1.0", tk.END).strip()
        if not question:
            self.update_answer_text("Please enter a question.")
            return

        self.update_answer_text(" Processing...")
        image_data = None

        if self.running:
            ret, frame = self.cap.read()
            if ret:
                image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image_rgb)
                image_data = self.image_to_base64(image)
        elif self.image_path:
            with open(self.image_path, "rb") as img_file:
                image_data = base64.b64encode(img_file.read()).decode("utf-8")

        response = self.get_response(image_data, question)
        self.update_answer_text("💡 " + response)

    def get_response(self, image_data, question):
        try:
            request = [{"text": question}]
            if image_data:
                request.insert(0, {"inline_data": {"mime_type": "image/jpeg", "data": image_data}})
            
            response = model.generate_content(request)
            return "\n".join(chunk.text for chunk in response)
        except Exception as e:
            return f"⚠️ Error: {str(e)}"

    def image_to_base64(self, image):
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")
        return base64.b64encode(buffer.getvalue()).decode("utf-8")

    def update_answer_text(self, text):
        self.root.after(0, lambda: self.answer_text.delete("1.0", tk.END))
        self.root.after(0, lambda: self.answer_text.insert(tk.END, text))

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageQAApp(root)
    root.mainloop()