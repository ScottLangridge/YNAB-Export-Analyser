from collections import defaultdict
from datetime import datetime
from enum import Enum


class TransactionList:
    def __init__(self, transactions=None):
        self.transactions = transactions if transactions is not None else []

    def import_csv(self, filepath):
        with open(filepath, 'r') as f:
            transaction_strings = [line.strip('\n') for line in f.readlines()[1:]]
        self.add_transactions([Transaction(line) for line in transaction_strings])

    def add_transaction(self, transaction):
        assert transaction.tid not in map(lambda t: t.tid, self.transactions)
        self.transactions.append(transaction)

    def add_transactions(self, transactions):
        for transaction in transactions:
            assert transaction.tid not in map(lambda t: t.tid, self.transactions)
        self.transactions.extend(transactions)

    def filter(self, filter_function, in_place=True):
        if in_place:
            self.transactions = list(filter(filter_function, self.transactions))
        else:
            return TransactionList(list(filter(filter_function, self.transactions)))

    def quick_filter_internal(self, in_place=True):
        def filter_func(x): return not (
                x.payee == 'Starting Balance' or
                x.payee == 'Rainy Day Fund' or
                x.payee.startswith('Transfer : ')
        )

        self.filter(filter_func, in_place)

    def breakdown_spend_by_field(self, field):
        get_value = {
            Field.ACCOUNT: lambda x: x.account,
            Field.FLAG: lambda x: x.flag,
            Field.DATE: lambda x: x.date,
            Field.PAYEE: lambda x: x.payee,
            Field.CATEGORY_GROUP_CATEGORY: lambda x: x.category_group_category,
            Field.CATEGORY_GROUP: lambda x: x.category_group,
            Field.CATEGORY: lambda x: x.category,
            Field.MEMO: lambda x: x.memo,
            Field.CLEARED: lambda x: x.cleared,
        }

        spent = defaultdict(int)
        for transaction in self.transactions:
            spent[get_value[field](transaction)] += transaction.outflow
        return spent

    # Expects dict of new name to list of old names.
    # e.g. {'Travel': ['Trainline', 'Northern Rail']}
    def rename_payees(self, replaces_dict):
        # Converts to dict of old name to new name for easier use.
        # e.g. {'Trainline': 'Travel', "Northern Rail': 'Travel'}
        replace = {}
        for new, lst_old in replaces_dict.items():
            for old in lst_old:
                replace[old] = new

        for i in range(len(self.transactions)):
            self.transactions[i].payee = replace.get(self.transactions[i].payee, self.transactions[i].payee)


class Transaction:
    next_transaction_id = 0

    def __init__(self, str_transaction):
        self.tid = Transaction.next_transaction_id
        Transaction.next_transaction_id += 1

        split_transaction = [i.strip('"') for i in str_transaction.split(',')]
        self.account = split_transaction[0]
        self.flag = split_transaction[1]
        self.date = datetime.strptime(split_transaction[2], "%d/%m/%Y").date()
        self.payee = split_transaction[3]
        self.category_group_category = split_transaction[4]
        self.category_group = split_transaction[5]
        self.category = split_transaction[6]
        self.memo = split_transaction[7]
        self.outflow = float(split_transaction[8])
        self.inflow = float(split_transaction[9])
        self.net = self.inflow - self.outflow
        self.cleared = split_transaction[10] == 'Cleared'


class Field(Enum):
    ACCOUNT = 1
    FLAG = 2
    DATE = 3
    PAYEE = 4
    CATEGORY_GROUP_CATEGORY = 5
    CATEGORY_GROUP = 6
    CATEGORY = 7
    MEMO = 8
    OUTFLOW = 9
    INFLOW = 10
    NET = 11
    CLEARED = 12
