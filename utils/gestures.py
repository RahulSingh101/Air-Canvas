class GestureDetector:

    def __init__(self):
        pass

    def is_draw_mode(self):
        # Index up, middle down
        return True  # simplified for stability

    def is_erase_mode(self):
        # Index & middle raised
        return False

    def is_zoom_in(self):
        return False

    def is_zoom_out(self):
        return False

    def is_undo(self):
        return False
