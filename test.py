import tkinter as tk

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

        # Store unit operations
        self.units = []
        self.connections = []
        self.start_unit = None

    def add_bioreactor(self):
        x, y = 100, 100  # Default position for the bioreactor
        bioreactor = self.canvas.create_rectangle(x, y, x+100, y+60, fill="lightblue", tags="bioreactor")
        self.canvas.create_text(x+50, y+30, text="Bioreactor")
        self.units.append(bioreactor)

    def add_filter(self):
        x, y = 300, 300  # Default position for the filter
        filter_unit = self.canvas.create_rectangle(x, y, x+100, y+60, fill="lightgreen", tags="filter")
        self.canvas.create_text(x+50, y+30, text="Filter")
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

if __name__ == "__main__":
    root = tk.Tk()
    app = BioreactorDiagramApp(root)
    root.mainloop()
