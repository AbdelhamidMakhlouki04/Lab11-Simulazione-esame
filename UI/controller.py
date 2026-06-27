import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDGenre(self):
        generi=self._model.get_all_genre()
        self._view.set_ddGenre(generi)

    def handleCreaGrafo(self, e):
        genere=self._view._ddGenre.value
        self._model.get_vertici(genere)
        self._model.get_archi(genere)

        self._model.crea_grafo()
        vertici,archi=self._model.get_num_grafo()
        print(vertici,archi)

    def handleCammino(self,e):
        pass