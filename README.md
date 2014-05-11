# Bulk importing existing data into OSM using iD web editor

Idea:

We want to bulk import already existing data into OSM in a controlled environment using micro-tasking tools like tasking manager
Bulk imports would be broken up into individual tasks based on node count, limiting the amount of vector data loaded into iD. This would be a work around of current browser limitations handling large vector data.
During the import we want to validate the added data to make sure assigned attributes and geometries are correct, we don’t copy redundant data into OSM and OSM topology is correct (roads are actually intersecting, no over- or undershoots etc).

Workflow:

Core functions:
1.	We upload our existing data (eg as shapefile) onto a server. 
2.	During the upload we can assign attribute fields to OSM tag fields to keep already existing attribute values
3.	On the server new features are split at grid lines. 
4.	Number of features/ feature vertexes per grid cell is counted. If number is above a defined threshold features are split again on sub-grid lines until threshold is met.
5.	Grid cells are displayed in Task Manager
6.	User can pick grid cell to work on.
7.	When clicking on that cell iD editor opens and loads OSM data and new data in two editable layers.
8.	User can now validate the new data, delete redundant data and validate attributes
9.	User can also make sure that existing data have nodes where old and new data intersect to ensure that road network is consistent.
10.	When data are saved, both layers are merged and saved into the OSM database.

Nice to have functions:
1.	On the server every feature gets a unique id (uuid) assigned.
2.	Split features keep their uuid.
3.	If a new grid cell is opened OSM database is checked for already posted features with the same uuid. 
4.	If such feature exists attributes of that features are adopted for the new feature and feature marked as validated. User should also have the option to merge features with same uuid (eg adding features to a relationship). 

