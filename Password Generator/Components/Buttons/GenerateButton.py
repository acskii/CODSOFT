from ttkbootstrap import Button
from Generation.Generator import *

# Button that invokes the generation method from Generation.Generator
class GenerateButton(Button):
    def __init__(self, master):
        self.generator = Generator()

        super().__init__(master,
                         text="Generate",
                         bootstyle='info-outline',
                         command=self.generate,
                         )
    # NOTE: TODO: Add a way to change button font

    def generate(self):
        # TODO: Trigger generator with new parameters
        return self.generator.generate()