from database.DAO import DAO
from copy import deepcopy

from model.powerOutages import Event


class Model:
    def __init__(self):
        self._best_subset = []
        self._max_involved = 0
        self._hours_of_disservice = 0
        self._max_h = None
        self._max_y = None
        self._listNerc = None
        self._listEvents = None
        self.loadNerc()



    def worstCase(self, nerc_id, max_y, max_h):
        self._best_subset = []
        self._max_involved = 0
        self._hours_of_disservice = 0
        self._max_h = max_h
        self._max_y = max_y
        self.loadEvents(nerc_id)
        self._ricorsione([], 0)
        return self._best_subset, self._max_involved, self._hours_of_disservice


    def _ricorsione(self, parziale: list[Event], level: int):
        hours_of_disservice = self._calculate_h(parziale)
        if hours_of_disservice > self._max_h:
            current_involved = self._calculate_involved(parziale[:-1])
            if current_involved > self._max_involved:
                self._best_subset = deepcopy(parziale[:-1])
                self._max_involved = current_involved
                self._hours_of_disservice = hours_of_disservice
        elif len(parziale) > 0 and parziale[-1] == self._listEvents[-1]:
            current_involved = self._calculate_involved(parziale)
            if current_involved > self._max_involved:
                self._best_subset = deepcopy(parziale)
                self._max_involved = current_involved
                self._hours_of_disservice = hours_of_disservice
        else:
            for e in self._listEvents[level:]:
                if e not in parziale and self._check_years_constraint(parziale, e):
                    parziale.append(e)
                    self._ricorsione(parziale, self._listEvents.index(e))
                    parziale.pop()


    def loadEvents(self, nerc_id):
        self._listEvents = DAO.getAllEvents(nerc_id)

    def loadNerc(self):
        self._listNerc = DAO.getAllNerc()

    @property
    def listNerc(self):
        return self._listNerc

    def _calculate_h(self, parziale: list[Event]):
        tot_h = 0
        for e in parziale:
            tot_h += e.hours_of_disservice
        return tot_h

    def _calculate_involved(self, parziale: list[Event]):
        tot_involved = 0
        for e in parziale:
            tot_involved += e.customers_affected
        return tot_involved

    def _check_years_constraint(self, parziale: list[Event], event: Event):
        for e in parziale:
            if e.date_event_began.year - event.date_event_began.year > self._max_y:
                return False
        return True