from random import randrange
from sys import maxsize


class AverageCase():
    def __init__(self, number_of_integers, bound, number_of_sequences):
        self.number_of_integers = number_of_integers
        self.bound = bound
        self.number_of_sequences = number_of_sequences
        self.hits = 0
        self.steps = 0
        self.sequence_list = []
        self.x = randrange(self.bound)

    def generate_sequences(self):
        for sequence_number in range(self.number_of_sequences):
            sequence = []
            for integer_number in range(self.number_of_integers):
                sequence.append(randrange(self.bound))
            self.sequence_list.append(sequence)

    def find_hits_and_steps(self):
        for sequence in self.sequence_list:
            try:
                index_number = sequence.index(self.x)
                self.hits += 1
                self.steps += index_number + 1
            except ValueError:
                self.steps += self.number_of_integers

    def display_results(self):
        print("%d  %f  %f" % (self.bound, self.hits*self.bound/self.number_of_sequences, self.steps/self.number_of_sequences))

    @classmethod
    def run_all_steps(cls, number_of_integers, bound, number_of_sequences):
        average_case = cls(number_of_integers, bound, number_of_sequences)
        average_case.generate_sequences()
        average_case.find_hits_and_steps()
        average_case.display_results()

if __name__ == "__main__":
    print("Bound Calculated Real")
    AverageCase.run_all_steps(50, 30, 10000)
    AverageCase.run_all_steps(50, 50, 10000)
    AverageCase.run_all_steps(50, 80, 10000)
    AverageCase.run_all_steps(50, 100, 10000)
    AverageCase.run_all_steps(50, 1000, 10000)
    AverageCase.run_all_steps(50, 10000, 10000)
    AverageCase.run_all_steps(50, maxsize, 10000)