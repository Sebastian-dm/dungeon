import svgwrite

from dungeon import Dungeon

# Setup Parameters
paper_dimensions = {"A4p":( 595,  842),
                    "A4l":( 842,  595),
                    "A3p":( 842, 1191),
                    "A3l":(1191,  842)}
width, height = paper_dimensions["A3l"]
square = 14.2
background_color = svgwrite.rgb(9, 46, 61, '%')
corridor_color = svgwrite.rgb(100, 100, 100, '%')

# Make Dungeons
dungeon = Dungeon(width=int(width/square), height=int(height/square))
dungeon.build_dungeon(max_iterations=400)

# Setup Drawing
print("Setting up drawing")
dwg = svgwrite.Drawing('output/dungeon_test.svg',
                    size=(width, height),
                    viewBox=(0,0,width, height),
                    profile='tiny')

# Draw Background
background = dwg.rect((0, 0), (width, height))
background.fill(color=background_color)
dwg.add(background)

# Draw Origin
origin = dwg.circle(center=dungeon.origin*square, r=square)
origin.fill(color="red")
dwg.add(origin)

# Draw Corridors
print("Drawing corridors")
for corridor in dungeon.corridors:
    corridor_line = dwg.line(start=corridor.start*square, end=corridor.end*square)
    corridor_line.stroke(color=corridor_color,
                            width=square,
                            linecap="round")
    dwg.add(corridor_line)

# Draw tricks and traps
print("Placing Tricks and traps")
for point in dungeon.tricks+dungeon.traps:
    text = dwg.text("T", insert=point*square+[-square/2, square/2])
    dwg.add(text)

# Draw tricks and traps
print("Placing Monsters")
for point in dungeon.monsters:
    text = dwg.text("M", insert=point*square+[-square/2, square/2])
    dwg.add(text)

# Save Drawing
dwg.save()