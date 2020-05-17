# from flask import *
#
# from app import Receipt
#
# accountant_route = Blueprint('accountant_route', __name__)
#
#
# @accountant_route.route('/admin/accountant/index')
# def accountant_index():
#     # check if signed in then show lower users list
#     if session.get('signed_in'):
#         data = Receipt.query.all()
#         if data:
#             return render_template('admin/accountant/index.html', data=data, role=session['role'], title = 'Receipt index')
#         return render_template('admin/accountant/index.html', data=None, role=session['role'], title = 'Receipt index')
#     return redirect('/admin/login')
#
#
# @accountant_route.route('/admin/accountant/create', methods=['GET', 'POST'])
# def create_accountant():
#     # check if signed in then show lower users list
#     if session.get('signed_in'):
#         if request.method == 'POST':
#             result = Receipt.create(accountant=request.form['name'])
#             if result is not None:
#                 flash('Successfully added new accountant')
#         return render_template('admin/accountant/create.html', role=session['role'], title = 'Add accountant')
#     return redirect('/admin/login')
#
#
# @accountant_route.route('/admin/accountant/details/<id>', methods=['get', 'post'])
# def accountant_details(id):
#     if session.get('signed_in'):
#
#         # find that accountant by id
#         accountant = Receipt.query.get(id)
#         if accountant:
#             # in jinja use items() to unpack key and value from dict
#             return render_template('admin/accountant/detail.html', data=accountant.as_dict(), role=session['role'], title = 'Receipt detail')
#         flash('Receipt not found')
#     return redirect('/admin/login')
#
#
# @accountant_route.route('/admin/accountant/edit/<id>', methods=['GET', 'POST'])
# def accountant_edit(id):
#     if session.get('signed_in'):
#         accountant = Receipt.query.get(id)
#         if accountant:
#             if request.method == 'POST':
#                 update_data = {'id': id,
#                                'accountant': request.form['name'],
#                                }
#                 Receipt.update(data=update_data)
#                 return redirect('/admin/accountant/index')
#             # show info first
#             return render_template('admin/accountant/edit.html', data=accountant.as_dict(), role=session['role'], title = 'Edit accountant')
#         return render_template('admin/accountant/edit.html', data=None, role = session['role'], title = 'Edit accountant')
#     return redirect('/admin/login')
#
#
# @accountant_route.route('/admin/accountant/delete/<id>', methods=['GET', 'POST'])
# def accountant_delete(id):
#     if session.get('signed_in'):
#
#         # won't delete, only change is_Active to False
#
#         # find user with id
#         accountant = Receipt.query.get(id)
#         if request.method == 'POST':
#             Receipt.delete(id)
#             return redirect('/admin/accountant/index')
#         if accountant:
#             return render_template('admin/accountant/delete.html', data=accountant.as_dict(), role=session['role'], title = 'Receipt details')
#         # need some more code for confirmation
#
#     return redirect('/admin/login')
