from django.shortcuts import render, reverse, redirect
from django.views import View
from django.views.generic import ListView
from django.core.mail import send_mail, EmailMultiAlternatives, mail_admins
from datetime import datetime
from django.template.loader import render_to_string

from .models import Appointment


class AppointmentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'make_appointment.html', {})

    def post(self, request, *args, **kwargs):
        appointment = Appointment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
        )

        appointment.save()

        # Тут 3-варианта

        # отправляем письмо
        send_mail(
            subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',
            # имя клиента и дата записи будут в теме для удобства
            message=appointment.message,  # сообщение с кратким описанием проблемы
            from_email='imaraliev.kg2005@yandex.ru',  # здесь указываете почту, с которой будете отправлять (об этом попозже)
            recipient_list=['asadullahgits@gmail.com']  # здесь список получателей. Например, секретарь, сам врач и т. д.
        )

        # # Получаем наш html
        # html_content = render_to_string(
        #     'appointment_created.html',
        #     {
        #         'appointment': appointment,
        #     }
        # )
        #
        # # в конструкторе уже знакомые нам параметры, да? Называются правда немного по-другому, но суть та же.
        # msg = EmailMultiAlternatives(
        #     subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',
        #     body=appointment.message,  # это то же, что и message
        #     from_email='imaraliev.kg2005@yandex.com',
        #     to=['asadullahgits@gmail.com']  # это то же, что и recipients_list
        # )
        # msg.send()  # отсылаем
        #
        # # отправляем письмо всем админам по аналогии с send_mail, только здесь получателя указывать не надо
        # mail_admins(
        #     subject=f'{appointment.client_name} {appointment.date.strftime("%d %m %Y")}',
        #     message=appointment.message,
        # )
        return redirect('appointments:make_appointment')


# class AppointmentDefaultView(ListView):
#     model = Appointment
#     context_object_name = 'list'
#     template_name = 'register/default.html'
#     paginate_by = 2