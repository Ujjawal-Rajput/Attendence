# Smart Attendance

Smart Attendance is an innovative solution designed to streamline the attendance process for educational institutions. Using this system, students can mark their attendance upon entering the classroom, simplifying record-keeping and minimizing disruptions.

## Benefits

- **Efficiency:** Automated attendance saves time for both students and teachers.
- **Accuracy:** Reduces human error in attendance tracking.
- **Real-Time Data:** Immediate updates on attendance status.
- **Eco-Friendly:** Eliminates the need for paper-based tracking.
- **Data Analysis:** Facilitates analysis of attendance patterns over time.
- **Integration:** Can be integrated with existing educational management systems.

## Features to be Implemented

1. **Face Recognition:** To allow automatic attendance marking when a student enters the classroom.
2. **Geo-Location Tagging:** Ensures that attendance is marked only when the student is in the classroom.
3. **Integration with Institutional Calendars:** Automatically marks students as absent if the class schedule indicates a holiday.
4. **Notification System:** Alerts students and faculty about attendance status.
5. **Reporting Dashboard:** Provides detailed reports on individual and class attendance.
6. **Mobile Application:** Enables students to mark attendance through their smartphones.
7. **Guest Student Feature:** Allows temporary attendance marking for non-regular students or guests.
8. **Backup and Recovery:** Ensures attendance data is never lost with robust backup solutions.
9. **Customizable Interface:** The ability to customize the interface to match institutional branding.

## Structure

```
|-- README.md
|-- requirements.txt ................. 1.
|-- run.py ........................... 2.
|-- attend ........................... 3.
|-- instance ......................... 4.
`-- attendenceSystem
    `-- ROOT ......................... 5.
        |-- static
        |   `-- img .................. 6.
        |   `-- css .................. 7.
                |-- index.css
        |   `-- js ................... 8.
        `-- templates ................ 9.
            |-- about.html
            |-- account.html
            |-- coordinatorPage.html
            |-- layout.html
            |-- login.html
            |-- register.html
            |-- studentPage.html
        `-- __init__.py
        `-- forms.py
        `-- models.py
        `-- routes.py
```

## Installation

*Python should be installed in the computer.*

```
$ pip install -r requirements.txt
$ python run.py
```

The result will be available at http://localhost:5000.

## Contact

*Try emailing for connecting us... (email can be found on this account info.)*

---

We are excited to see how Smart Attendance will transform the educational experience and look forward to your feedback and contributions!

