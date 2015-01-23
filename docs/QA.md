
# QA

### Notes

* Current enrollment term is "Spring 2014-2015"
* Initial course data load can take quite a while and possibly even timeout, esp if selecting "All Courses" from the Term dropdown. 

### User Story Checklist

User stories assume a logged-in Canvas user with Account admin privileges.

As a user...

* I should see a 'DCE Course Admin' link in the left-hand navbar.
* I should be able to click the 'DCE Course Admin' link to launch the tool.
* After launching the tool, but before course data has finished loading, I should see an empty table and a "spinner" graphic indicating that the course data is loading.
* I should see the table populated with rows corresponding to each course after the course data has loaded.
* I should be able to view courses for a particular term by changing the term selection dropdown above the table to the right. By default the current term should be selected. Selecting "All" should display courses from all available terms.
* I should see a notice at the top of the table indicating the range of courses being viewed and the total number of courses.
* I should see five columns in the table: Course, Public Syllabus, Default View, Published? and Public?
* I should be able to filter the rows of the table using the input controls at the top of each column.
* I should be able to undo any filtering by resetting the filtering controls to "All" in the case of dropdowns, and clearing the text input field in the case of the course name.
* I should be able to sort the rows of the table by clicking an up-down arrow icon positioned on the right side of the column header. By default the table should be sorted by course name, ascending.
* I should be able to adjust the number of table rows displayed using a dropdown menu below the table to the left.
* I should be able to paginate through the table rows using "Previous", "Next" and numbered page links grouped below the table to the right.
* I should be able to view the home page of a course by clicking the home icon to the left of the course name.
* I should be able to view the syllabus of a course, when available, by clicking the syllabus icon in the Public Syllabus column.
* I should be able to update a course's "Is Public?" and "Is Published?" status by clicking the Y|N toggle switches in the respective columns.
* When I update a course's status the value of the toggle switch should reflect the change.
* When I update a course's status I should see a pop-up notification that the change was successful. The pop-up should disappear after 3 seconds or after I click the pop-up's close icon.


