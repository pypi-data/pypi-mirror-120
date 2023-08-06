======================
Account Batch Scenario
======================

Imports::

    >>> import datetime
    >>> from dateutil.relativedelta import relativedelta
    >>> from decimal import Decimal
    >>> from proteus import config, Model, Wizard
    >>> from trytond.tests.tools import activate_modules
    >>> from trytond.modules.company.tests.tools import create_company, \
    ...     get_company
    >>> from trytond.modules.account.tests.tools import create_fiscalyear, \
    ...     create_chart, get_accounts, create_tax, create_tax_code
    >>> from trytond.modules.account_invoice.tests.tools import \
    ...     set_fiscalyear_invoice_sequences, create_payment_term
    >>> today = datetime.date.today()

Install account_batch::

    >>> config = activate_modules('account_batch')

Create company::

    >>> _ = create_company()
    >>> company = get_company()

Create fiscal year::

    >>> fiscalyear = set_fiscalyear_invoice_sequences(
    ...     create_fiscalyear(company))
    >>> fiscalyear.click('create_period')
    >>> period = fiscalyear.periods[0]

Create chart of accounts::

    >>> _ = create_chart(company)
    >>> accounts = get_accounts(company)
    >>> revenue = accounts['revenue']
    >>> expense = accounts['expense']
    >>> receivable = accounts['receivable']
    >>> payable = accounts['payable']
    >>> cash = accounts['cash']
    >>> tax = accounts['tax']

Create taxes with codes::

    >>> tax_out = create_tax(Decimal('0.19'))
    >>> base19out = create_tax_code(tax_out, amount='base')
    >>> base19out.save()
    >>> tax19out = create_tax_code(tax_out)
    >>> tax19out.save()
    >>> tax_in = create_tax(Decimal('0.19'))
    >>> base19in = create_tax_code(tax_in, amount='base')
    >>> base19in.save()
    >>> tax19in = create_tax_code(tax_in)
    >>> tax19in.save()

Create sequence and account journal::

    >>> Sequence = Model.get('ir.sequence')
    >>> AccountJournal = Model.get('account.journal')

    >>> sequence = Sequence(name='Bank',
    ...     code='account.journal',
    ...     company=company,
    ... )
    >>> sequence.save()
    >>> account_journal = AccountJournal(name='Bank',
    ...     type='bank',
    ...     sequence=sequence,
    ... )
    >>> account_journal.save()     

Create a batch journal::

    >>> BatchJournal = Model.get('account.batch.journal')

    >>> batch_journal = BatchJournal(name='Batch Bank',
    ...     account_journal=account_journal,
    ...     currency=company.currency,
    ...     company=company,
    ... )
    >>> batch_journal.save()

Create parties::

    >>> Party = Model.get('party.party')
    >>> customer = Party(name='Customer')
    >>> customer.save()
    >>> supplier = Party(name='Supplier')
    >>> supplier.save()

Create payment term::

    >>> payment_term = create_payment_term()
    >>> payment_term.save()

Create a batch user::

    >>> User = Model.get('res.user')
    >>> Group = Model.get('res.group')
    >>> Party = Model.get('party.party')
    >>> Employee = Model.get('company.employee')
    >>> batch_user = User()
    >>> batch_user.name = 'Batch User'
    >>> batch_user.login = 'batch'
    >>> batch_user.main_company = company
    >>> batch_group, = Group.find([('name', '=', 'Batch')])
    >>> batch_user.groups.append(batch_group)
    >>> account_group, = Group.find([('name', '=', 'Account')])
    >>> batch_user.groups.append(account_group)
    >>> employee_party = Party(name="Batch Employee")
    >>> employee_party.save()
    >>> employee = Employee(party=employee_party)
    >>> employee.save()
    >>> batch_user.employees.append(employee)
    >>> batch_user.employee = employee
    >>> batch_user.save()
    >>> print(1, config.user)
    >>> config.user = batch_user.id
    >>> config._context = User.get_preferences(True, config.context)
    >>> print(2, config.user)

Create a batch and check for missing account on journal::

    >>> Batch = Model.get('account.batch')
    >>> batch = Batch(name='Testbatch',
    ...     journal=batch_journal,
    ... )  # doctest: +IGNORE_EXCEPTION_DETAIL 
    Traceback (most recent call last):
        ...
    UserError: ...

Create a batch after configuring the journal with an account::

    >>> batch_journal.account = cash
    >>> batch_journal.save()
    >>> batch = Batch(name='Testbatch',
    ...     journal=batch_journal,
    ... )
    >>> batch.save()

Create a revenue batch line without tax::

    >>> BatchLine = Model.get('account.batch.line')
    >>> batch_line1 = BatchLine(journal=batch_journal,
    ...     batch=batch,
    ...     date=today,
    ...     amount=Decimal(100),
    ...     account=cash,
    ...     contra_account=revenue,
    ... )
    >>> batch_line1.save()
    >>> batch_line1.side_account
    'debit'
    >>> batch_line1.side_contra_account
    'credit'
    >>> len(batch.lines)
    1
    >>> len(batch.move_lines)
    2
    >>> revenue.reload()
    >>> revenue.credit
    Decimal('100.00')
    >>> revenue.debit
    Decimal('0.00')
    >>> expense.reload()
    >>> expense.credit
    Decimal('0.00')
    >>> expense.debit
    Decimal('0.00')
    >>> cash.reload()
    >>> cash.credit
    Decimal('0.00')
    >>> cash.debit
    Decimal('100.00')
    >>> base19out.reload()
    >>> base19out.amount
    Decimal('0.00')
    >>> tax19out.reload()
    >>> tax19out.amount
    Decimal('0.00')
    >>> base19in.reload()
    >>> base19in.amount
    Decimal('0.00')
    >>> tax19in.reload()
    >>> tax19in.amount
    Decimal('0.00')

Cancel the former line::

    >>> batch_line2 = BatchLine(journal=batch_journal,
    ...     batch=batch,
    ...     date=today,
    ...     amount=Decimal(-100),
    ...     contra_account=revenue,
    ...     account=cash,
    ...     is_cancelation_move=True,
    ... )
    >>> batch_line2.save()
    >>> batch_line2.is_cancelation_move
    1
    >>> batch_line2.side_account
    'credit'
    >>> batch_line2.side_contra_account
    'debit'
    >>> batch.reload()
    >>> len(batch.lines)
    2
    >>> len(batch.move_lines)
    4
    >>> revenue.reload()
    >>> revenue.credit
    Decimal('0.00')
    >>> revenue.debit
    Decimal('0.00')
    >>> expense.reload()
    >>> expense.credit
    Decimal('0.00')
    >>> expense.debit
    Decimal('0.00')
    >>> cash.reload()
    >>> cash.credit
    Decimal('0.00')
    >>> cash.debit
    Decimal('0.00')
    >>> base19out.reload()
    >>> base19out.amount
    Decimal('0.00')
    >>> tax19out.reload()
    >>> tax19out.amount
    Decimal('0.00')
    >>> base19in.reload()
    >>> base19in.amount
    Decimal('0.00')
    >>> tax19in.reload()
    >>> tax19in.amount
    Decimal('0.00')

Create an expense batch line without tax::

    >>> batch_line3 = BatchLine(journal=batch_journal,
    ...     batch=batch,
    ...     date=today,
    ...     amount=Decimal(-100),
    ...     account=cash,
    ...     contra_account=expense,
    ... )
    >>> batch_line3.save()
    >>> batch_line3.side_account
    'credit'
    >>> batch_line3.side_contra_account
    'debit'
    >>> batch.reload()
    >>> len(batch.lines)
    3
    >>> len(batch.move_lines)
    6
    >>> revenue.reload()
    >>> revenue.credit
    Decimal('0.00')
    >>> revenue.debit
    Decimal('0.00')
    >>> expense.reload()
    >>> expense.credit
    Decimal('0.00')
    >>> expense.debit
    Decimal('100.00')
    >>> cash.reload()
    >>> cash.credit
    Decimal('100.00')
    >>> cash.debit
    Decimal('0.00')
    >>> base19out.reload()
    >>> base19out.amount
    Decimal('0.00')
    >>> tax19out.reload()
    >>> tax19out.amount
    Decimal('0.00')
    >>> base19in.reload()
    >>> base19in.amount
    Decimal('0.00')
    >>> tax19in.reload()
    >>> tax19in.amount
    Decimal('0.00')

Cancel the former line::

    >>> batch_line4 = BatchLine(journal=batch_journal,
    ...     batch=batch,
    ...     date=today,
    ...     amount=Decimal(100),
    ...     account=cash,
    ...     contra_account=expense,
    ...     is_cancelation_move=True,
    ... )
    >>> batch_line4.save()
    >>> batch_line4.side_account
    'debit'
    >>> batch_line4.side_contra_account
    'credit'
    >>> batch.reload()
    >>> len(batch.lines)
    4
    >>> len(batch.move_lines)
    8
    >>> revenue.reload()
    >>> revenue.credit
    Decimal('0.00')
    >>> revenue.debit
    Decimal('0.00')
    >>> expense.reload()
    >>> expense.credit
    Decimal('0.00')
    >>> expense.debit
    Decimal('0.00')
    >>> cash.reload()
    >>> cash.credit
    Decimal('0.00')
    >>> cash.debit
    Decimal('0.00')
    >>> base19out.reload()
    >>> base19out.amount
    Decimal('0.00')
    >>> tax19out.reload()
    >>> tax19out.amount
    Decimal('0.00')
    >>> base19in.reload()
    >>> base19in.amount
    Decimal('0.00')
    >>> tax19in.reload()
    >>> tax19in.amount
    Decimal('0.00')

Create a revenue batch line with tax::

    >>> batch_line5 = BatchLine(journal=batch_journal,
    ...     batch=batch,
    ...     date=today,
    ...     amount=Decimal(1000),
    ...     account=cash,
    ...     contra_account=revenue,
    ...     tax=tax_out,
    ... )
    >>> batch_line5.save()
    >>> batch_line5.side_account
    'debit'
    >>> batch_line5.side_contra_account
    'credit'
    >>> batch.reload()
    >>> len(batch.lines)
    5
    >>> len(batch.move_lines)
    11
    >>> revenue.reload()
    >>> revenue.credit
    Decimal('840.34')
    >>> revenue.debit
    Decimal('0.00')
    >>> expense.reload()
    >>> expense.credit
    Decimal('0.00')
    >>> expense.debit
    Decimal('0.00')
    >>> cash.reload()
    >>> cash.credit
    Decimal('0.00')
    >>> cash.debit
    Decimal('1000.00')
    >>> base19out.reload()
    >>> base19out.amount
    Decimal('840.34')
    >>> tax19out.reload()
    >>> tax19out.amount
    Decimal('159.66')
    >>> base19in.reload()
    >>> base19in.amount
    Decimal('0.00')
    >>> tax19in.reload()
    >>> tax19in.amount
    Decimal('0.00')

Cancel the former line::

    >>> batch_line6 = BatchLine(journal=batch_journal,
    ...     batch=batch,
    ...     date=today,
    ...     amount=Decimal(-1000),
    ...     account=cash,
    ...     contra_account=revenue,
    ...     tax=tax_out,
    ...     is_cancelation_move=True,
    ... )
    >>> batch_line6.save()
    >>> batch_line6.side_account
    'credit'
    >>> batch_line6.side_contra_account
    'debit'
    >>> batch.reload()
    >>> len(batch.lines)
    6
    >>> len(batch.move_lines)
    14
    >>> revenue.reload()
    >>> revenue.credit
    Decimal('0.00')
    >>> revenue.debit
    Decimal('0.00')
    >>> expense.reload()
    >>> expense.credit
    Decimal('0.00')
    >>> expense.debit
    Decimal('0.00')
    >>> cash.reload()
    >>> cash.credit
    Decimal('0.00')
    >>> cash.debit
    Decimal('0.00')
    >>> base19out.reload()
    >>> base19out.amount
    Decimal('0.00')
    >>> tax19out.reload()
    >>> tax19out.amount
    Decimal('0.00')
    >>> base19in.reload()
    >>> base19in.amount
    Decimal('0.00')
    >>> tax19in.reload()
    >>> tax19in.amount
    Decimal('0.00')

Create an expense batch line with tax::

    >>> batch_line7 = BatchLine(journal=batch_journal,
    ...     batch=batch,
    ...     date=today,
    ...     amount=Decimal(-1000),
    ...     account=cash,
    ...     contra_account=expense,
    ...     tax=tax_in,
    ... )
    >>> batch_line7.save()
    >>> batch_line7.side_account
    'credit'
    >>> batch_line7.side_contra_account
    'debit'
    >>> batch.reload()
    >>> len(batch.lines)
    7
    >>> len(batch.move_lines)
    17
    >>> revenue.reload()
    >>> revenue.credit
    Decimal('0.00')
    >>> revenue.debit
    Decimal('0.00')
    >>> expense.reload()
    >>> expense.credit
    Decimal('0.00')
    >>> expense.debit
    Decimal('840.34')
    >>> cash.reload()
    >>> cash.credit
    Decimal('1000.00')
    >>> cash.debit
    Decimal('0.00')
    >>> base19out.reload()
    >>> base19out.amount
    Decimal('0.00')
    >>> tax19out.reload()
    >>> tax19out.amount
    Decimal('0.00')
    >>> base19in.reload()
    >>> base19in.amount
    Decimal('-840.34')
    >>> tax19in.reload()
    >>> tax19in.amount
    Decimal('-159.66')

Cancel the former line::

    >>> batch_line8 = BatchLine(journal=batch_journal,
    ...     batch=batch,
    ...     date=today,
    ...     amount=Decimal(1000),
    ...     account=cash,
    ...     contra_account=expense,
    ...     tax=tax_in,
    ...     is_cancelation_move=True,
    ... )
    >>> batch_line8.save()
    >>> batch_line8.side_account
    'debit'
    >>> batch_line8.side_contra_account
    'credit'
    >>> batch.reload()
    >>> len(batch.lines)
    8
    >>> len(batch.move_lines)
    20
    >>> revenue.reload()
    >>> revenue.credit
    Decimal('0.00')
    >>> revenue.debit
    Decimal('0.00')
    >>> expense.reload()
    >>> expense.credit
    Decimal('0.00')
    >>> expense.debit
    Decimal('0.00')
    >>> cash.reload()
    >>> cash.credit
    Decimal('0.00')
    >>> cash.debit
    Decimal('0.00')
    >>> base19out.reload()
    >>> base19out.amount
    Decimal('0.00')
    >>> tax19out.reload()
    >>> tax19out.amount
    Decimal('0.00')
    >>> base19in.reload()
    >>> base19in.amount
    Decimal('0.00')
    >>> tax19in.reload()
    >>> tax19in.amount
    Decimal('0.00')

Create 2 customer invoices::

    >>> Invoice = Model.get('account.invoice')
    >>> customer_invoice1 = Invoice(type='out')
    >>> customer_invoice1.party = customer
    >>> customer_invoice1.payment_term = payment_term
    >>> invoice_line = customer_invoice1.lines.new()
    >>> invoice_line.quantity = 1
    >>> invoice_line.unit_price = Decimal('100')
    >>> invoice_line.account = revenue
    >>> invoice_line.description = 'Test'
    >>> customer_invoice1.click('post')
    >>> customer_invoice1.state
    u'posted'

    >>> customer_invoice2 = Invoice(type='out')
    >>> customer_invoice2.party = customer
    >>> customer_invoice2.payment_term = payment_term
    >>> invoice_line = customer_invoice2.lines.new()
    >>> invoice_line.quantity = 1
    >>> invoice_line.unit_price = Decimal('150')
    >>> invoice_line.account = revenue
    >>> invoice_line.description = 'Test'
    >>> customer_invoice2.click('post')
    >>> customer_invoice2.state
    u'posted'

Create 1 customer credit note::

    >>> customer_credit_note = Invoice(type='out')
    >>> customer_credit_note.party = customer
    >>> customer_credit_note.payment_term = payment_term
    >>> invoice_line = customer_credit_note.lines.new()
    >>> invoice_line.quantity = -1
    >>> invoice_line.unit_price = Decimal('50')
    >>> invoice_line.account = revenue
    >>> invoice_line.description = 'Test'
    >>> customer_credit_note.click('post')
    >>> customer_credit_note.state
    u'posted'

Create 1 supplier invoice::

    >>> supplier_invoice = Invoice(type='in')
    >>> supplier_invoice.party = supplier
    >>> supplier_invoice.payment_term = payment_term
    >>> invoice_line = supplier_invoice.lines.new()
    >>> invoice_line.quantity = 1
    >>> invoice_line.unit_price = Decimal('50')
    >>> invoice_line.account = expense
    >>> invoice_line.description = 'Test'
    >>> supplier_invoice.invoice_date = today
    >>> supplier_invoice.click('post')
    >>> supplier_invoice.state
    u'posted'

Check for intermediate results::
 
    >>> receivable.reload()
    >>> receivable.credit
    Decimal('50.00')
    >>> receivable.debit
    Decimal('250.00')
    >>> payable.reload()
    >>> payable.credit
    Decimal('50.00')
    >>> payable.debit
    Decimal('0.00')

    >>> revenue.reload()
    >>> revenue.credit
    Decimal('250.00')
    >>> revenue.debit
    Decimal('50.00')
    >>> expense.reload()
    >>> expense.credit
    Decimal('0.00')
    >>> expense.debit
    Decimal('50.00')

    >>> cash.reload()
    >>> cash.credit
    Decimal('0.00')
    >>> cash.debit
    Decimal('0.00')
    >>> base19out.reload()
    >>> base19out.amount
    Decimal('0.00')
    >>> tax19out.reload()
    >>> tax19out.amount
    Decimal('0.00')
    >>> base19in.reload()
    >>> base19in.amount
    Decimal('0.00')
    >>> tax19in.reload()
    >>> tax19in.amount
    Decimal('0.00')

Create a receivable batch line with a customer invoice::

    >>> customer_invoice1.account == receivable
    True
    >>> batch_line9 = BatchLine(journal=batch_journal,
    ...     batch=batch,
    ...     date=today,
    ...     account=cash,
    ...     invoice=customer_invoice1,
    ... )
    >>> batch_line9.save()
    >>> batch_line9.reload()
    >>> batch_line9.side_account
    'debit'
    >>> batch_line9.side_contra_account
    'credit'
    >>> batch_line9.contra_account == customer_invoice1.account
    True
    >>> batch_line9.amount == customer_invoice1.total_amount
    True
    >>> batch_line9.party == customer_invoice1.party
    True
    >>> batch.reload()
    >>> len(batch.lines)
    9
    >>> len(batch.move_lines)
    22
    >>> receivable.reload()
    >>> receivable.credit
    Decimal('150.00')
    >>> receivable.debit
    Decimal('250.00')
    >>> payable.reload()
    >>> payable.credit
    Decimal('50.00')
    >>> payable.debit
    Decimal('0.00')

    >>> revenue.reload()
    >>> revenue.credit
    Decimal('250.00')
    >>> revenue.debit
    Decimal('50.00')
    >>> expense.reload()
    >>> expense.credit
    Decimal('0.00')
    >>> expense.debit
    Decimal('50.00')

    >>> cash.reload()
    >>> cash.credit
    Decimal('0.00')
    >>> cash.debit
    Decimal('100.00')
    >>> base19out.reload()
    >>> base19out.amount
    Decimal('0.00')
    >>> tax19out.reload()
    >>> tax19out.amount
    Decimal('0.00')
    >>> base19in.reload()
    >>> base19in.amount
    Decimal('0.00')
    >>> tax19in.reload()
    >>> tax19in.amount
    Decimal('0.00')

Create another receivable batch line with a second customer invoice::

    >>> customer_invoice2.account == receivable
    True
    >>> batch_line10 = BatchLine(journal=batch_journal,
    ...     batch=batch,
    ...     date=today,
    ...     account=cash,
    ...     invoice=customer_invoice2,
    ... )
    >>> batch_line10.save()
    >>> batch_line10.reload()
    >>> batch_line10.side_account
    'debit'
    >>> batch_line10.side_contra_account
    'credit'
    >>> batch_line10.contra_account == customer_invoice2.account
    True
    >>> batch_line10.amount == customer_invoice2.total_amount
    True
    >>> batch_line10.party == customer_invoice2.party
    True
    >>> batch.reload()
    >>> len(batch.lines)
    10
    >>> len(batch.move_lines)
    24
    >>> receivable.reload()
    >>> receivable.credit
    Decimal('300.00')
    >>> receivable.debit
    Decimal('250.00')
    >>> payable.reload()
    >>> payable.credit
    Decimal('50.00')
    >>> payable.debit
    Decimal('0.00')

    >>> revenue.reload()
    >>> revenue.credit
    Decimal('250.00')
    >>> revenue.debit
    Decimal('50.00')
    >>> expense.reload()
    >>> expense.credit
    Decimal('0.00')
    >>> expense.debit
    Decimal('50.00')

    >>> cash.reload()
    >>> cash.credit
    Decimal('0.00')
    >>> cash.debit
    Decimal('250.00')
    >>> base19out.reload()
    >>> base19out.amount
    Decimal('0.00')
    >>> tax19out.reload()
    >>> tax19out.amount
    Decimal('0.00')
    >>> base19in.reload()
    >>> base19in.amount
    Decimal('0.00')
    >>> tax19in.reload()
    >>> tax19in.amount
    Decimal('0.00')

Create a receivable batch line with a customer credit note::

    >>> customer_credit_note.account == receivable
    True
    >>> batch_line11 = BatchLine(journal=batch_journal,
    ...     batch=batch,
    ...     date=today,
    ...     account=cash,
    ...     invoice=customer_credit_note,
    ... )
    >>> batch_line11.save()
    >>> batch_line11.reload()
    >>> batch_line11.side_account
    'credit'
    >>> batch_line11.side_contra_account
    'debit'
    >>> batch_line11.contra_account == customer_credit_note.account
    True
    >>> batch_line11.amount == customer_credit_note.total_amount
    True
    >>> batch_line11.party == customer_credit_note.party
    True
    >>> batch.reload()
    >>> len(batch.lines)
    11
    >>> len(batch.move_lines)
    26
    >>> receivable.reload()
    >>> receivable.credit
    Decimal('300.00')
    >>> receivable.debit
    Decimal('300.00')
    >>> payable.reload()
    >>> payable.credit
    Decimal('50.00')
    >>> payable.debit
    Decimal('0.00')

    >>> revenue.reload()
    >>> revenue.credit
    Decimal('250.00')
    >>> revenue.debit
    Decimal('50.00')
    >>> expense.reload()
    >>> expense.credit
    Decimal('0.00')
    >>> expense.debit
    Decimal('50.00')

    >>> cash.reload()
    >>> cash.credit
    Decimal('50.00')
    >>> cash.debit
    Decimal('250.00')
    >>> base19out.reload()
    >>> base19out.amount
    Decimal('0.00')
    >>> tax19out.reload()
    >>> tax19out.amount
    Decimal('0.00')
    >>> base19in.reload()
    >>> base19in.amount
    Decimal('0.00')
    >>> tax19in.reload()
    >>> tax19in.amount
    Decimal('0.00')

Create a payable batch line with a supplier invoice::

    >>> supplier_invoice.account == payable
    True
    >>> batch_line12 = BatchLine(journal=batch_journal,
    ...     batch=batch,
    ...     date=today,
    ...     account=cash,
    ...     invoice=supplier_invoice,
    ... )
    >>> batch_line12.save()
    >>> batch_line12.reload()
    >>> batch_line12.side_account
    'credit'
    >>> batch_line12.side_contra_account
    'debit'
    >>> batch_line12.contra_account == supplier_invoice.account
    True
    >>> batch_line12.amount == supplier_invoice.total_amount * -1
    True
    >>> batch_line12.party == supplier_invoice.party
    True
    >>> batch.reload()
    >>> len(batch.lines)
    12
    >>> len(batch.move_lines)
    28
    >>> receivable.reload()
    >>> receivable.credit
    Decimal('300.00')
    >>> receivable.debit
    Decimal('300.00')
    >>> payable.reload()
    >>> payable.credit
    Decimal('50.00')
    >>> payable.debit
    Decimal('50.00')

    >>> revenue.reload()
    >>> revenue.credit
    Decimal('250.00')
    >>> revenue.debit
    Decimal('50.00')
    >>> expense.reload()
    >>> expense.credit
    Decimal('0.00')
    >>> expense.debit
    Decimal('50.00')

    >>> cash.reload()
    >>> cash.credit
    Decimal('100.00')
    >>> cash.debit
    Decimal('250.00')
    >>> base19out.reload()
    >>> base19out.amount
    Decimal('0.00')
    >>> tax19out.reload()
    >>> tax19out.amount
    Decimal('0.00')
    >>> base19in.reload()
    >>> base19in.amount
    Decimal('0.00')
    >>> tax19in.reload()
    >>> tax19in.amount
    Decimal('0.00')

Post the batch::

    >>> Move = Model.get('account.move')
    >>> batch.click('close')
    >>> batch.state
    u'closed'
    >>> customer_invoice1.reload()
    >>> customer_invoice1.state
    u'paid'
    >>> customer_invoice2.reload()
    >>> customer_invoice2.state
    u'paid'
    >>> customer_credit_note.reload()
    >>> customer_credit_note.state
    u'paid'
    >>> supplier_invoice.reload()
    >>> supplier_invoice.state
    u'paid'
    >>> batch.reload()
    >>> (len([ml for ml in batch.move_lines if ml.move_state == 'posted'])
    ...       == len(batch.move_lines))
    True

Use the cancelation wizard to cancel some posted batch lines::

    >>> wizard_cancel = Wizard('account.batch.cancel',
    ...     [batch_line1, batch_line3, batch_line5, batch_line7])
    >>> wizard_cancel.form.description = 'Continue'
    >>> wizard_cancel.execute('cancelation')
    >>> wizard_cancel.state
    'end'
    >>> batch.reload()
    >>> len(batch.lines)
    16
    >>> len(batch.move_lines)
    38

    >>> receivable.reload()
    >>> receivable.credit
    Decimal('300.00')
    >>> receivable.debit
    Decimal('300.00')
    >>> payable.reload()
    >>> payable.credit
    Decimal('50.00')
    >>> payable.debit
    Decimal('50.00')

    >>> revenue.reload()
    >>> revenue.credit
    Decimal('-690.34')
    >>> revenue.debit
    Decimal('50.00')
    >>> expense.reload()
    >>> expense.credit
    Decimal('0.00')
    >>> expense.debit
    Decimal('-890.34')

    >>> cash.reload()
    >>> cash.credit
    Decimal('-1000.00')
    >>> cash.debit
    Decimal('-850.00')
    >>> base19out.reload()
    >>> base19out.amount
    Decimal('-840.34')
    >>> tax19out.reload()
    >>> tax19out.amount
    Decimal('-159.66')
    >>> base19in.reload()
    >>> base19in.amount
    Decimal('840.34')
    >>> tax19in.reload()
    >>> tax19in.amount
    Decimal('159.66')

