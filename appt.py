"""Python source file provides classes Appt and Agenda
Hadley Dixon, 2022-04-04, CIS 211
Credit: Collaborated with Kora Dumpert
"""

from datetime import datetime

class Appt:
    """An appointment has a start time, an end time, and a title.
    The start and end time should be on the same day.
    Usage example:
        appt1 = Appt(datetime(2018, 3, 15, 13, 30), datetime(2018, 3, 15, 15, 30), "Early afternoon nap")
        appt2 = Appt(datetime(2018, 3, 15, 15, 00), datetime(2018, 3, 15, 16, 00), "Coffee break")
        if appt2 > appt1:
            print(f"appt1 '{appt1}' was over when appt2 '{appt2}'  started")
        elif appt1.overlaps(appt2):
            print("Oh no, a conflict in the schedule!")
            print(appt1.intersect(appt2))
    Should print:
        Oh no, a conflict in the schedule!
        2018-03-15 15:00 15:30 | Early afternoon nap and Coffee break
    """
    def __init__(self, start: datetime, finish: datetime, desc: str):
        """An appointment from start time to finish time, with description desc.
        Start and finish should be the same day.
        """
        assert finish > start, f"Period finish ({finish}) must be after start ({start})"
        self.start = start
        self.finish = finish
        self.desc = desc


    def __eq__(self, other: 'Appt') -> bool:
        """Equality means same time period, ignoring description"""
        return self.start == other.start and self.finish == other.finish


    def __lt__(self, other: 'Appt') -> bool:
        """Appointment a is before appointment b iff the finish time of a
        is equal or earlier than the start time of b"""
        return self.finish <= other.start


    def __gt__(self, other: 'Appt') -> bool:
        """Appointment a is after appointment b iff the start time of a
        is equal or after the finish time of b"""
        return self.start >= other.finish


    def overlaps(self, other: 'Appt') -> bool:
        """Is there a non-zero overlap between these periods?"""
        if not self.__lt__(other) and not other.__lt__(self):
            return True


    def intersect(self, other: 'Appt') -> 'Appt':
        """The overlapping portion of two Appt objects"""
        assert self.overlaps(other)  # Precondition
        return Appt(max(self.start, other.start), min(self.finish, other.finish), f"{self.desc} and {other.desc}")


    def __str__(self) -> str:
        """The textual format of an appointment is
        yyyy-mm-dd hh:mm hh:mm  | description
        Note that this is accurate only if start and finish
        are on the same day.
        """
        date_iso = self.start.date().isoformat()
        start_iso = self.start.time().isoformat(timespec='minutes')
        finish_iso = self.finish.time().isoformat(timespec='minutes')
        return f"{date_iso} {start_iso} {finish_iso} | {self.desc}"


    def __repr__(self) -> str:
        """Controls string formatting"""
        return f"Appt({repr(self.start)}, {repr(self.finish)}, {repr(self.desc)})"


    def start_time(appt: 'Appt') -> datetime:
        """Extracts the start time from Appt object"""
        return appt.start


class Agenda:
    """An Agenda is a collection of appointments,
    similar to a list.

    Usage:
    appt1 = Appt(datetime(2018, 3, 15, 13, 30), datetime(2018, 3, 15, 15, 30), "Early afternoon nap")
    appt2 = Appt(datetime(2018, 3, 15, 15, 00), datetime(2018, 3, 15, 16, 00), "Coffee break")
    agenda = Agenda()
    agenda.append(appt1)
    agenda.append(appt2)
    ag_conflicts = agenda.conflicts()
    if len(ag_conflicts) == 0:
        print(f"Agenda has no conflicts")
    else:
        print(f"In agenda:\n{agenda.text()}")
        print(f"Conflicts:\n {ag_conflicts}")

    Expected output:
    In agenda:
    2018-03-15 13:30 15:30 | Early afternoon nap
    2018-03-15 15:00 16:00 | Coffee break
    Conflicts:
    2018-03-15 15:00 15:30 | Early afternoon nap and Coffee break
    """
    def __init__(self):
        """Constructor initializes en empty collection"""
        self.elements = []


    def __eq__(self, other: 'Agenda') -> bool:
        """Delegate to __eq__ (==) of wrapped lists"""
        return self.elements == other.elements


    def __len__(self):
        """Delegates the len method of lists to Agenda"""
        return len(self.elements)


    def append(self, other: 'Agenda'):
        """Delegates the append method of lists to Agenda"""
        return self.elements.append(other)


    def __str__(self):
        """Each Appt on its own line"""
        lines = [str(e) for e in self.elements]
        return "\n".join(lines)


    def __repr__(self) -> str:
        """The constructor does not actually work this way"""
        return f"Agenda({self.elements})"


    def sort(self):
        """Sort agenda by appointment start times"""
        self.elements.sort(key=lambda appt: appt.start)


    def conflicts(self) -> 'Agenda':
        """Returns an agenda consisting of the conflicts
        (overlaps) between appointments in this agenda.
        """
        self.sort()
        agenda = Agenda()
        for i in range(len(self.elements)):
            for j in range(i + 1, len(self.elements)):
                if self.elements[i].overlaps(self.elements[j]):
                    conflict = self.elements[i].intersect(self.elements[j])
                    agenda.append(conflict)
                else:
                    break
        return agenda


if __name__ == "__main__":
    print("Running usage examples")
    appt1 = Appt(datetime(2018, 3, 15, 13, 30), datetime(2018, 3, 15, 15, 30), "Early afternoon nap")
    appt2 = Appt(datetime(2018, 3, 15, 15, 00), datetime(2018, 3, 15, 16, 00), "Coffee break")
    if appt2 > appt1:
        print(f"appt1 '{appt1}' was over when appt2 '{appt2}'  started")
    elif appt1.overlaps(appt2):
        print("Oh no, a conflict in the schedule!")
        print(appt1.intersect(appt2))
    agenda = Agenda()
    agenda.append(appt1)
    agenda.append(appt2)
    ag_conflicts = agenda.conflicts()
    if len(ag_conflicts) == 0:
        print(f"Agenda has no conflicts")
    else:
        print(f"In agenda:\n{agenda}")
        print(f"Conflicts:\n {ag_conflicts}")