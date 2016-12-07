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
