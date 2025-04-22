import tkinter as tk
from tkinter import ttk, messagebox
import csv

SCORES_FILE = "scores.csv"

def load_scores():
    try:
        with open(SCORES_FILE, "r") as file:
            reader = csv.reader(file)
            scores = []
            for row in reader:
                if len(row) == 2:
                    try:
                        scores.append((row[0], int(row[1])))
                    except ValueError:
                        continue
            return scores
    except FileNotFoundError:
        return []

def save_scores(scores):
    with open(SCORES_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        for name, score in scores:
            writer.writerow([name, score])

def filter_scores(scores, name_filter="", min_score=None):
    return [s for s in scores if (name_filter.lower() in s[0].lower()) and (min_score is None or s[1] >= min_score)]

def count_scores_in_range(scores, min_val, max_val):
    return sum(min_val <= score <= max_val for _, score in scores)

class ScoreManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Score Manager")
        self.geometry("600x400")

        self.scores = load_scores()
        self.create_widgets()
        self.display_scores(self.scores)

    def create_widgets(self):
        self.tree = ttk.Treeview(self, columns=("Name", "Score"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Score", text="Score")
        self.tree.pack(fill=tk.BOTH, expand=True)

        frame = tk.Frame(self)
        frame.pack(pady=5)

        tk.Label(frame, text="Name contains:").grid(row=0, column=0)
        self.name_filter = tk.Entry(frame)
        self.name_filter.grid(row=0, column=1)

        tk.Label(frame, text="Min score:").grid(row=0, column=2)
        self.min_score = tk.Entry(frame)
        self.min_score.grid(row=0, column=3)

        tk.Button(frame, text="Filter", command=self.apply_filters).grid(row=0, column=4, padx=5)
        tk.Button(frame, text="Clear", command=self.clear_filters).grid(row=0, column=5, padx=5)

    def display_scores(self, scores):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for name, score in scores:
            self.tree.insert("", tk.END, values=(name, score))

    def apply_filters(self):
        name_text = self.name_filter.get()
        try:
            min_val = int(self.min_score.get()) if self.min_score.get() else None
        except ValueError:
            messagebox.showerror("Invalid Input", "Min score must be an integer")
            return
        filtered = filter_scores(self.scores, name_filter=name_text, min_score=min_val)
        self.display_scores(filtered)

    def clear_filters(self):
        self.name_filter.delete(0, tk.END)
        self.min_score.delete(0, tk.END)
        self.display_scores(self.scores)

    def sort_scores(self, mode):
        if mode == "name":
            sorted_scores = sorted(self.scores, key=lambda x: x[0].lower())
        elif mode == "score":
            sorted_scores = sorted(self.scores, key=lambda x: x[1], reverse=True)
        else:
            sorted_scores = sorted(self.scores, key=lambda x: (x[0].lower(), -x[1]))
        self.display_scores(sorted_scores)

    def count_range(self):
        count = count_scores_in_range(self.scores, 10, 50)
        messagebox.showinfo("Count", f"Scores between 10–50: {count}")

if __name__ == "__main__":
    app = ScoreManager()
    app.mainloop()
