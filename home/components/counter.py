from django_unicorn.components import UnicornView

class CounterView(UnicornView):
    count = 0

    def increment(self):
        self.count += 1
        

    def decrement(self):
        self.count -= 1

    # def mount(self):
    #     kwarg = self.component_kwargs["contatore"]
    #     print(kwarg)