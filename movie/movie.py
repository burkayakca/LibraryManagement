class Movie:
    def __init__(self,name,director,year,genre):
        self.name = name
        self.director = director
        self.year = year
        self.genre = genre

movie1 = Movie("john wick","ridley scott","2010","action")
movie2 = Movie("john","scott","2015","SciFi")

class MovieManager: 
    def __init__(self):
        self.movieDB = {}

    def addMovie(self,movie):
        if movie not in self.movieDB:
            self.movieDB.update({ movie.name : {
                "director" : movie.director,
                "year": movie.year,
                "genre": movie.genre
                }
            })
        else:
            print("Bu film zaten mevcut.")
    
    def removeMovie(self,movie):
        if movie in self.movieDB:
            del self.movieDB[movie]
            print(f"{movie} silindi.")
        else:
            print("Film bulunamadı.")


manager = MovieManager()
manager.addMovie(movie1)
manager.addMovie(movie2)


print(manager.movieDB)