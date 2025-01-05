import tkinter as tk
from tkinter import ttk, messagebox
import requests
import self
from PIL import Image, ImageTk
import io
import pygame
import webbrowser


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


        self.set_background_image("background.jpeg")

        # Start Screen
        self.start_screen()

    def set_background_image(self, image_path):

        try:
            image = Image.open(image_path)
            image = image.resize((1000, 700), Image.ANTIALIAS)
            self.background_image = ImageTk.PhotoImage(image)
            self.background_label = tk.Label(self.root, image=self.background_image)
            self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.background_label.lower()
        except Exception as e:
            print(f"Error loading background image: {e}")

    def start_screen(self):
        self.clear_window()
        start_frame = tk.Frame(self.root, bg="#001F3F")
        start_frame.pack(fill="both", expand=True)

        tk.Label(start_frame, text="Welcome to Movie Search App",
                 font=("Helvetica", 24, "bold"), bg="#001F3F", fg="#FFFFFF").pack(pady=50)
        tk.Label(start_frame, text="Search for movies, view details, and save to favourites!",
                 font=("Helvetica", 14), bg="#001F3F", fg="#FFFFFF").pack(pady=10)

        ttk.Button(start_frame, text="Start", command=self.search_screen).pack(pady=20)

    def search_screen(self):

        self.clear_window()


        search_frame = tk.Frame(self.root, bg="#001F3F")
        search_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(search_frame, text="Search Movies:", font=("Helvetica", 14), bg="#001F3F", fg="#FFFFFF").pack(side="left",
                                                                                                             padx=10)
        self.search_entry = ttk.Entry(search_frame, width=50)
        self.search_entry.pack(side="left", padx=10)
        ttk.Button(search_frame, text="Search", command=self.search_movies).pack(side="left", padx=10)

        # Results Frame with Scrollbar
        results_container = tk.Frame(self.root, bg="#001F3F")
        results_container.pack(fill="both", expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(results_container, bg="#001F3F")
        self.scrollbar = ttk.Scrollbar(results_container, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.results_frame = tk.Frame(self.canvas, bg="#001F3F")
        self.canvas.create_window((0, 0), window=self.results_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)

        self.results_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def search_movies(self):

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

        for widget in self.results_frame.winfo_children():
            widget.destroy()

        for movie in movies:
            self.display_movie(movie)

    def display_movie(self, movie):

        frame = tk.Frame(self.results_frame, bg="#001F3F", bd=2, relief="groove")
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
                photo = tk.PhotoImage()
        else:
            photo = tk.PhotoImage()

        poster_label = tk.Label(frame, image=photo, bg="#001F3F")
        poster_label.image = photo
        poster_label.pack(side="left", padx=5, pady=5)


        details_frame = tk.Frame(frame, bg="#001F3F")
        details_frame.pack(side="left", fill="both", expand=True)

        title = movie.get("title", "Unknown Title")
        overview = movie.get("overview", "No description available.")
        release_date = movie.get("release_date", "N/A")
        movie_url = f"https://www.themoviedb.org/movie/{movie.get('id', '')}"

        tk.Label(details_frame, text=title, font=("Helvetica", 14, "bold"), bg="#001F3F", fg="#FFFFFF").pack(anchor="w", padx=5, pady=2)
        tk.Label(details_frame, text=f"Release Date: {release_date}", font=("Helvetica", 10, "italic"),
                 bg="#001F3F", fg="#FFFFFF").pack(anchor="w", padx=5)
        tk.Label(details_frame, text=overview, font=("Helvetica", 10), bg="#001F3F", fg="#FFFFFF", wraplength=600, anchor="w",
                 justify="left").pack(padx=5, pady=5)


        btn_frame = tk.Frame(details_frame, bg="#001F3F")
        btn_frame.pack(anchor="w", padx=5, pady=5)

        ttk.Button(btn_frame, text="Save to Favourites", command=lambda: self.open_link(movie_url)).pack(
            side="left", padx=5)
        ttk.Button(btn_frame, text="Watch Now", command=lambda: self.open_link(movie_url)).pack(side="left", padx=5)

    def open_link(self, url):

        webbrowser.open(url)

    def clear_window(self):

        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = MovieApp(root)
    root.mainloop()


self.root.title("Movie Search App")
self.root.geometry("1000x1000")
self.set_background_image("background.jpeg")















