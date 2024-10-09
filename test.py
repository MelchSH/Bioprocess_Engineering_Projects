import tkinter as tk
#from bioreactor_model import Bioreactor  # Import your bioreactor model

class BioreactorDiagramApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bioreactor and Filter Diagram")

        # Canvas for drawing the diagram
        self.canvas = tk.Canvas(root, width=800, height=600, bg='white')
        self.canvas.pack()

        # Buttons to add bioreactor and filter
        self.add_bioreactor_button = tk.Button(root, text="Add Bioreactor", command=self.add_bioreactor)
        self.add_bioreactor_button.pack(side=tk.LEFT)

        self.add_filter_button = tk.Button(root, text="Add Filter", command=self.add_filter)
        self.add_filter_button.pack(side=tk.LEFT)

        self.add_connection_button = tk.Button(root, text="Connect", command=self.add_connection)
        self.add_connection_button.pack(side=tk.LEFT)

        # Store unit operations and positions
        self.units = []
        self.connections = []
        self.current_unit = None
        self.offset_x = 0
        self.offset_y = 0

        # Bioreactor model instance
        #self.bioreactor_model = Bioreactor()

    def add_bioreactor(self):
        x, y = 100, 100  # Default position for the bioreactor
        bioreactor = self.canvas.create_rectangle(x, y, x+100, y+60, fill="lightblue", tags="bioreactor")
        self.canvas.create_text(x+50, y+30, text="Bioreactor")
        self.canvas.tag_bind(bioreactor, "<Button-1>", self.on_click)
        self.canvas.tag_bind(bioreactor, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(bioreactor, "<ButtonRelease-1>", self.on_release)
        self.units.append(bioreactor)

    def add_filter(self):
        x, y = 300, 300  # Default position for the filter
        filter_unit = self.canvas.create_rectangle(x, y, x+100, y+60, fill="lightgreen", tags="filter")
        self.canvas.create_text(x+50, y+30, text="Filter")
        self.canvas.tag_bind(filter_unit, "<Button-1>", self.on_click)
        self.canvas.tag_bind(filter_unit, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(filter_unit, "<ButtonRelease-1>", self.on_release)
        self.units.append(filter_unit)

    def add_connection(self):
        if len(self.units) >= 2:
            bioreactor = self.units[0]  # Assuming first unit is the bioreactor
            filter_unit = self.units[1]  # Assuming second unit is the filter
            bx1, by1, bx2, by2 = self.canvas.coords(bioreactor)
            fx1, fy1, fx2, fy2 = self.canvas.coords(filter_unit)

            # Draw a line between the center of the bioreactor and filter
            self.canvas.create_line(bx2, (by1+by2)/2, fx1, (fy1+fy2)/2, arrow=tk.LAST, width=2)
            self.connections.append((bioreactor, filter_unit))

    def on_click(self, event):
        # Get the clicked rectangle (unit)
        self.current_unit = self.canvas.find_withtag("current")[0]
        # Save the offset of the click inside the rectangle
        self.offset_x = event.x - self.canvas.coords(self.current_unit)[0]
        self.offset_y = event.y - self.canvas.coords(self.current_unit)[1]

    def on_drag(self, event):
        # Get current coordinates of the unit
        x1, y1, x2, y2 = self.canvas.coords(self.current_unit)
        # Move the rectangle to the new mouse position
        self.canvas.move(self.current_unit, event.x - x1 - self.offset_x, event.y - y1 - self.offset_y)
        # Move the text as well (the text will always have the same tag index as the unit)
        self.canvas.move(self.current_unit + 1, event.x - x1 - self.offset_x, event.y - y1 - self.offset_y)

    def on_release(self, event):
        self.current_unit = None

if __name__ == "__main__":
    root = tk.Tk()
    app = BioreactorDiagramApp(root)
    root.mainloop()
