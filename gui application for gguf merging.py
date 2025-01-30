#!/usr/bin/env python3
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess

def merge_splits():
    # Hide the main window so only the file picker appears
    root.withdraw()

    # Ask the user to select the first split file
    selected_path = filedialog.askopenfilename(
        title="Select the first part of the split",
        filetypes=[("GGUF Files", "*.gguf"), ("All Files", "*.*")]
    )
    if not selected_path:
        messagebox.showinfo("Aborted", "No file selected. Exiting.")
        return

    # Extract filename and directory
    filename = os.path.basename(selected_path)
    dir_path = os.path.dirname(selected_path)

    # Derive the base name by removing "-000..." (adjust if your naming is different)
    if "-000" in filename:
        base_name_part = filename.split("-000")[0]
    else:
        # If there's no "-000" substring, just remove the extension
        base_name_part, _ = os.path.splitext(filename)

    # Assume the final merged file should have ".gguf" extension
    final_output_name = base_name_part + ".gguf"

    # Build full path for the merged file
    output_path = os.path.join(dir_path, final_output_name)

    # Construct the merge command
    command = [
        "unbuffer",
        "llama-gguf-split",
        "--merge",
        selected_path,
        output_path
    ]

    try:
        # Use Popen to read output line by line in real time
        with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True) as proc:
            for line in proc.stdout:
                # Print each line as it arrives (line already includes a newline)
                print(line, end='')
            proc.wait()

            if proc.returncode == 0:
                messagebox.showinfo("Success", f"Merged successfully to:\n{output_path}")
            else:
                messagebox.showerror("Error", f"Merge command exited with code {proc.returncode}")

    except FileNotFoundError:
        messagebox.showerror("Error", "Could not find 'llama-gguf-split' in PATH.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")

def main():
    global root
    root = tk.Tk()
    root.title("Merge Splits")
    root.geometry("300x100")

    # A button to initiate the merge; optionally, you could just run merge_splits() at startup
    merge_button = tk.Button(root, text="Select and Merge Splits", command=merge_splits)
    merge_button.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()

