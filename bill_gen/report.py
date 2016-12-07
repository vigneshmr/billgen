from bill import Bill
from common_str import (
    BOILER_PLATE,
    DEFAULT_USERS_COUNT,
)
from person import Person
from util import Util


class Report:
    def __int__(self):
        pass

    def _read_person_info(self):
        Util.write('\nUser Info:')
        person_count = Util.read_value('How many users? (Default: ' + DEFAULT_USERS_COUNT + ')') or str(
            DEFAULT_USERS_COUNT)
        Util.write('\nGenerating report for ' + person_count + ' user(s)...')
        persons = []
        for iPerson in range(int(person_count)):
            Util.print_line()
            Util.write('User: ' + str(iPerson))
            Util.print_line()
            person = Person(
                Util.read_value('Name (Default: Person_*)') or ('Person_' + str(iPerson)),
                Util.read_value('Monthly usage (Default: 0)') or '0',
                Util.read_value('Over usage (Default: 0)') or '0',
            )
            persons.append(person)
        return persons

    def generate_report(self):
        Util.print_line()
        Util.write('Family bill generator')
        Util.print_line()
        Util.write ('Tips: ')
        Util.write(BOILER_PLATE)
        Util.print_line()

        bill = Bill(
            Util.read_value('Total Bill Amount'),
            self._read_person_info(),
        )
        Util.print_line()
        Util.write('*** Bill ***')
        Util.print_line()
        Util.write(bill.generate_report())
