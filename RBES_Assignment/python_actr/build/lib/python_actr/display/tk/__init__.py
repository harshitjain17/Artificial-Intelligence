from python_actr.lib import grid
from .cellular import CellularRenderer
from .default import DefaultRenderer

def render(obj,canvas):
    if not hasattr(obj,'_display'):
        if isinstance(obj,grid.World):
            obj._display=CellularRenderer(obj,canvas)
        else:
            obj._display=DefaultRenderer(obj,canvas)    
    obj._display.render(canvas)
    for c in obj.get_children():
        render(c,canvas)
        
