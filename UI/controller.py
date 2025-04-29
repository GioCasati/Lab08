import flet as ft

from model.nerc import Nerc


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._idMap = {}
        self.fillIDMap()

    def handleWorstCase(self, e):
        try:
            nerc_id = self._view._ddNerc.value
            max_y = int(self._view._txtYears.value)
            max_h = float(self._view._txtHours.value)
            if not nerc_id or not max_y or not max_h:
                self._view.create_alert("Select a nerc and fill all fields")
            else:
                sequence, num_involved, hours_of_disservice = self._model.worstCase(nerc_id, max_y, max_h)
                self._view._txtOut.controls.append(ft.Text(f"Number of people affected: {num_involved}"))
                self._view._txtOut.controls.append(ft.Text(f"Total of hours of disservice: {hours_of_disservice}"))
                for e in sequence:
                    self._view._txtOut.controls.append(ft.Text(e))
                self._view._txtOut.controls.append(ft.Text(""))
            self._view.update_page()
        except ValueError as ve:
            self._view.create_alert("Type an integer for the number of years and a decimal for the number of hours")


    def fillDD(self):
        nercList = self._model.listNerc
        for n in nercList:
            self._view._ddNerc.options.append(ft.dropdown.Option(key=n.id, text=n.value, data=n))
        self._view.update_page()

    def fillIDMap(self):
        values = self._model.listNerc
        for v in values:
            self._idMap[v.value] = v
