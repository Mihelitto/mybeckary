from mybeckary.celery import app
from django.core.mail import send_mail
from .models import Order

@app.task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    print('******',order)
    subject = 'Order nr. {}'.format(order_id)
    message = 'Dear {},\n\nYou have successfully placed an order.\
                    Your order id is {}.'.format(order.first_name, order.id)
    mail_sent = send_mail(subject,message,'admin@admin.com',[order.email])
    print('******', mail_sent)
    return mail_sent