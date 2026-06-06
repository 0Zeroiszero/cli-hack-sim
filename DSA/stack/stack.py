class Stack:
    '''
    Stack ini digunakan untuk menyimpan log histori.
    Digunakan karena stack memiliki sifat LIFO (Last In First Out),
    sehingga log terbaru akan selalu berada di atas dan mudah diakses.
    '''
    def __init__(self) -> None:
        self.stack: list = []

    def push(self, item) -> None:
        self.stack.append(item)

    def pop(self) -> object:
        if not self.is_empty():
            return self.stack.pop()
        else:
            raise IndexError("Stack is empty")

    def peek(self) -> object:
        if not self.is_empty():
            return self.stack[-1]
        else:
            raise IndexError("Stack is empty")

    def is_empty(self) -> bool:
        return len(self.stack) == 0

    def size(self) -> int:
        return len(self.stack)
    
    def show_logs(self):
        print("\n=== HISTORI LOG (TERBARU -> LAMA) ===")
        for item in reversed(self.stack):
            print(item)