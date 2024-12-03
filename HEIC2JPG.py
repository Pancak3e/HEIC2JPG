import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image
import pillow_heif  # Library to handle HEIC file decoding
import os

# Class to handle HEIC to JPG conversion using a graphical interface
class HeicConverter:
    def __init__(self, root):
        """
        Initialize the GUI application with a root window and widgets.
        
        Args:
            root (tk.Tk): The main Tkinter root window.
        """
        self.root = root
        self.root.title("HEIC to JPG Converter")  # Set the window title
        
        # Create the main frame for the application
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Button to select HEIC files
        self.select_button = ttk.Button(main_frame, text="Select HEIC Files", command=self.select_files)
        self.select_button.grid(row=0, column=0, pady=5)
        
        # Progress bar to show conversion progress
        self.progress = ttk.Progressbar(main_frame, length=300, mode='determinate')
        self.progress.grid(row=1, column=0, pady=5)
        
        # Label to display current status
        self.status_label = ttk.Label(main_frame, text="Ready")
        self.status_label.grid(row=2, column=0, pady=5)

    def reset_ui(self):
        """
        Reset the UI elements to their initial state after a conversion process.
        """
        self.progress['value'] = 0
        self.status_label['text'] = "Ready"
        self.select_button['state'] = 'normal'

    def select_files(self):
        """
        Open a file dialog to select HEIC files for conversion.
        """
        files = filedialog.askopenfilenames(
            filetypes=[("HEIC files", "*.heic"), ("All files", "*.*")]
        )
        if files:
            self.select_button['state'] = 'disabled'  # Disable the button to prevent re-selection
            self.convert_files(files)

    def convert_files(self, files):
        """
        Convert the selected HEIC files to JPG format.

        Args:
            files (list): List of file paths for the selected HEIC files.
        """
        total_files = len(files)  # Total number of files to process
        self.progress['maximum'] = total_files
        converted_count = 0  # Counter for successfully converted files
        
        for i, file in enumerate(files, 1):
            try:
                # Read the HEIC file using pillow_heif
                heif_file = pillow_heif.read_heif(file)
                image = Image.frombytes(
                    heif_file.mode,  # Image mode (e.g., RGB)
                    heif_file.size,  # Image size (width, height)
                    heif_file.data,  # Image data
                    "raw"  # Raw format for decoding
                )
                
                # Construct the output path and save the image as JPG
                output_path = os.path.splitext(file)[0] + '.jpg'
                image.save(output_path, 'JPEG')
                converted_count += 1  # Increment the counter for successful conversions
                
                # Update the progress bar and status label
                self.progress['value'] = i
                self.status_label['text'] = f"Converting: {i}/{total_files}"
                self.root.update()  # Refresh the UI
                
            except Exception as e:
                # Show an error message if conversion fails for a file
                messagebox.showerror("Error", f"Error converting {os.path.basename(file)}: {str(e)}")
        
        # Display success message and reset the UI
        if converted_count > 0:
            messagebox.showinfo("Success", f"Successfully converted {converted_count} files!")
        self.reset_ui()

if __name__ == "__main__":
    # Initialize and run the application
    root = tk.Tk()
    app = HeicConverter(root)
    root.mainloop()
