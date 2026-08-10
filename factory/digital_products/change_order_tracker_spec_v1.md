# Contractor Change Order & Scope Creep Tracker — Build Spec v1

## Workbook tabs
1. START HERE — workflow and assumptions.
2. JOBS — job ID, customer, original contract value, original estimated cost, original expected gross profit.
3. CHANGE ORDERS — change ID, job ID, request date, description, status, customer approval date, added labor hours, labor rate, added materials, subcontractors, other cost, total added cost, customer price adjustment, incremental gross profit, incremental margin, invoice status, payment status, notes.
4. DASHBOARD — total approved change-order revenue, total added cost, incremental gross profit, unpaid approved changes, pending changes, margin impact by job.

## Formula rules
- Total added cost = labor hours × labor rate + materials + subcontractors + other cost.
- Incremental gross profit = customer price adjustment − total added cost.
- Incremental margin = incremental gross profit / customer price adjustment when price adjustment > 0.
- Never count pending/unapproved changes as realized revenue.
- Never count unpaid customer adjustments as cash received.

## Fulfillment standard
The customer-facing workbook should contain formulas, example rows clearly marked as examples, frozen headers, filters, currency/percentage formatting, data validation for statuses, and no macros or external connections.

## Positioning
Operational planning and documentation template only. It is not a contract, legal advice, bookkeeping, accounting, tax, or financial advice.
