# This is my first use of **class** as I study Python and proper use of it. The class Person is quite simple: name, height, and weight, and  Critique and suggestions are welcome!
# Code Review is a community where programmers peer-review your working code to address issues such as security, maintainability, performance, and scalability. We require that the code be working correctly, to the best of the author's knowledge, before proceeding with a review."

class Person:
    BMI_UNDER = 0
    BMI_HEALTHY = 1
    BMI_OVER = 2
    BMI_STATUS = ['underweight', 'healthy', 'overweight']
    BMI_CODE = ['BMI_UNDER', 'BMI_HEALTHY', 'BMI_OVER']

    def __init__(self, name, height, weight):
        self._name = name
        self._height = height
        self._weight = weight

    def get_name(self):
        return self._name

    def get_bmi(self):
        return self._weight * 703 / self._height ** 2

    def get_bmi_type(self):
        bmi = self.get_bmi()
        if bmi < 18.5:
            status = Person.BMI_UNDER
        elif bmi < 25.0:
            status = Person.BMI_HEALTHY
        else:
            status = Person.BMI_OVER
        return status

    def get_bmi_status(self):
        return Person.BMI_STATUS[self.get_bmi_type()]

    def get_bmi_code(self):
        return Person.BMI_CODE[self.get_bmi_type()]

    def get_bmi_report(self):
        return 'BMI is %.1f %s' % (self.get_bmi(), self.get_bmi_status())


if __name__ == '__main__':

    def first_test():
        test_list = [
            ('Major Fat', 69, 170, Person.BMI_OVER),
            ('Ann Smart', 69, 169, Person.BMI_HEALTHY),
            ('Mary Cool', 69, 126, Person.BMI_HEALTHY),
            ('Ed Skinny', 69, 125, Person.BMI_UNDER),
        ]
        for name, height, weight, expected in test_list:
            person = Person(name, height, weight)
            print(person.get_name(), person.get_bmi_report())
            if person.get_bmi_type() != expected:
                print('*** ERROR expected:', Person.BMI_STATUS[expected])
        print()

    def get_integer(from_int, to_int, question):
        while True:
            try:
                i = int(input(question + ': '))
                if from_int <= i <= to_int:
                    break
            except ValueError:
                pass
            print('Enter an integer from {0} to {1}'.format(from_int, to_int))
        return i

    def interactive_test():
        new_list = []
        while True:
            name = input('Enter name: ')
            if not name:  # Exit if the name is blank ''
                print('Thank you for testing', end='')
                print('' if len(new_list) == 0 else '\nTest list to reuse...')
                break
            height = get_integer(22, 108, 'Enter your height in inches')
            weight = get_integer(4, 1400, 'Enter your weight in lbs')
            person = Person(name, height, weight)
            print(person.get_bmi_report())
            new_list += [(name, height, weight)]
        for name, height, weight in new_list:
            person = Person(name, height, weight)
            status_name = 'Person.' + person.get_bmi_code()
            print("('%s', %d, %d, %s)," % (name, height, weight, status_name))

    first_test()
    interactive_test()
