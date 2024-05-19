class Node:
    def __init__(self, start_x, start_y, end_x, end_y):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y

    def __str__(self):
        return (
            f"Node: start_x={self.start_x}, "
            f"start_y={self.start_y}, "
            f"end_x={self.end_x}, "
            f"end_y={self.end_y}]"
        )

    def __repr__(self):
        return (
            f"Node: start_x={self.start_x}, "
            f"start_y={self.start_y}, "
            f"end_x={self.end_x}, "
            f"end_y={self.end_y}"
        )
