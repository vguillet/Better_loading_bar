#Better_loading_bar


"Add a full featured loading bar to any loop type and process in just two lines!"


Better_loading_bar is a single script, multi-function and multi-option class meant to allow for easy setting up and tracking of tasks progress. ANSI colours are used to enhance readability, but require compatible install to be visible (progress bar will work regardless).

Integration is kept as simple as possible, while giving the user full access to a significant number of usefull information such as ETA, run time, completion, etc...

The progress bar also contains an activity indicator, which allows for easy determination of ongoing processes existance (useful for while loops).

The progress bar can be run on a single line in the or can update over new lines as process proceeds.

####Progress bar:

Progress bars are used to keep track of pre-defined length processes. To create a progress bar, simply initiate an instance of the progress bar (specify the wanted information there, max_step must be specified).

```python
bar =  Progress_bar(max_step=30)
```

Run` .update_progress` to update progress (for loops) or `.update_activity` to keep the activity animations going between main progress updates (when minor progress is made).

####Activity bar

Activity bars are used to keep track of unknown-length processes (while loops).
To create an activity bar, simply initiate an instance of the progress bar (specify the wanted information there, keep max_step to None):

```python
bar =  Progress_bar(max_step=None)
```

Run `.update_activity` at the end of every iteration to update activity.

***NEW FEATURES:*** Added coloured and ***rainbow bar***
