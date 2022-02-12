from TransactionList import TransactionList, Field
from Plotter import Plotter

t_list = TransactionList()
t_list.import_csv('transactions.csv')
t_list.quick_filter_internal()

fun_money_list = t_list.filter(lambda x: x.category_group == "Fun Money", in_place=False)

rename_dict = {
    'Evening Food Drinks': ['Little Bao Boy', 'Ndr Cafe And Pub L', 'The Round Table Di', 'Zaap Thai', "Lister's Arms", 'Rough Trade'],
    'Snack Food Drinks': ['Kapow Coffee', 'Greggs', 'La Stazione', "Mcdonald's", 'Pumpkin CafĀ©'],
    'Travel': ['Nottingham City Transport Travel Centre', 'Tramlink Nottingham', 'National Express', 'Trainline', "Northern Trains Limited"],
    'Snooker': ['POST OFFICE 116 ALBION STREET 12FEB 13.23 ATM']
}
fun_money_list.rename_payees(rename_dict)
# Plotter().dict_to_pie(fun_money_list.breakdown_spend_by_field(Field.PAYEE))
Plotter().dict_to_pie(t_list.breakdown_spend_by_field(Field.CATEGORY_GROUP))
