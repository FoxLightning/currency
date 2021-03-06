from io import BytesIO

from account.models import User

from django.core.mail import EmailMessage

from rate.models import Rate, Subscription

import xlwt


def display(obj, attr: str) -> str:
    get_display = f'get_{attr}_display'

    if hasattr(obj, get_display):
        return getattr(obj, get_display)()

    return str(getattr(obj, attr))


def last_rates() -> list:
    """
    Return all last rates of all banks and currency
    """
    query = Rate.objects.raw(
        """
        SELECT
            r.id,
            r.source,
            r.currency,
            r.buy,
            r.sale,
            r.created
        FROM
            rate_rate AS r INNER JOIN (
                SELECT
                    source,
                    currency,
                    MAX(created) as created
                FROM
                    rate_rate
                GROUP BY
                    source,
                    currency
            ) as q
            ON r.source = q.source
            AND r.currency = q.currency
            AND r.created = q.created
        """
    )
    return list(query)


def user_rates(user) -> list:
    """
    Return last rates for banks in subscription of chosen user
    """
    query_sources = Subscription.objects.filter(user=user).only('banks')
    user_sources = [i.banks for i in query_sources]
    user_rates = [i for i in filter(lambda x: x.source in user_sources, last_rates())]
    return user_rates


def create_xml(query):
    """
    Create xml from queryset, include all fields in models
    """
    xmlfile = BytesIO()
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Rates')

    fields = [i for i in Rate._meta.fields]

    for col, field in enumerate(fields):
        ws.write(0, col, field.verbose_name)

    # write name if field
    for row, cortege in enumerate(query, 1):
        for col, field in enumerate(fields):
            ws.write(row, col, display(cortege, field.name))
    wb.save(xmlfile)
    return xmlfile


def send_user_by_xml(user):
    """
    sand email and attach xml file
    """
    excelfile = create_xml(user_rates(user))
    # send email
    email = EmailMessage()
    email.subject = 'Currency rates'
    email.body = 'Last currency rates'
    email.from_email = 'battlefieldblo@gmail.com'
    email.to = [user.email]
    email.attach('Currency_rates.xls', excelfile.getvalue(), 'application/ms-excel')
    email.send()


def send_xml_to_all():
    for user in User.objects.all().iterator():
        send_user_by_xml(user)
