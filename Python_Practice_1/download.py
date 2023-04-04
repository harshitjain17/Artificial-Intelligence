class _StackNode :
	def __init__( self, item, link ) :
		self.item = item
		self.next = link

class Stack:
    def __init__( self ):
        self._top = None
        self._size = 0
       
    def peek( self ):
        assert not self.is_empty(), "Cannot peek at an empty stack"
        return (self._top.item)
    
    def push ( self, item ):
        '''Method to push an item to the top of a Stack
        '''
        if self._top is None:
            self._top = _StackNode( item, None )
        else:
            new_stack_node = _StackNode( item, self._top )
            self._top = new_stack_node
    
    def pop(self):
        '''Method to pop an item from the top of a Stack
        '''
        if self._top is None:
            return None
        else:
            pop_value = self._top.item
            self._top = self._top.next
            return pop_value
    
    def is_empty(self):
        ''' Used to tell us whether the Stack is empty (returns a True or False)
        '''
        return self._top is None