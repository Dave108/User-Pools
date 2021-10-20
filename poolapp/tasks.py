from celery import shared_task


@shared_task(bind=True)
def testing_func(self):
    # operation to perform
    for i in range(1, 21):
        print(i, '----------')
    return "SUCCESS"


@shared_task(bind=True)
def time_over(self):
    # operation to perform
    print("from non scheduled celery")
    return "CELERY SUCCESS mail sent--"
