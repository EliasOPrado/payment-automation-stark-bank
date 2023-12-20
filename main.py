import time
import schedule
import random
from connection import starkbank
from fake_data import generate_random_invoice
from starkcore.error import InputErrors, InternalServerError
from datetime import datetime, timedelta

class InvoiceScheduler:
    # Transfers money for a single invoice if it's marked as paid and not yet transferred
    def transfer_single_invoice(self, invoice):
        # Retrieves recent transfers
        transfers = starkbank.transfer.query(
            after=datetime.now() - timedelta(days=3),
            before=datetime.now() + timedelta(hours=random.randint(1, 24)),
        )

        # Checks if the invoice is not paid, exits the function if it's unpaid
        if invoice.status != "paid":
            return

        # Checks if the invoice is already paid via a transfer
        is_invoice_paid = any(
            invoice.id in transfer.description for transfer in transfers
        )

        # Initiates a transfer if the invoice is paid but not yet transferred
        if not is_invoice_paid:
            first_name = invoice.name.split()[0] if invoice.name else "Unknown"
            new_transfer = starkbank.Transfer(
                amount=invoice.amount,
                tax_id="20.018.183/0001-80",
                name="Stark Bank S.A.",
                bank_code="20018183",
                branch_code="0001",
                account_number="6341320293482496",
                account_type="payment",
                tags=[first_name, f"invoice/{invoice.id}"],
                description=f"Payment for invoice {invoice.id}",
                fee=invoice.fee,
            )
            transfer = starkbank.transfer.create([new_transfer])
            print(f"Transfer {transfer} sent.")

    # Transfers money for a batch of invoices
    def transfer_batch_invoices(self):
        # Retrieves invoices within a specific time frame
        invoices = starkbank.invoice.query(
            after=datetime.now() - timedelta(days=3),
            before=datetime.now() + timedelta(hours=random.randint(1, 24)),
        )

        # Processes each invoice for transfer
        for invoice in invoices:
            self.transfer_single_invoice(invoice)

    # Schedules invoice creation at random intervals
    def schedule_invoices(self):
        interval_seconds = random.uniform(15, 22.5) * 60
        interval_minutes = round(interval_seconds / 60)
        print(f"Scheduled invoice after {interval_minutes} minutes approximately")

        try:
            invoice = starkbank.invoice.create([generate_random_invoice()])
            print(invoice)
        except InputErrors as e:
            print(f"Input error: {e}. Generating a new invoice.")
        except InternalServerError:
            print("Internal Server Error. Waiting for 60 seconds.")
            time.sleep(60)

        time.sleep(interval_seconds)

    # Runs the entire scheduler
    def run_scheduler(self):
        # Schedules batch invoice transfers to run every 3 hours
        schedule.every(10800).seconds.do(self.transfer_batch_invoices)

        # Main loop that handles scheduling invoice creation and batch transfers
        while True:
            self.schedule_invoices()
            schedule.run_pending()
            time.sleep(1)

if __name__ == "__main__":
    # Initialize and run the scheduler
    scheduler = InvoiceScheduler()
    scheduler.run_scheduler()