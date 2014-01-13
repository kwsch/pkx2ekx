# ceol's RNG standalone used for crypt

__author__ = "Patrick Jacobs <ceolwulf@gmail.com>"

class Rng(object):
    """Base class for the linear congruent random number generator.
    
    I may refer to this class as the RNG, the LC RNG, or the LCRNG
    throughout documentation. All of these mean the same thing: this
    pseudo-random number generator.
    """
    
    # Store every iteration of the LC RNG.
    frames = []
    
    seed = 0
    
    # Variables for the LC RNG. They may change depending on what child
    # RNG class is being used.
    mult = 0
    add = 0
    mask = 0xFFFFFFFF
    width = 0x10
    
    def __init__(self):
        pass
    
    def _advance(self):
        "Calculate the next LC RNG step."
        
        self.seed *= self.mult
        #self.seed &= self.mask
        self.seed += self.add
        self.seed &= self.mask
        
        return self.seed >> self.width
    
    def advance(self, steps=1):
        "Advance the LC RNG the specified number of steps."
        
        for i in range(0, steps):
            self.frames.append(self._advance())
        
        return self.frames[-1]
    
    def _reverse(self):
        "Calculate the previous LC RNG step."
        pass
    
    def reverse(self, steps):
        "Reverse the LC RNG the specified number of steps."
        pass

class Prng(Rng):
    
    def __init__(self, seed=0):
        super(Prng, self).__init__()

        self.seed = seed
        self.mult = 0x41C64E6D
        self.add = 0x6073