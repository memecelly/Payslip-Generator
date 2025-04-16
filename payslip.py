from fpdf import FPDF
import smtplib
import ssl
from email.message import EmailMessage
import os
import datetime

# Ensure the 'employee_payslips' folder exists
os.makedirs("employee_payslips", exist_ok=True)

# Create a subclass of FPDF to customize functionality
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Header: Example PDF', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

# Generate a sample PDF using the custom PDF class
def generate_sample_pdf():
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf.cell(0, 10, f'This PDF was created on: {current_date}', 0, 1)
    sample_path = 'employee_payslips/example.pdf'
    pdf.output(sample_path)
    print("Sample PDF generated successfully!")

# SimplePayslipGenerator creates payslip PDFs for employees
class SimplePayslipGenerator:
    def __init__(self):
        self.pdf = FPDF()

    def create_payslip(self, employee_data):
        date_str = datetime.datetime.now().strftime('%Y%m%d')
        sanitized_name = employee_data['name'].replace(" ", "_")
        filename = f"payslip_{sanitized_name}_{date_str}.pdf"
        full_path = os.path.join("employee_payslips", filename)

        # Add a new page and set the font
        self.pdf.add_page()
        self.pdf.set_font("Arial", size=15)

        # Company header
        self.pdf.cell(200, 10, txt="MayceeIT", ln=True, align='L')

        # Employee details
        self.pdf.cell(200, 10, txt=f"Employee: {employee_data['name']}", ln=True, align='L')
        self.pdf.cell(200, 10, txt=f"Date: {datetime.datetime.now().strftime('%d/%m/%Y')}", ln=True, align='L')

        # Earnings section
        self.pdf.set_font("Arial", style='B', size=12)
        self.pdf.cell(200, 10, txt="Earnings", ln=True, align='L')
        self.pdf.set_font("Arial", size=10)
        self.pdf.cell(200, 10, txt=f"Basic Salary: ${employee_data['basic_salary']}", ln=True, align='L')
        self.pdf.cell(200, 10, txt=f"Allowances: ${employee_data['allowances']}", ln=True, align='L')

        # Deductions section
        self.pdf.set_font("Arial", style='B', size=12)
        self.pdf.cell(200, 10, txt="Deductions", ln=True, align='L')
        self.pdf.set_font("Arial", size=10)
        self.pdf.cell(200, 10, txt=f"Deductions: ${employee_data['deductions']}", ln=True, align='L')

        # Net Pay
        net_pay = employee_data['basic_salary'] + employee_data['allowances'] - employee_data['deductions']
        self.pdf.set_font("Arial", style='B', size=12)
        self.pdf.cell(200, 10, txt="Net Pay", ln=True, align='L')
        self.pdf.set_font("Arial", size=10)
        self.pdf.cell(200, 10, txt=f"Net Pay: ${net_pay}", ln=True, align='L')

        # Save the PDF file and return the path
        self.pdf.output(full_path)
        print(f"Payslip saved as {full_path}")
        return full_path

# Function to send an email with the PDF attachment
def send_email_with_attachment(sender_email, receiver_email, password, subject, body, attachment_path):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.set_content(body)

    with open(attachment_path, 'rb') as f:
        file_data = f.read()
        file_name = os.path.basename(attachment_path)
        msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=file_name)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.login(sender_email, password)
        server.send_message(msg)
    print("Email sent successfully!")

# Example usage
if __name__ == "__main__":
    # Step 1: Generate a sample PDF
    generate_sample_pdf()

    # Step 2: Generate the payslip
    payslip_generator = SimplePayslipGenerator()
    sample_employee = {
        'name': 'Ellioth Tiringe',
        'basic_salary': 1600,
        'allowances': 300,
        'deductions': 150,
    }
    payslip_filename = payslip_generator.create_payslip(sample_employee)

    # Step 3: Email details
    sender_email = "tendaitasha557@gmail.com"
    receiver_email = "receiver@example.com"
    password = "lfcx efce vwis krpf"  # App-specific password
    subject = "Your Payslip"
    body = "Please find attached your payslip."

    # Step 4: Send the email with the payslip attached
    send_email_with_attachment(sender_email, receiver_email, password, subject, body, payslip_filename)
