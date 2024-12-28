# import schedule
# import time
# import requests
# from AuthApp.models import DynamicControlScheduling

# import random
# import string

# def generate_random_string(length):
#     # Choose from letters and digits
#     characters = string.ascii_letters + string.digits
#     return ''.join(random.choice(characters) for _ in range(length))





# # Function that performs the task
# def hit_url_task():
#     obj = DynamicControlScheduling.objects.get(id = 1)
#     job_executed = obj.sw1
#     sks = obj.sks

#     if  job_executed == True:  
#         url = f'http://127.0.0.1:8000/referencerewd/{sks}/'          
#         requests.get(url)
#         obj.sks = generate_random_string(100)
#         obj.sw1 = False
#         obj.save()
#         obj.save()     


#     else:
#         url = f'http://127.0.0.1:8000/sent_reword/{sks}/'  
        
#         requests.get(url)
#         obj.sw1 = True
#         obj.save()

#         print("Task already executed , skipping...")

# # Schedule the task to run every minute



# schedule.every(10).minutes.do(hit_url_task)

# # Function to run the scheduler
# def run_schedule():
#     while True:
#         schedule.run_pending()  # Check for and run any pending jobs
#         time.sleep(1)  # Sleep for a short period to prevent busy waiting

