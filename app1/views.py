from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse,JsonResponse
from .models import AmbulanceRequest, UserModel
from django.views.decorators.csrf import csrf_exempt

import json
from openai import OpenAI

def login(request):
    if request.method == 'POST':
        fin_cod = request.POST['fin_code']
        passwor = request.POST['password']
        print(fin_cod,passwor)
        # Retrieve the user with the given fin_code
        try:
            user = UserModel.objects.get(fin_code=fin_cod)
        except UserModel.DoesNotExist:
            user = None

        # Check +if the user exists and the password is correct
        if user.fin_code==fin_cod and user.password==passwor:
            # Log in the user manually
            request.session['fin_code'] = fin_cod
            return redirect('main')
        else:
            # If authentication fails, display an error message
            return render(request, 'login.html', {'error_message': 'Invalid fin code or password'})

    return render(request, 'login.html')

def main(request):
    # Access the authenticated user using request.user
    user = request.user
    # Your view logic here
    fin_code = request.session.get('fin_code', '')
    return render(request, 'index.html')


def ambulance(request):
    if request.method == 'POST':
        # Retrieve the authenticated user
        user = request.user
        fin_code = request.session.get('fin_code', '')
        records_to_delete = AmbulanceRequest.objects.filter(fin_code=fin_code)
    
        if records_to_delete.exists():
            # Delete the records
            records_to_delete.delete()
        name_data = UserModel.objects.filter(fin_code=fin_code).values('name').first()
        name = name_data['name']
        surname_data = UserModel.objects.filter(fin_code=fin_code).values('surname').first()
        surname = surname_data['surname']
        patrical_data = UserModel.objects.filter(fin_code=fin_code).values('patrical_name').first()
        patrical_name = patrical_data['patrical_name']
        # Retrieve other fields from the request
        # Create an AmbulanceRequest for the user
        ambulance_request = AmbulanceRequest.objects.create(
            fin_code=fin_code,
            name=name,
            surname=surname,
            patrical_name=patrical_name,
            sent=True,
        )

        # Redirect to a success page or any other page

    return JsonResponse({'fin_code':fin_code})




def get_sent_status(request):
    if request.method == 'POST':
        # Check if the content type is 'application/json'
        if request.content_type == 'application/json':
            try:
                # Load JSON data from the request body
                data = json.loads(request.body.decode('utf-8'))
                # Assuming the 'fin_code' parameter is present in the JSON data
                fin_code = data.get('fin_code')

                if fin_code is not None:
                    try:
                        # Retrieve the object based on the provided 'fin_code'
                        obj = AmbulanceRequest.objects.get(fin_code=fin_code)
                        # Get the value of the 'sent' field
                        sent_value = obj.sent

                        # Return the 'sent' field value as JSON
                        return JsonResponse({'sent': sent_value})
                    except AmbulanceRequest.DoesNotExist:
                        return JsonResponse({'error': 'Object not found'}, status=404)
                else:
                    return JsonResponse({'error': 'Missing "fin_code" parameter in JSON data'}, status=400)

            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        else:
            return JsonResponse({'error': 'Invalid content type'}, status=415)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
# Other views and functions...
def callers(request):
    sent_callers = AmbulanceRequest.objects.filter(sent=True)
    context = {'all_callers': sent_callers}
    return render(request, 'callers_template.html', context)

def update_sent(request, caller_id):
    caller = get_object_or_404(AmbulanceRequest, pk=caller_id)
    
    # Update the 'sent' field to False
    caller.sent = False
    caller.save()

    return redirect('callers')
def cancel(request):
    if request.method == 'POST':
        # Retrieve the authenticated user
        user = request.user
        fin_code = request.session.get('fin_code', '')
        ambulance_request = AmbulanceRequest.objects.get(fin_code=fin_code)

        # Update the 'sent' field to 0
        ambulance_request.sent = 0
        ambulance_request.save()
    return JsonResponse({"success":"Mission failed successfully!"})
    
api_key = 'Your AI key' #we used chatgpt 3.5 Turbo
client = OpenAI(api_key=api_key)
messages = [
        {"role": "system", "content": "You are a healthcare chatbot which gives medical assessment to people who have some symptoms.\
            Follow my instructions as precisely as possible. Everytime you recieve input about symptoms of a disease,\
            I want to guess what disease it is and output which doctor should patient visit. Use plain text.\
            Example: Found! Neurologist.\n\
             Do not ask questions that you already got answers! It is very strict rule   \
            Output must be just like that. Never use anything besides it.\
            Doctor speciality must only be one of these, if not tell releated one:['Allergist/immunologist', 'Anesthesiologist', 'Cardiologist', 'Dermatologist', 'Endocrinologist', 'Family physician', 'Gastroenterologist', 'Geneticist', 'Hematologist', 'Hospice and palliative medicine specialist', 'Immunologist', 'Infectious disease physician', 'Internal Medicine', 'Nephrologist', 'Neurologist', 'Obstetrician/gynecologist (OBGYNs)', 'Oncologist', 'Ophthalmologist', 'Orthopedist', 'Otolaryngologist', 'Osteopath', 'Pathologist', 'Pediatrician', 'Physician executive', 'Plastic surgeon', 'Podiatrist', 'Psychiatrist', 'Pulmonologist', 'Radiologist', 'Rheumatologist ', 'Sleep medicine specialist ', 'Surgeon', 'Urologist'] \
            Never go out of the structure of the example that I provided.\
            Never provide additional context.\
            However, if you are not quite sure about it, ask related questions around provided symptoms. Do not ask so many questions and do not ask the question that you already got response. After done with these questions, give your answer just like this: Found! Cardiologist. Do not use additional sentences or recommend anything, just type which doctor.\
            Example of the conversation for a specific condition :\n\
            User: I have headache\n\
            GPT: Can you please provide me with some additional information about your headache? Is it a dull or sharp pain? Is it localized or does it radiate to other areas? How long have you been experiencing the headache?\n\
            User: It is sharp pain. it radiates to other areas.\n\
            GPT: Found! Neurologist"
            }
        ]
@csrf_exempt  # For demonstration purposes; use proper CSRF protection in production
def chatbot_view(request):
    global messages
    if request.method == 'POST':
        # Assuming the content type is 'application/json'
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body.decode('utf-8'))
                user_input = data.get('user_input', '')
                print("User:", user_input)
                
                if user_input:
                    messages.append({"role": "user", "content": user_input})
                    message = [{"role": "user", "content": user_input}]

                    chat = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=messages
                    )

                    reply = chat.choices[0].message.content

                    if reply.split(" ")[0] == "Found!":
                        doc = ' '.join(reply.split(" ")[1:])
                        return JsonResponse({
                            'reply': f"You should visit {doc}",
                            'category': doc,
                        })

                    return JsonResponse({'reply': f"ChatBot: {reply}"})
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        else:
            return JsonResponse({'error': 'Invalid content type'}, status=415)

    return JsonResponse({'error': 'Invalid request'})

def UserProfile(request):
    fin_code = request.session.get('fin_code', '')
    name_data = UserModel.objects.filter(fin_code=fin_code).values('name').first()
    name = name_data['name']
    surname_data = UserModel.objects.filter(fin_code=fin_code).values('surname').first()
    surname = surname_data['surname']
    patrical_data = UserModel.objects.filter(fin_code=fin_code).values('patrical_name').first()
    patrical_name = patrical_data['patrical_name']
    return JsonResponse({
        'name':name,
        'surname':surname,
        'patrical_name':patrical_name,
        "fin_code":fin_code,
    })

def delete_history(request):
    global messages
    messages = [
        {"role": "system", "content": "You are a healthcare chatbot which gives medical assessment to people who have some symptoms.\
            Follow my instructions as precisely as possible. Everytime you recieve input about symptoms of a disease,\
            I want to guess what disease it is and output which doctor should patient visit. Use plain text.\
            Example: Found! Neurologist.\n\
            Do not ask questions that you already got answers! It is very strict rule   \
            Output must be just like that. Never use anything besides it.\
            Doctor speciality must only be one of these, if not tell releated one:['Allergist/immunologist', 'Anesthesiologist', 'Cardiologist', 'Dermatologist', 'Endocrinologist', 'Family physician', 'Gastroenterologist', 'Geneticist', 'Hematologist', 'Hospice and palliative medicine specialist', 'Immunologist', 'Infectious disease physician', 'Internal Medicine', 'Nephrologist', 'Neurologist', 'Obstetrician/gynecologist (OBGYNs)', 'Oncologist', 'Ophthalmologist', 'Orthopedist', 'Otolaryngologist', 'Osteopath', 'Pathologist', 'Pediatrician', 'Physician executive', 'Plastic surgeon', 'Podiatrist', 'Psychiatrist', 'Pulmonologist', 'Radiologist', 'Rheumatologist ', 'Sleep medicine specialist ', 'Surgeon', 'Urologist'] \
            Never go out of the structure of the example that I provided.\
            Never provide additional context.\
            However, if you are not quite sure about it, ask related questions around provided symptoms. Do not ask so many questions and do not ask the question that you already got response. After done with these questions, give your answer just like this: Found! Cardiologist. Do not use additional sentences or recommend anything, just type which doctor.\
            Example of the conversation for a specific condition :\n\
            User: I have headache\n\
            GPT: Can you please provide me with some additional information about your headache? Is it a dull or sharp pain? Is it localized or does it radiate to other areas? How long have you been experiencing the headache?\n\
            User: It is sharp pain. it radiates to other areas.\n\
            GPT: Found! Neurologist"
            }
        ]
    return JsonResponse({"Response":"History deleted!"})