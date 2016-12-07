"""
Bill generator for tmobile

June 8 2016

Vignesh Murugesan

"""

import HTMLParser
import datetime

import requests
from prettytable import PrettyTable

now = datetime.datetime.now()

# Constants
LAST_PAYMENT_DATE = '22nd'
DEFAULT_USERS_COUNT = '5'

# Tips
BoilerPlate = """
Regular usage:

VG: 17
PK: 12.75
"""

# Default bill message
DEFAULT_MESSAGE = """This bill was generated using python!
If you have any suggestions, fork out and share your git-pull requests here
https://github.com/vigneshmurugesan90/scripts/blob/master/bill_gen.py"""


class Person:
    def __init__(self, name, monthly_usage, over_usage):
        self.name = name
        self.monthly_usage = float(monthly_usage)
        self.over_usage = float(over_usage)

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
        self.bill_total = float(bill_total)
        self.persons = persons

    def get_shared_total(self):
        expense_total = 0
        for person in self.persons:
            expense_total += person.get_usage_total()
        shared_total = self.bill_total - expense_total
        return shared_total

    def get_shared_per_head(self):
        return self.get_shared_total() / len(self.persons)

    def generate_report(self):
        print ''
        print ''
        report_text = "\nHello everyone,\n\nBill for month of %s %s:\n\nPer-head-split:\n"
        report_text %= (now.strftime("%B"), str(now.year))
        report_text += "\n%s\n        " % str(self.bill_total)
        for person in self.persons:
            if person.get_usage_total() > 0:
                report_text += "\n-(%.2f+%.2f)\n                " % (person.monthly_usage, person.over_usage)
        report_text += "\n=%.2f / %d = $%.2f" % (self.get_shared_total(),
                         len(self.persons),
                         self.get_shared_per_head())
        report_text += "\n\n\nYour-totals:\n"

        t = PrettyTable(['Name', 'BaseChargeSplit', 'MonthlyUsage', 'Overage', 'Total'])
        # calculate expense
        person_owed_list = []
        for person in self.persons:
            person_owed_list.append(person.get_total_owed(main_bill_share=self.get_shared_per_head()))

        # adjust for round-off
        person_owed_list = [round(owed_value, 2) for owed_value in person_owed_list]
        error = self.bill_total - sum(person_owed_list)
        person_owed_list[now.month % len(person_owed_list)] += error

        # report them
        for i, person in enumerate(self.persons):
            t.add_row([person.name,
                       "{0:.2f}".format(self.get_shared_per_head()),
                       "{0:.2f}".format(person.monthly_usage),
                       "{0:.2f}".format(person.over_usage),
                       "{0:.2f}".format(person_owed_list[i])],
                      )
        report_text += '\n' + str(t) + '\n'
        report_text += "\nLast day for payment: " \
                       + LAST_PAYMENT_DATE \
                       + " of this month.\n\nPs:\n\n#Random-Rajnikanth-Jokes :)\n" \
                       + RandomMsg.get_message()
        print report_text


class Report:
    def __int__(self):
        pass

    @staticmethod
    def print_line():
        print str('-' * 80)

    @staticmethod
    def read_value(key):
        print '%s: ' % key
        return raw_input()

    @staticmethod
    def _read_person_info():
        print '\nUser Info:'
        person_count = Report.read_value('How many users? (Default: ' + DEFAULT_USERS_COUNT + ')') or str(
            DEFAULT_USERS_COUNT)
        print '\nGenerating repot for ' + person_count + ' user(s)...'
        persons = []
        for iPerson in range(int(person_count)):
            Report.print_line()
            print 'User: ' + str(iPerson)
            Report.print_line()
            person = Person(
                Report.read_value('Name (Default: Stranger_*)') or ('Stranger_' + str(iPerson)),
                Report.read_value('Monthly usage (Default: 0)') or '0',
                Report.read_value('Over usage (Default: 0)') or '0',
            )
            persons.append(person)
        return persons

    @staticmethod
    def generate_report():
        Report.print_line()
        print 'TMOBILE REPORT GENERATOR'
        Report.print_line()
        print 'Tips: '
        print BoilerPlate
        Report.print_line()

        bill = Bill(
            Report.read_value('Total Bill Amount'),
            Report._read_person_info(),
        )
        bill.generate_report()


class RandomMsg:
    def __int__(self):
        pass

    @staticmethod
    def get_message():
        r = requests.get('http://api.irkfdb.in/facts/random')
        if not r:
            # api call failed. return default
            return DEFAULT_MESSAGE
        # call succeeded. Return joke
        msg = r.json()
        html_parser = HTMLParser.HTMLParser()
        joke = str(msg['resultSet']['data'][0]['fact'])
        joke = joke.replace('<b>', '')
        joke = joke.replace('</b>', '')
        return html_parser.unescape(joke)


# Entry point
Report.generate_report()
