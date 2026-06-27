from dataclasses import dataclass


@dataclass
class Genre:
    genre_id: int
    genre_name: str

@dataclass
class Vertici:
    artist_id: int
    artist_name: str

@dataclass
class Archi:
    artist_id1 : int
    artist_id2 : int

@dataclass
class Peso:
    artist_id : int
    quantity : int