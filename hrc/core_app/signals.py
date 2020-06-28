# from datetime import datetime
# from django.db.models.signals import post_save, pre_save
# from django.dispatch import receiver
# from django.core.mail import EmailMessage
#
# from .models import Category, CoreUser
#
#
# @receiver(post_save, sender=Category)
# def sm_category_create_or_update(sender, created, **kwargs):
#     # Send mail to all users if category created
#     instance = kwargs['instance']
#     subject = ''
#     for item in CoreUser.objects.all():
#         to_email = item.email
#         html_content = f'<p><i>Здравствуйте {item.username}</i></p>'
#         if created and instance:
#             subject += f'@HCL mailer -> new category "{instance.category_short_name}" created - {datetime.now()}'
#             html_content += f'Создана новая категория {instance.category_short_name}: ' \
#                             f'<a href="/category_detail/{instance.category_short_name}/"</a>'
#         elif not created and instance:
#             subject += f'@HCL mailer -> category "{instance.category_short_name}" updated - {datetime.now()}'
#             html_content += f'Обновлена категория {instance.category_short_name}: ' \
#                             f'<a href="/category_detail/{instance.category_short_name}/"</a>'
#         html_content += '<p><i>Всего доброго.</i></p>'
#         from_email = 'robot@hcl.hansa.ru'
#         message = EmailMessage(subject, html_content, from_email, [to_email])
#         message.content_subtype = "html"
#         message.send()
