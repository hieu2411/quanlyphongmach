import datetime

from dateutil import parser
from flask import *

from app import Statistic, Drug, Receipt, Medical_bill
from route.function_route import equal_datetime

accountant_route = Blueprint('accountant_route', __name__)


def not_in(days, date):
    for day in days:
        if equal_datetime(day, date):
            return False
    return True


def get_profit_drugs_sold_report():
    # get all the day that have medical bills (unique)
    # put drug solds, patients, receipt into day
    days = []
    drugs = []
    profits = []
    drug_solds = Statistic.query.group_by(Statistic.date).all()
    receipts = Receipt.query.all()
    for drug_sold in drug_solds:
        # add new day into days
        if len(days) == 0 or not_in(days, drug_sold.date):
            days.append(datetime.datetime(drug_sold.date.year, drug_sold.date.month, drug_sold.date.day))
            profits.append(drug_sold.profit)
            drug = Drug.query.get(drug_sold.drug_id)
            drugs.append([{
                'drug': drug.name,
                'price_in': drug.price_in,
                'price_out': drug.price_out,
                'quantity': drug_sold.quantity,
                'profit': drug_sold.profit
            }])
        else:
            # append more value into existed day
            for day in days:
                if equal_datetime(day, drug_sold.date):
                    index = days.index(day)
                    drug = Drug.query.get(drug_sold.drug_id)
                    drugs[index].append({
                        'drug': drug.name,
                        'price_in': drug.price_in,
                        'price_out': drug.price_out,
                        'quantity': drug_sold.quantity,
                        'profit': drug_sold.profit
                    })
                    profits[index] += drug_sold.profit


    result = []
    for i in range(len(days)):
        result.append({
            'date': days[i],
            'profit': profits[i],
            'fee': 0,
            'drugs_sold': drugs[i],
        })
    # add examination fee to each day
    for receipt in receipts:
        bill = Medical_bill.query.get(receipt.medical_bill_id)
        for day in days:
            if equal_datetime(day, bill.examination_date):
                result[days.index(day)]['fee'] += receipt.fee
    return result


@accountant_route.route('/admin/accountant/profit/index')
def profit_index():
    # check if signed in then show lower users list
    if session.get('signed_in'):
        result = get_profit_drugs_sold_report()
        return render_template('admin/accountant/profit_index.html', data=result, role=session['role'],
                               title='Profit index')
    return redirect('/admin/login')


@accountant_route.route('/admin/accountant/profit/details/<date>', methods=['get', 'post'])
def profit_details(date):
    if session.get('signed_in'):
        date = parser.parse(date)
        results = get_profit_drugs_sold_report()
        result_detail = None
        for result in results:
            if equal_datetime(result['date'], date):
                result_detail = result
                return render_template('admin/accountant/profit_details.html', data=result_detail, role=session['role'],
                                       title=str(date.day) + '/' + str(date.month) + '/' + str(
                                           date.year) + ' profit detail')

        flash('Report not found')
        return render_template('admin/accountant/profit_details.html', data=None, role=session['role'],
                               title='Profit detail not found')
    return redirect('/admin/login')


@accountant_route.route('/admin/accountant/drugs_sold/index')
def drugs_sold_index():
    # check if signed in then show lower users list
    if session.get('signed_in'):
        result = get_profit_drugs_sold_report()
        return render_template('admin/accountant/drugs_sold_index.html', data=result, role=session['role'],
                               title='Drugs sold index')
    return redirect('/admin/login')


@accountant_route.route('/admin/accountant/drugs_sold/details/<date>', methods=['get', 'post'])
def drugs_sold_details(date):
    if session.get('signed_in'):
        date = parser.parse(date)
        results = get_profit_drugs_sold_report()
        result_detail = None
        for result in results:
            if equal_datetime(result['date'], date):
                result_detail = result
                return render_template('admin/accountant/drugs_sold_details.html', data=result_detail, role=session['role'],
                                       title=str(date.day) + '/' + str(date.month) + '/' + str(
                                           date.year) + ' drugs sold detail')

        flash('Report not found')
        return render_template('admin/accountant/profit_details.html', data=None, role=session['role'],
                               title='Profit detail not found')
    return redirect('/admin/login')
