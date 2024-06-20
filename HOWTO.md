# HOWTO complete the Appointments project

## Skeleton of appt.py

`Appt` objects will record the dates and times 
that appointments begin and end using a 
Python class called `datetime`

At the end of the file,  create the code to 
be run if this program is executed as the 
main Python program.

## Building the Appt class

```python
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
```

For appointments, we want `<` to mean “before” 
and `>` to mean “after”. One appointment is 
after another if it has ended when the other 
starts. For example, if I have a meeting from 
10am to 11am, and class beginning 11am, then 
my meeting is before my class. But if my meeting
is from 10am to 11:30am, and class starts at 
11am, then my meeting is not _before_ my class 
even though it starts earlier. If two appointments 
overlap, we will say that neither one is before 
(<) the other.

### Checking for overlapping appointments

Our ultimate goal is to check for conflicting 
appointments. For example, if we have scheduled 
a lunch meeting from noon to 1:30pm, and scheduled 
another meeting from 1pm to 2pm, then there is a 
conflict in our schedule because those appointments
 overlap in time. 

```python
    def overlaps(self, other: 'Appt') -> bool:
        """Is there a non-zero overlap between these periods?"""
```

```python
    def intersect(self, other: 'Appt') -> 'Appt':
        """The overlapping portion of two Appt objects"""
        assert self.overlaps(other)  # Precondition
```

The result of method `intersect` should be a new `Appt` object. 
The usage example in the docstring for class 
`Appt` illustrates how the description of the new 
appointment should be formed from the descriptions 
of the two overlapping appointments.

### Formatting appointments

If we print an appointment, 
it doesn't look very nice:

```
>>> from appt import Appt
>>> from datetime import datetime
>>> ap = Appt(datetime(2018, 3, 15, 15, 00), datetime(2018, 3, 15, 16, 00), "Coffee break")
>>>print(ap)
<appt.Appt object at 0x10cc1e4e0>
``` 

This default formatting does not cause any of 
our test cases to fail yet, but it will cause 
problems later when we are reading and writing 
agenda files, and it is clearly not very useful.
A user of our scheduling software is more likely
to care that coffee break begins at 3:00pm than 
that it is stored in an object at memory 
address 0x10cc1e4e0.

## The Agenda class

An `Agenda` is a collection of `Appt` objects.   

```python
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
```

### Delegation: `append`, `len` (`__len__`), and `==` (`__eq__`)

```python
    def __eq__(self, other: 'Agenda') -> bool:
        """Delegate to __eq__ (==) of wrapped lists"""
        return self.elements == other.elements
```

### Formatting an `Agenda`: `str` and `repr` (`__str__` and `__repr__`)

We will need a method to format an `Agenda` object, 
preferably the same as we expect to find input
files.  

```python
    def __str__(self):
        """Each Appt on its own line"""
```

Since the constructor of class `Agenda` only 
creates an empty `Agenda` object, a good 
debugging representation will not look like a 
correct call to the constructor.  It's more 
important to make it useful. 

```python
    def __repr__(self) -> str:
        """The constructor does not actually work this way"""
```

The other important method we need is one 
to produce a list of conflicts. If 
If the list of conflicts is wrapped in another 
`Agenda` object, then the `len` method of `Agenda`
suffices for distinguishing whether or not an 
agenda is free of conflict. 

```python
 def conflicts(self) -> 'Agenda':
        """Returns an agenda consisting of the conflicts
        (overlaps) between appointments in this agenda.
        """
```

*Algorithm must run in time O(n lg n) 
 where n is max(number of appointments, number 
 of conflicts).*

We can make the conflict-finding method much more efficient if we start by putting the Appt objects in order by start time. But this will be a _side effect_ of the conflicts method, so we'd better note that in the docstring:

```python
def conflicts(self) -> 'Agenda':
        """Returns an agenda consisting of the conflicts
        (overlaps) between this agenda and the other.
        Side effect: This agenda is sorted
        """
```

Sorting an `Agenda` just requires sorting the list 
of `Appt` objects in the `Agenda`.  Instead of sorting 
by the order of `Appt` objects (which is undefined 
for overlapping appointments), we will sort by their
start time.  The `sort` method of class `list` 
has an optional argument that lets us extract a 
*sort key* from an element.  We want to extract 
the start time. 

## Aside: Tidying up with *lambda* 

```python
    def sort(self):
        """Sort agenda by appointment start times"""
```
## Finding conflicts 

Search for conflicts with nested loops, cutting the inner loop short with a break statement. The outer _for_ loop iterates through all the appointments in the Agenda list. The inner _for_ loop starts at the item just after the current appointment. It could continue to the end of the sequence, if all the appointments overlapped, but it can be cut off as soon as we encounter an appointment that starts after the appointment selected by the outer loop.

```python
  def test_1_fast(self):
        """A linear time algorithm should be able to test
        an agenda with 5000 elements in well under a second,
        even on a fairly slow computer.
        """ 
```
