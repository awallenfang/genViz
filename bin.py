class Bin():
    def __init__(self, val = -90, attack = 0.5, release = 0.9):
        self.val = val
        self.attack = attack
        self.release = release

    def smooth_val(self):
        return self.val
    
    def linear_val(self):
        return (90. + self.smooth_val()) / 90
    
    def update(self, new_val):
        # direction_strength = self.release if self.val > new_val else self.attack
        # self.val = (self.val * direction_strength) + (new_val * (1 - direction_strength))
        self.val = new_val

    def __str__(self):
        return f'Bin({self.val})'
    def __repr__(self):
        return f'Bin({self.val})'
