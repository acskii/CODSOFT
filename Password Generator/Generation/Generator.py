import random
import string

# The Core of this task. -> password generator
class Generator:
    STRENGTH = ['simple', 'normal', 'impossible', 'PIN']
    LOWERCASE = list(string.ascii_lowercase)
    UPPERCASE = list(string.ascii_uppercase)
    SPECIAL = list(string.punctuation)
    DIGITS = list(string.digits)

    def __init__(self, length=8, strength='normal'):
        self.strength = strength if self.authunticate_strength(strength) else 'normal'
        if self.strength == 'PIN':
            self.length = length if 4 <= length <= 8 else 4
        else:
            self.length = length if 8 <= length <= 100 else 8 
            
        self.special = False
        self.digits = True
        self.upperCase = False
        self.lowerCase = True
        self.restrictedSpecial = None
        self.tweak_strength(self.strength)

    def tweak_strength(self, strength):
        if strength == self.STRENGTH[0]:
            self.special = False
            self.digits = True
            self.upperCase = False
            self.lowerCase = True
            self.restrictedSpecial = None

        elif strength == self.STRENGTH[1]:
            self.special = False
            self.digits = True
            self.upperCase = True
            self.lowerCase = True
            self.restrictedSpecial = ['?', '$', '%', '#', '@', '&']

        elif strength == self.STRENGTH[2]:
            self.special = True
            self.digits = True
            self.upperCase = True
            self.lowerCase = True
            self.restrictedSpecial = None
            
        elif strength == self.STRENGTH[3]:
            self.special = False
            self.digits = True
            self.upperCase = False
            self.lowerCase = False
            self.restrictedSpecial = None

    def edit_params(self, length, strength):
        self.strength = strength if self.authunticate_strength(strength) else 'normal' 
        if self.strength == 'PIN':
            self.length = length if 4 <= length <= 8 else 4
        else:
            self.length = length if 8 <= length <= 100 else 8
            
        self.tweak_strength(self.strength)

    def generate(self):
        # Actual password generation here
        # A 'simple' password is consistent of lower-case letters and digits ONLY
        # A 'normal' password is consistent of lower-case letters, upper-case letters, digits and some special
        # A 'impossible' password is consistent of everything collected in class ( will filter some specials )
        characterPool = []
        
        if self.lowerCase: 
            characterPool.extend(self.LOWERCASE)
        if self.upperCase:
            characterPool.extend(self.UPPERCASE)
        if self.digits:
            characterPool.extend(self.DIGITS)     
        if self.special:
            characterPool.extend(self.SPECIAL)
        if self.restrictedSpecial != None:
            characterPool.extend(self.restrictedSpecial)
        
        generated = []
        for _ in range(self.length):
            #TODO: Experiment with random.choices for weights
            generated.append(random.choice(characterPool))
                
        return ''.join(generated)

    @classmethod
    def authunticate_strength(cls, strength):
        return strength in cls.STRENGTH
    
#g = Generator(4, strength='simple')
#print(g.generate())