# SC-localDB-workaround

Solution to add non-public database access to a ScreenCloud playground. Intended as a workaround for a server that disallows external connections.

When a user requests to create an order a command gets added to the cmds object in the data file on ScreenCloud. The main script will run on a set schedule checking to see if the cmds object is populated. The script will then run any command it finds against the local DB, do the specified task, then remove the command from the Json file and send a PUT to update the data back on ScreenCloud.

data.json (An example of the JSON preview in ScreenCloud):
  - dyn_list is here to generate page elements dynamically (not really important for the scope of this but needed in the full project)
  - store orders that get displayed on screen in orders (whoa)
  - cmds to hold unexecuted commands
