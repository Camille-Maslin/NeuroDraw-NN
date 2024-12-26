"""
Drawing history management for undo/redo functionality.
"""

class DrawingHistory:
    def __init__(self):
        self.history = []  # Liste des états (chaque état est une liste de traits)
        self.current_index = -1
    
    def add_state(self, strokes):
        """Ajoute un nouvel état à l'historique"""
        # Supprimer tous les états après l'index actuel
        self.history = self.history[:self.current_index + 1]
        
        # Créer une copie profonde des traits
        new_state = []
        for stroke in strokes:
            new_state.append(stroke.copy())
        
        self.history.append(new_state)
        self.current_index += 1
    
    def undo(self):
        """Retourne à l'état précédent"""
        if self.can_undo():
            self.current_index -= 1
            if self.current_index >= 0:
                return self.history[self.current_index]
            return []
        return None
    
    def redo(self):
        """Rétablit l'état suivant"""
        if self.can_redo():
            self.current_index += 1
            return self.history[self.current_index]
        return None
    
    def can_undo(self):
        """Vérifie s'il est possible d'annuler"""
        return self.current_index >= 0
    
    def can_redo(self):
        """Vérifie s'il est possible de rétablir"""
        return self.current_index < len(self.history) - 1 