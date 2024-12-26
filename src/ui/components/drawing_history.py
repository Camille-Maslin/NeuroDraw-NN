"""
Drawing history management for undo/redo functionality.
"""

class DrawingHistory:
    def __init__(self):
        self.history = []  # List of states (each state is a list of strokes)
        self.current_index = -1
    
    def add_state(self, strokes):
        """Adds a new state to the history"""
        # Remove all states after current index
        self.history = self.history[:self.current_index + 1]
        
        # Create a deep copy of strokes
        new_state = []
        for stroke in strokes:
            new_state.append(stroke.copy())
        
        self.history.append(new_state)
        self.current_index += 1
    
    def undo(self):
        """Returns to the previous state"""
        if self.can_undo():
            self.current_index -= 1
            if self.current_index >= 0:
                return self.history[self.current_index]
            return []
        return None
    
    def redo(self):
        """Restores the next state"""
        if self.can_redo():
            self.current_index += 1
            return self.history[self.current_index]
        return None
    
    def can_undo(self):
        """Checks if undo is possible"""
        return self.current_index >= 0
    
    def can_redo(self):
        """Checks if redo is possible"""
        return self.current_index < len(self.history) - 1 