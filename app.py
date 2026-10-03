from typesafe_sdk import Choice, TypeSafeClient
import os
import time

# O ideal é configurar a JEV_API_KEY nas variáveis de ambiente. Fiz assim apenas
# para facilitar reprodutibilidade
os.environ["TYPESAFE_API_KEY"] = (
    "... incluir a sua JEV_API_KEY..."
)

client_problem_1 = """"
Subject: Urgent: Incorrect Order Received - Order #48291

Dear Customer Support Team,

I am writing to express my disappointment regarding order #48291, which I received earlier today.

Unfortunately, the items delivered do not match what I originally ordered. I had purchased a Navy 
Blue Wool Sweater (Size M), but instead, I received a Black Cotton Hoodie (Size L).

I have attached a photo of the item received, along with the packing slip from the box for your reference. 
Since this sweater was intended as a gift for an event this weekend, I would greatly appreciate it if you 
could prioritize resolving this issue.

Could you please send the correct item as soon as possible and provide instructions (along with a prepaid 
shipping label) on how to return the incorrect product?

Thank you for your prompt attention to this matter. I look forward to your quick response.

Best regards,

Alex Johnson

alex.johnson@email.com

(555) 019-2834
"""

after_sale_analyst_problem = """"
Guys, for the love of God, can someone from IT/Support take a look at our ticketing system? 
It's the third day in a row this has happened!

Every time I go to reply to a customer's email, right at the crucial moment, the screen just freezes. 
I do all the troubleshooting, pull up their history, type out a huge paragraph explaining their refund... 
and the second I click 'Send', the system dies. I just get that endless spinning wheel of death and nothing happens. 

The worst part is that the customer is already annoyed because their product arrived defective. 
My response SLA is breaching, flashing red in my face, and I can't get back to them. The guy has 
already messaged us on WhatsApp thinking we're ignoring his case!

So what do I have to do? Refresh the page. When it reloads, the system logs me out, I lose my entire draft, 
and I have to type it all out from scratch, praying it doesn't freeze again.

We keep talking in meetings about implementing AI, automation, and all that stuff, but the bare minimum—sending 
an after-sales email—isn't working. We're not going to retain any customers this way. Can someone save me, please? Is 
there a background update running, or is the server just giving up?
"""

after_sale = """"
Department Overview:

The After-Sales Support team is dedicated to customer retention, satisfaction, 
and issue resolution following a purchase. This department handles order discrepancies, 
returns, replacements, product troubleshooting, and ongoing customer feedback to ensure 
a seamless post-purchase experience.

Core Responsibilities:

Processing returns, exchanges, and refund requests.

Resolving customer complaints regarding defective or incorrect orders.

Gathering customer feedback to improve overall service quality.

Managing warranty claims and product support.
"""

finance = """"
Department Overview:

The Finance Department manages the organization's overall financial health, 
fiscal compliance, and capital allocation. This team oversees all monetary 
transactions—including revenue collection, vendor payments, and financial 
reporting—to ensure profitability and regulatory adherence.

Core Responsibilities:

Managing Accounts Payable (AP) and Accounts Receivable (AR).

Preparing financial statements, budgets, and cash flow forecasts.

Handling payroll, tax compliance, and auditing procedures.

Assessing financial risk and evaluating investment opportunities.
"""

tech = """"
Department Overview:

The Technology Department designs, maintains, and secures the company's digital 
infrastructure and software systems. This team ensures high availability of core tools, 
safeguards sensitive data, and integrates advanced AI or automation models to optimize 
operational efficiency across all business units.

Core Responsibilities:

Managing cloud infrastructure, servers, and network security.

Developing and maintaining internal software, APIs, and customer-facing platforms.

Providing technical support (help desk) for employee hardware and software.

Implementing data protection standards and cybersecurity protocols.
"""

start_time = time.time()

with TypeSafeClient() as client:
    response = client.system_one(
        state=after_sale_analyst_problem,
        questions={
            "dep": Choice(
                instructions="Which team should handle this?",
                criteria={
                    "tech": tech,
                    "finance": finance,
                    "after_sale": after_sale,
                },
            ),
        },
    )

    print(f"You need to talk with {response.answers["dep"].choice} team")


t = round((time.time() - start_time) * 1000, 2)
print(f"response in {t} ms")
