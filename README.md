# PJ's Plant Planner

An app to help keep track of what I've planted where and when.

# Saving and Loading

This is working now, but only limited to the plant widgets. I decided I didn't want to deal with
tracking everything other than plants, so I'm going to abandon the drawing component
and just add support for importing in images created elsewhere.

# Background Image

A background image can be optionally imported onto the map for you to overlay plants onto.
If an image isn't imported, it just uses a white background that will fill the screen. If
an image is imported, the canvas is sized to fit the image.

## What if the image is larger than the screen?

I should add in scroll bars for large background images to allow for more varied map sizes.

# Plant Icons

I've got a basic icon, but it's nothing special. This should really be something that
can be greyed out (or some other colour)  when no planted date is set. This will give a
handy visual clue for what plants are or aren't active.

# To Do

- (Sorta) Make some nicer icons for plants. I might turn this into a drop down of plant types to
choose when adding.
- Colour plant icons based on whether they are planted or not.
- Add some validation of the date so the planted time actually is a date.
- There's a bug where the save as dialog won't let you close it. Fix that.

# Time Worked

15 hrs

