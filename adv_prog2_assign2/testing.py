import tkinter as tk
from tkinter import ttk, messagebox
import requests
from PIL import Image, ImageTk
import io
import pygame

# TMDB API setup
API_KEY = "abb83470db14bcf626cb0852af8ba901"
BASE_URL = "https://api.themoviedb.org/3/search/movie"
POSTER_BASE_URL = "https://image.tmdb.org/t/p/w200"

class MovieApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Search App")
        self.root.geometry("1000x700")  # Set window size
        pygame.mixer.init()
        pygame.mixer.music.load("background.mp3")
        pygame.mixer.music.play(-1)  # Loop sound

        # Add background image
        self.set_background_image("background.jpeg")

        # Start Screen
        self.start_screen()

    def set_background_image(self, image_path):
        """Set a background image for the app."""
        try:
            image = Image.open(image_path)
            image = image.resize((1000, 700), Image.ANTIALIAS)
            self.background_image = ImageTk.PhotoImage(image)
            self.background_label = tk.Label(self.root, image=self.background_image)
            self.background_label.place(relwidth=1, relheight=1)
        except Exception as e:
            print(f"Error loading background image: {e}")

    def start_screen(self):
        """Initial screen with app description and Start button."""
        self.clear_window()
        start_frame = tk.Frame(self.root, bg="navy")
        start_frame.pack(fill="both", expand=True)

        tk.Label(start_frame, text="Welcome to Movie Search App",
                 font=("Helvetica", 24, "bold"), bg="navy", fg="white").pack(pady=50)
        tk.Label(start_frame, text="Search for movies, view details, and save to favourites!",
                 font=("Helvetica", 14), bg="navy", fg="white").pack(pady=10)

        ttk.Button(start_frame, text="Start", command=self.search_screen).pack(pady=20)

    def search_screen(self):
        """Screen with search functionality and results display."""
        self.clear_window()

        # Top Frame for Search Bar
        search_frame = tk.Frame(self.root, bg="navy")
        search_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(search_frame, text="Search Movies:", font=("Helvetica", 14), bg="navy", fg="white").pack(side="left",
                                                                                                          padx=10)
        self.search_entry = ttk.Entry(search_frame, width=50)
        self.search_entry.pack(side="left", padx=10)
        ttk.Button(search_frame, text="Search", command=self.search_movies).pack(side="left", padx=10)

        # Results Frame with Scrollbar
        results_container = tk.Frame(self.root, bg="white")
        results_container.pack(fill="both", expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(results_container, bg="white")
        self.scrollbar = ttk.Scrollbar(results_container, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.results_frame = tk.Frame(self.canvas, bg="white")
        self.canvas.create_window((0, 0), window=self.results_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)

        self.results_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def search_movies(self):
        """Fetch and display movies from the API."""
        query = self.search_entry.get()
        if not query:
            messagebox.showerror("Error", "Please enter a movie name.")
            return

        url = f"{BASE_URL}?api_key={API_KEY}&query={query}"
        response = requests.get(url)
        if response.status_code != 200:
            messagebox.showerror("Error", "Failed to fetch movies. Please try again.")
            return

        data = response.json()
        movies = data.get("results", [])
        if not movies:
            messagebox.showinfo("No Results", "No movies found for your search.")
            return

        self.display_results(movies)

    def display_results(self, movies):
        """Display all movies returned by the API."""
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        for movie in movies:
            self.display_movie(movie)

    def display_movie(self, movie):
        """Display a single movie's details."""
        frame = tk.Frame(self.results_frame, bg="white", bd=2, relief="groove")
        frame.pack(fill="x", padx=10, pady=5)

        # Poster Image
        poster_path = movie.get("poster_path")
        if poster_path:
            poster_url = POSTER_BASE_URL + poster_path
            try:
                response = requests.get(poster_url)
                poster_img = Image.open(io.BytesIO(response.content))
                poster_img = poster_img.resize((100, 150))
                photo = ImageTk.PhotoImage(poster_img)
            except Exception:
                photo = tk.PhotoImage()  # Default empty image
        else:
            photo = tk.PhotoImage()

        poster_label = tk.Label(frame, image=photo, bg="white")
        poster_label.image = photo
        poster_label.pack(side="left", padx=5, pady=5)

        # Movie Details
        details_frame = tk.Frame(frame, bg="white")
        details_frame.pack(side="left", fill="both", expand=True)

        title = movie.get("title", "Unknown Title")
        overview = movie.get("overview", "No description available.")
        release_date = movie.get("release_date", "N/A")

        tk.Label(details_frame, text=title, font=("Helvetica", 14, "bold"), bg="white").pack(anchor="w", padx=5, pady=2)
        tk.Label(details_frame, text=f"Release Date: {release_date}", font=("Helvetica", 10, "italic"),
                 bg="white").pack(anchor="w", padx=5)
        tk.Label(details_frame, text=overview, font=("Helvetica", 10), bg="white", wraplength=600, anchor="w",
                 justify="left").pack(padx=5, pady=5)

        # Buttons
        btn_frame = tk.Frame(details_frame, bg="white")
        btn_frame.pack(anchor="w", padx=5, pady=5)

        ttk.Button(btn_frame, text="Save to Favourites", command=lambda: self.add_to_favourites(title)).pack(
            side="left", padx=5)
        ttk.Button(btn_frame, text="Watch Now", command=lambda: self.watch_now(title)).pack(side="left", padx=5)

    def add_to_favourites(self, title):
        messagebox.showinfo("Favourites", f"{title} added to favourites!")

    def watch_now(self, title):
        messagebox.showinfo("Watch Now", f"Enjoy watching {title}!")

    def clear_window(self):
        """Clear all widgets from the window."""
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = MovieApp(root)
    root.mainloop()
