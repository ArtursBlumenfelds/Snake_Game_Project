import tkinter as tk
from tkinter import ttk, messagebox
import csv
from datetime import datetime, date

SCORES_FILE = "scores.csv"

def load_scores():
    try:
        with open(SCORES_FILE, "r") as file:
            reader = csv.reader(file)
            scores = []
            for row in reader:
                if len(row) == 3:
                    try:
                        name = row[0]
                        score = int(row[1])
                        score_date = datetime.strptime(row[2], "%Y-%m-%d")
                        scores.append((name, score, score_date))
                    except ValueError:
                        continue
            return scores
    except FileNotFoundError:
        return []

def save_scores(scores):
    with open(SCORES_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        for name, score, score_date in scores:
            writer.writerow([name, score, score_date.strftime("%Y-%m-%d")])

def filter_scores(scores, name_filter="", min_score=None):
    return [s for s in scores if (name_filter.lower() in s[0].lower()) and (min_score is None or s[1] >= min_score)]

class ScoreManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Score Manager")
        self.geometry("700x400")

        self.scores = load_scores()
        self.create_widgets()
        self.display_scores(self.scores)

    def create_widgets(self):
        self.tree = ttk.Treeview(self, columns=("Name", "Score", "Date"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Score", text="Score")
        self.tree.heading("Date", text="Date")
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

        sort_frame = tk.Frame(self)
        sort_frame.pack(pady=5)

        tk.Button(sort_frame, text="Sort by Name", command=lambda: self.sort_scores("name")).pack(side=tk.LEFT, padx=5)
        tk.Button(sort_frame, text="Sort by Score", command=lambda: self.sort_scores("score")).pack(side=tk.LEFT, padx=5)
        tk.Button(sort_frame, text="Newest First", command=lambda: self.sort_scores("date_newest")).pack(side=tk.LEFT, padx=5)
        tk.Button(sort_frame, text="Oldest First", command=lambda: self.sort_scores("date_oldest")).pack(side=tk.LEFT, padx=5)

    def display_scores(self, scores):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for name, score, score_date in scores:
            self.tree.insert("", tk.END, values=(name, score, score_date.strftime("%Y-%m-%d")))

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
        elif mode == "date_newest":
            sorted_scores = sorted(self.scores, key=lambda x: x[2], reverse=True)
        elif mode == "date_oldest":
            sorted_scores = sorted(self.scores, key=lambda x: x[2])
        else:
            sorted_scores = self.scores
        self.display_scores(sorted_scores)

if __name__ == "__main__":
    app = ScoreManager()
    app.mainloop()