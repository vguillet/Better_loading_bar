Better_loading_bar

Better_loading_bar is a single script, multi-function and multi-option class meant to allow for easy setting up and tracking of task progress. ANSI colors are used to enhance readability, but require compatible install to be visible (progress bar will work regardless).

Integration is kept as simple as possible, while giving the user full access to a significant number of usefull information such as ETA, run time, completion, etc...

The progress bar also contains an activity indicator, which allows for easy determination of ongoing process during (useful for while loops).
The progress bar can be run on a single line or can update over new lines as process proceeds.

To use, simply initiate an instance of the loading bar, specify the wanted information, and run the .update_progress_bar (for loops) or .update_activity_indicator (while loops) whenever progress is made.
