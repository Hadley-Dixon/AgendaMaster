# Project Description

## What it does 

An agenda is a list of appointments.  Appointments are represented 
internally as Appt objects, and externally  (when we read them from a 
file or print them) as text.  The textual format of an appointment 
looks like this: 

```
# Winter 2019 schedule for CIS 211
2019-01-08 10:00 11:20 | CIS 211 lecture 1
2019-01-10 10:00 11:20 | CIS 211 lecture 2
```

The line beginning with # is a comment.  Each of the other 
two lines specifies the content of an individual 
Appt object.  

The main feature of this project when it is complete 
will be determining whether or not any of the Appt objects 
in an Agenda conflict, i.e., whether they overlap in 
time.  For example, it might not be easy to see whether 
the following list of class sessions contains any conflicts: 

```
 # Winter 2019 schedule for CIS 211
2019-01-08 10:00 11:20 | CIS 211 lecture 1
2019-01-10 10:00 11:20 | CIS 211 lecture 2
2019-01-15 10:00 11:20 | CIS 211 lecture 3
2019-01-17 10:00 11:20 | CIS 211 lecture 4
2019-01-22 10:00 11:20 | CIS 211 lecture 5
2019-01-24 10:00 11:20 | CIS 211 lecture 6
2019-01-29 10:00 11:20 | CIS 211 lecture 7
2019-01-31 10:00 11:20 | CIS 211 lecture 8
2019-02-05 10:00 11:20 | CIS 211 lecture 9
2019-02-07 10:00 11:20 | CIS 211 lecture 10
2019-02-12 10:00 11:20 | CIS 211 lecture 11
2019-02-14 10:00 11:20 | CIS 211 lecture 12
2019-02-19 10:00 11:20 | CIS 211 lecture 13
2019-02-21 10:00 11:20 | CIS 211 lecture 14
2019-02-26 10:00 11:20 | CIS 211 lecture 15
2019-02-28 10:00 11:20 | CIS 211 lecture 16
2019-03-05 10:00 11:20 | CIS 211 lecture 17
2019-03-07 10:00 11:20 | CIS 211 lecture 18
2019-03-12 10:00 11:20 | CIS 211 lecture 19
2019-03-14 10:00 11:20 | CIS 211 lecture 20
2019-02-07 10:00 11:20 | CIS 211 midterm
```

Can you see the conflict?  Your program will be able
to check it and produce output like this: 

```
Agenda checked, 21 appointments
Conflict: 2019-02-07 10:00 11:20 |  CIS 211 lecture 10 and  CIS 211 midterm
```

Oops, the midterm is scheduled during lecture, 
so I had better not plan a lecture for that day! 
