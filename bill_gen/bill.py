from datetime import datetime
from prettytable import PrettyTable

from common_str import (
    LAST_PAYMENT_DATE,
)

from rand_msg import RandomMsg


class Bill:
    def __init__(self, bill_total, persons):
        self.bill_total = float(bill_total)
        self.persons = persons
        self.now = datetime.now()

    def get_shared_total(self):
        expense_total = 0
        for person in self.persons:
            expense_total += person.get_usage_total()
        shared_total = self.bill_total - expense_total
        return shared_total

    def get_shared_per_head(self):
        return self.get_shared_total() / len(self.persons)

    def generate_report(self):
        # header
        report_text = "\nHello everyone,\n\nBill for month of %s %s:\n\nPer-head-split:\n"
        # bill date
        report_text %= (self.now.strftime("%B"), str(self.now.year))
        # bill total
        report_text += "\n%s\n        " % str(self.bill_total)
        # each person's bill
        for person in self.persons:
            if person.get_usage_total() > 0:
                report_text += "\n-(%.2f+%.2f)\n                " % (person.monthly_usage, person.over_usage)
        report_text += "\n=%.2f / %d = $%.2f" % (self.get_shared_total(),
                         len(self.persons),
                         self.get_shared_per_head())
        report_text += "\n\n\nYour-totals:\n"

        # tabulate
        t = PrettyTable(['Name', 'BaseChargeSplit', 'MonthlyUsage', 'Overage', 'Total'])
        # calculate expense
        person_owed_list = []
        for person in self.persons:
            person_owed_list.append(person.get_total_owed(main_bill_share=self.get_shared_per_head()))

        # adjust for round-off
        person_owed_list = [round(owed_value, 2) for owed_value in person_owed_list]
        error = self.bill_total - sum(person_owed_list)
        person_owed_list[self.now.month % len(person_owed_list)] += error

        # generate report
        for i, person in enumerate(self.persons):
            t.add_row([person.name,
                       "{0:.2f}".format(self.get_shared_per_head()),
                       "{0:.2f}".format(person.monthly_usage),
                       "{0:.2f}".format(person.over_usage),
                       "{0:.2f}".format(person_owed_list[i])],
                      )
        report_text += '\n' + str(t) + '\n'

        # payment due-date
        report_text += "\nLast day for payment: " \
                       + LAST_PAYMENT_DATE \
                       + " of this month.\n\nPs:\n\n#Random-Rajnikanth-Jokes :)\n" \
                       + RandomMsg.get_message()
        return report_text
