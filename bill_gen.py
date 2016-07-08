"""
Bill generator for tmobile

June 8 2016

Vignesh Murugesan

"""

import datetime
import random
import itertools

now = datetime.datetime.now()

# Tips
BoilerPlate = """
Regular usage:

VG: 17
PK: 12.75
"""

class Person:
    def __init__(self, name, monthly_usage, over_usage):
        self.name = name
        self.monthly_usage= float(monthly_usage)
        self.over_usage= float(over_usage)

    def get_usage_total(self):
        """
        get bill-split + monthly usage and over_usage of person
        :return:
        """
        return self.monthly_usage + self.over_usage

    def get_total_owed(self, main_bill_share):
        return self.get_usage_total() + main_bill_share


class Bill:
    def __init__(self, bill_total, persons):
        self.bill_total=float(bill_total)
        self.persons = persons

    def get_shared_total(self):
        shared_total = 0
        expense_total = 0
        for person in self.persons:
            expense_total += person.get_usage_total()
        shared_total = self.bill_total - expense_total
        return shared_total

    def get_shared_per_head(self):
        return self.get_shared_total()/len(self.persons)

    def generate_report(self):
        report = self.persons
        print ''
        print ''
        report_text = """
Hello everyone,

Bill for month of %s %s:

Per-head-split:
"""
        report_text = report_text % (now.strftime("%B"), str(now.year))
        report_text += """
%s
        """ % str(self.bill_total)
        for person in self.persons:
            if person.get_usage_total() > 0:
                report_text += """
-(%.2f+%.2f)
                """%(person.monthly_usage, person.over_usage)

        report_text += """
=%.2f / %d = $%.2f"""%(self.get_shared_total(),
             len(self.persons),
             self.get_shared_per_head())

        report_text += """


Your-total:
"""

        # calculate expense
        person_owed_list = []
        for person in self.persons:
            person_owed_list.append(person.get_total_owed(main_bill_share=self.get_shared_per_head()))

        # correct round-off
        error = self.bill_total - sum(person_owed_list)
        person_owed_list[random.randint(0,len(person_owed_list)-1)] += error

        # report them
        for i, person in enumerate(self.persons):
            report_text+="""
%s %.2f + %.2f + %.2f  = %.2f""" % (person.name,
                                    self.get_shared_per_head(),
                                    person.monthly_usage,
                                    person.over_usage,
                                    person_owed_list[i])

        report_text += """
Last day for payment: 22nd of this month.

Ps:

#Bill-Trivia :)
This bill was generated using python!
If you have any suggestions, fork out and share your git-pull requests here
https://github.com/vigneshmurugesan90/scripts/blob/master/bill_gen.py
        """
        print report_text
        print 'Adjusted total: %f' % sum(person_owed_list)


class Report:
    def __int__(self):
        pass

    @staticmethod
    def print_line():
        print ['-' * 80]

    @staticmethod
    def read_value(key):
        print '%s: '%key
        return raw_input()

    @staticmethod
    def _read_person_info():
        print '  User Info:'
        person_count = Report.read_value('How many users?')
        persons = []
        for _ in range(int(person_count)):
            person = Person(
                Report.read_value('Name'),
                Report.read_value('Monthly usage'),
                Report.read_value('Over usage'),
            )
            persons.append(person)
        return persons

    @staticmethod
    def generate_report():
        Report.print_line()
        print '  TMOBILE REPORT GENERATOR'
        Report.print_line()
        print 'Tips: '
        print BoilerPlate
        Report.print_line()

        bill = Bill(
            Report.read_value('Total Bill Amount'),
            Report._read_person_info(),
        )
        bill.generate_report()


# Entry point
Report.generate_report()
