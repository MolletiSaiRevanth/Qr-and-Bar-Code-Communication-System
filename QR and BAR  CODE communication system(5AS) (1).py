import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import qrcode
import barcode
from barcode.writer import ImageWriter
from PIL import Image, ImageTk
import cv2
import numpy as np
import io
import os

class HybridCodeSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Hybrid QR & Barcode Communication System")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Color scheme
        self.bg_color = "#f0f0f0"
        self.primary_color = "#2196F3"
        self.root.configure(bg=self.bg_color)
        
        # Create main notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_generate_tab()
        self.create_scan_tab()
        
    def create_generate_tab(self):
        """Tab for generating QR codes and Barcodes"""
        generate_frame = tk.Frame(self.notebook, bg=self.bg_color)
        self.notebook.add(generate_frame, text="Generate Codes")
        
        # Input section
        input_frame = tk.LabelFrame(generate_frame, text="Enter Data", 
                                    bg=self.bg_color, font=("Arial", 12, "bold"))
        input_frame.pack(padx=20, pady=20, fill='x')
        
        tk.Label(input_frame, text="Enter text or data:", 
                bg=self.bg_color, font=("Arial", 10)).pack(anchor='w', padx=10, pady=5)
        
        self.data_entry = tk.Text(input_frame, height=4, width=60, font=("Arial", 10))
        self.data_entry.pack(padx=10, pady=5)
        
        # Code type selection
        type_frame = tk.Frame(input_frame, bg=self.bg_color)
        type_frame.pack(pady=10)
        
        tk.Label(type_frame, text="Select Code Type:", 
                bg=self.bg_color, font=("Arial", 10)).pack(side='left', padx=5)
        
        self.code_type = tk.StringVar(value="QR")
        tk.Radiobutton(type_frame, text="QR Code", variable=self.code_type, 
                      value="QR", bg=self.bg_color, font=("Arial", 10)).pack(side='left', padx=10)
        tk.Radiobutton(type_frame, text="Barcode (Code128)", variable=self.code_type, 
                      value="BARCODE", bg=self.bg_color, font=("Arial", 10)).pack(side='left', padx=10)
        
        # Generate button
        tk.Button(input_frame, text="Generate Code", command=self.generate_code,
                 bg=self.primary_color, fg="white", font=("Arial", 11, "bold"),
                 padx=20, pady=5).pack(pady=10)
        
        # Display section
        display_frame = tk.LabelFrame(generate_frame, text="Generated Code", 
                                     bg=self.bg_color, font=("Arial", 12, "bold"))
        display_frame.pack(padx=20, pady=10, fill='both', expand=True)
        
        self.image_label = tk.Label(display_frame, bg="white", text="Code will appear here")
        self.image_label.pack(padx=10, pady=10, fill='both', expand=True)
        
        # Save button
        tk.Button(display_frame, text="Save Code", command=self.save_code,
                 bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
                 padx=15, pady=5).pack(pady=10)
        
        self.current_image = None
        
    def create_scan_tab(self):
        """Tab for scanning QR codes and Barcodes"""
        scan_frame = tk.Frame(self.notebook, bg=self.bg_color)
        self.notebook.add(scan_frame, text="Scan Codes")
        
        # Button section
        button_frame = tk.Frame(scan_frame, bg=self.bg_color)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Select Image to Scan", command=self.scan_from_file,
                 bg=self.primary_color, fg="white", font=("Arial", 11, "bold"),
                 padx=20, pady=10).pack()
        
        # Image display
        img_frame = tk.LabelFrame(scan_frame, text="Scanned Image", 
                                 bg=self.bg_color, font=("Arial", 12, "bold"))
        img_frame.pack(padx=20, pady=10, fill='both', expand=True)
        
        self.scan_image_label = tk.Label(img_frame, bg="white", text="No image loaded")
        self.scan_image_label.pack(padx=10, pady=10, fill='both', expand=True)
        
        # Result display
        result_frame = tk.LabelFrame(scan_frame, text="Decoded Data", 
                                    bg=self.bg_color, font=("Arial", 12, "bold"))
        result_frame.pack(padx=20, pady=10, fill='both', expand=True)
        
        self.result_text = tk.Text(result_frame, height=6, width=70, 
                                   font=("Arial", 10), state='disabled')
        self.result_text.pack(padx=10, pady=10)
        
    def generate_code(self):
        """Generate QR code or Barcode based on selection"""
        data = self.data_entry.get("1.0", "end-1c").strip()
        
        if not data:
            messagebox.showwarning("Warning", "Please enter data to encode!")
            return
        
        try:
            if self.code_type.get() == "QR":
                self.generate_qr(data)
            else:
                self.generate_barcode(data)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate code:\n{str(e)}")
    
    def generate_qr(self, data):
        """Generate QR code"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        self.current_image = img
        self.display_image(img)
        messagebox.showinfo("Success", "QR Code generated successfully!")
    
    def generate_barcode(self, data):
        """Generate Barcode (Code128)"""
        # Barcode requires alphanumeric data
        code128 = barcode.get_barcode_class('code128')
        barcode_instance = code128(data, writer=ImageWriter())
        
        # Save to bytes buffer
        buffer = io.BytesIO()
        barcode_instance.write(buffer)
        buffer.seek(0)
        
        img = Image.open(buffer)
        self.current_image = img
        self.display_image(img)
        messagebox.showinfo("Success", "Barcode generated successfully!")
    
    def display_image(self, img):
        """Display image in the GUI"""
        # Resize image to fit in the display area
        img_copy = img.copy()
        img_copy.thumbnail((400, 400), Image.Resampling.LANCZOS)
        
        photo = ImageTk.PhotoImage(img_copy)
        self.image_label.configure(image=photo, text="")
        self.image_label.image = photo
    
    def save_code(self):
        """Save generated code to file"""
        if self.current_image is None:
            messagebox.showwarning("Warning", "No code to save! Generate a code first.")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        
        if file_path:
            self.current_image.save(file_path)
            messagebox.showinfo("Success", f"Code saved to:\n{file_path}")
    
    def scan_from_file(self):
        """Scan QR code or Barcode from image file using OpenCV"""
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            # Display the image
            img = Image.open(file_path)
            img_copy = img.copy()
            img_copy.thumbnail((400, 400), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img_copy)
            self.scan_image_label.configure(image=photo, text="")
            self.scan_image_label.image = photo
            
            # Read image with OpenCV
            image = cv2.imread(file_path)
            
            # Try QR Code detection first
            qr_detector = cv2.QRCodeDetector()
            data, bbox, _ = qr_detector.detectAndDecode(image)
            
            result = ""
            found = False
            
            if data:
                result += "QR Code Found!\n"
                result += f"Type: QR Code\n"
                result += f"Data: {data}\n"
                result += "-" * 50 + "\n"
                found = True
            
            # Try Barcode detection using simple edge detection
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply thresholding
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Try to read barcode using contour detection (basic approach)
            # Note: This is a simplified barcode detection, not as robust as pyzbar
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = w / float(h)
                # Barcodes typically have high aspect ratio
                if aspect_ratio > 3 and w > 100:
                    result += "Barcode-like pattern detected!\n"
                    result += "(For accurate barcode reading, install pyzbar library)\n"
                    result += "-" * 50 + "\n"
                    found = True
                    break
            
            if found:
                self.result_text.configure(state='normal')
                self.result_text.delete("1.0", "end")
                self.result_text.insert("1.0", result)
                self.result_text.configure(state='disabled')
                messagebox.showinfo("Success", "Code detected successfully!")
            else:
                self.result_text.configure(state='normal')
                self.result_text.delete("1.0", "end")
                self.result_text.insert("1.0", "No QR code or Barcode found in the image!\n\n"
                                              "Tips:\n"
                                              "- Make sure the code is clear and visible\n"
                                              "- Try a higher resolution image\n"
                                              "- Ensure good lighting in the image")
                self.result_text.configure(state='disabled')
                messagebox.showwarning("Warning", "No code found in the image!")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to scan code:\n{str(e)}")

def main():
    root = tk.Tk()
    app = HybridCodeSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()