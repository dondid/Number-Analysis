import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import numpy as np


class NumberAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Analysis App")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        try:
            icon_image = tk.PhotoImage(file="inf.png")
            self.root.iconphoto(True, icon_image)
        except:
            pass  # In case the icon isn't available
        self.root.geometry("1000x700")

        self.numbers = []

        # Create frames
        self.input_frame = tk.Frame(root, bg="#f0f0f0")
        self.input_frame.pack(fill=tk.X, padx=20, pady=20)

        self.result_frame = tk.Frame(root, bg="#f0f0f0")
        self.result_frame.pack(fill=tk.X, padx=20)

        self.graph_frame = tk.Frame(root, bg="#f0f0f0")
        self.graph_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Input elements
        self.create_input_widgets()

        # Result elements
        self.create_result_widgets()

        # Graph elements
        self.create_graph()

    def create_input_widgets(self):
        # Number input
        tk.Label(self.input_frame, text="Enter a number:", bg="#f0f0f0", font=("Arial", 12)).grid(row=0, column=0,
                                                                                                  padx=5, pady=5)
        self.number_entry = tk.Entry(self.input_frame, width=15, font=("Arial", 12))
        self.number_entry.grid(row=0, column=1, padx=5, pady=5)
        self.number_entry.bind("<Return>", lambda event: self.add_number())

        self.add_button = tk.Button(self.input_frame, text="✅", command=self.add_number,
                                    bg="#4CAF50", fg="white", font=("Arial", 10))
        self.add_button.grid(row=0, column=2, padx=5, pady=5)

        # File input
        self.file_button = tk.Button(self.input_frame, text="⬇️", command=self.load_from_file,
                                     bg="#2196F3", fg="white", font=("Arial", 10))
        self.file_button.grid(row=0, column=3, padx=5, pady=5)

        # Clear button
        self.clear_button = tk.Button(self.input_frame, text="❌", command=self.clear_data,
                                      bg="#f44336", fg="white", font=("Arial", 10))
        self.clear_button.grid(row=0, column=4, padx=5, pady=5)

        # Numbers list
        tk.Label(self.input_frame, text="Current Numbers:", bg="#f0f0f0", font=("Arial", 12)).grid(row=1, column=0,
                                                                                                   padx=5, pady=5)
        self.numbers_text = tk.Text(self.input_frame, width=50, height=5, font=("Arial", 10))
        self.numbers_text.grid(row=1, column=1, columnspan=4, padx=5, pady=5)
        self.numbers_text.config(state=tk.DISABLED)

    def create_result_widgets(self):
        # Results display
        result_style = {"bg": "#f0f0f0", "font": ("Arial", 12), "pady": 5}

        tk.Label(self.result_frame, text="Minimum:", **result_style).grid(row=0, column=0, sticky="w")
        self.min_label = tk.Label(self.result_frame, text="N/A", width=15, **result_style)
        self.min_label.grid(row=0, column=1, sticky="w")

        tk.Label(self.result_frame, text="Maximum:", **result_style).grid(row=1, column=0, sticky="w")
        self.max_label = tk.Label(self.result_frame, text="N/A", width=15, **result_style)
        self.max_label.grid(row=1, column=1, sticky="w")

        tk.Label(self.result_frame, text="Sum:", **result_style).grid(row=2, column=0, sticky="w")
        self.sum_label = tk.Label(self.result_frame, text="N/A", width=15, **result_style)
        self.sum_label.grid(row=2, column=1, sticky="w")

        tk.Label(self.result_frame, text="Average:", **result_style).grid(row=0, column=2, sticky="w", padx=(20, 0))
        self.avg_label = tk.Label(self.result_frame, text="N/A", width=15, **result_style)
        self.avg_label.grid(row=0, column=3, sticky="w")

        tk.Label(self.result_frame, text="Count:", **result_style).grid(row=1, column=2, sticky="w", padx=(20, 0))
        self.count_label = tk.Label(self.result_frame, text="0", width=15, **result_style)
        self.count_label.grid(row=1, column=3, sticky="w")

    def create_graph(self):
        self.figure, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(10, 5))
        self.figure.set_facecolor("#f0f0f0")

        self.canvas = FigureCanvasTkAgg(self.figure, self.graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Initialize empty graphs
        self.update_graph()

    def getint(self, text):
        """Function to convert text to integer, handling potential errors"""
        try:
            return int(text)
        except ValueError:
            try:
                return float(text)
            except ValueError:
                messagebox.showerror("Invalid Input", f"'{text}' is not a valid number.")
                return None

    def add_number(self):
        number_text = self.number_entry.get().strip()
        if number_text:
            number = self.getint(number_text)
            if number is not None:
                self.numbers.append(number)
                self.update_display()
                self.number_entry.delete(0, tk.END)

    def load_from_file(self):
        file_path = filedialog.askopenfilename(
            title="Select a file with numbers",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )

        if file_path:
            try:
                with open(file_path, 'r') as file:
                    for line in file:
                        for number_str in line.split():
                            number = self.getint(number_str)
                            if number is not None:
                                self.numbers.append(number)
                self.update_display()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read file: {str(e)}")

    def clear_data(self):
        self.numbers = []
        self.update_display()

    def update_display(self):
        # Update numbers list
        self.numbers_text.config(state=tk.NORMAL)
        self.numbers_text.delete(1.0, tk.END)
        if self.numbers:
            self.numbers_text.insert(tk.END, ", ".join(map(str, self.numbers)))
        self.numbers_text.config(state=tk.DISABLED)

        # Update stats
        if self.numbers:
            self.min_label.config(text=str(min(self.numbers)))
            self.max_label.config(text=str(max(self.numbers)))
            self.sum_label.config(text=str(sum(self.numbers)))
            self.avg_label.config(text=f"{sum(self.numbers) / len(self.numbers):.2f}")
            self.count_label.config(text=str(len(self.numbers)))
        else:
            self.min_label.config(text="N/A")
            self.max_label.config(text="N/A")
            self.sum_label.config(text="N/A")
            self.avg_label.config(text="N/A")
            self.count_label.config(text="0")

        # Update graph
        self.update_graph()

    def update_graph(self):
        # Clear previous plots
        self.ax1.clear()
        self.ax2.clear()

        if self.numbers:
            # Line graph
            x = range(len(self.numbers))
            self.ax1.plot(x, self.numbers, 'o-', color='#2196F3')
            self.ax1.set_title('Number Sequence')
            self.ax1.set_xlabel('Index')
            self.ax1.set_ylabel('Value')
            self.ax1.grid(True, linestyle='--', alpha=0.7)

            # Histogram
            self.ax2.hist(self.numbers, bins=min(10, len(set(self.numbers))), color='#4CAF50', alpha=0.7)
            self.ax2.set_title('Distribution')
            self.ax2.set_xlabel('Value')
            self.ax2.set_ylabel('Frequency')
            self.ax2.grid(True, linestyle='--', alpha=0.7)
        else:
            self.ax1.set_title('Number Sequence')
            self.ax1.set_xlabel('Index')
            self.ax1.set_ylabel('Value')
            self.ax1.text(0.5, 0.5, 'No data available', ha='center', va='center', transform=self.ax1.transAxes)

            self.ax2.set_title('Distribution')
            self.ax2.set_xlabel('Value')
            self.ax2.set_ylabel('Frequency')
            self.ax2.text(0.5, 0.5, 'No data available', ha='center', va='center', transform=self.ax2.transAxes)

        self.figure.tight_layout()
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = NumberAnalysisApp(root)
    root.mainloop()