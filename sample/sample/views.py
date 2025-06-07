from django.http import HttpResponse,JsonResponse
from .models import Booking,Class,User,TimeZone
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def bookClass(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required'}, status=400)

    try:
        data = json.loads(request.body)
        class_id = data.get('class_id')
        user_id = data.get('user_id')
    except Exception:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    if not class_id or not user_id:
        return JsonResponse({'error': 'class_id and user_id are required'}, status=400)

    # Validate class exists
    try:
        cls = Class.objects.get(class_id=class_id)
    except Class.DoesNotExist:
        return JsonResponse({'error': 'Class not found'}, status=404)

    # Validate user exists
    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    # Check if user already booked the class
    if Booking.objects.filter(user_id=user, class_id=cls).exists():
        return JsonResponse({'error': 'User already booked this class'}, status=400)

    # Check if slots available
    if cls.no_of_slots <= 0:
        return JsonResponse({'error': 'No slots available'}, status=400)

    # Create booking
    Booking.objects.create(user_id=user, class_id=cls)

    # Reduce slot count and save
    cls.no_of_slots -= 1
    cls.save()

    return JsonResponse({'message': 'Booking successful', 'remaining_slots': cls.no_of_slots})

def home(request):
    return HttpResponse("Hello from APP1!")
def getClasses(request):
    classes = Class.objects.all()
    data = []

    for cls in classes:
        data.append({
            'class_id': cls.class_id,
            'class_name': cls.class_name,
            'instructor': cls.instructor,
            'date_time': cls.date_time,
            'no_of_slots': cls.no_of_slots,
            'time_zone': cls.time_zone_id.time_zone_name if cls.time_zone_id else None,
        })

    return JsonResponse({'classes': data}) 

def getUsers(request):
    users = User.objects.all()
    data = []
    for user in users:
        data.append({
            'user_id': user.user_id,
            'user_name': user.user_name,
            'user_email': user.user_email,
            'time_zone': user.time_zone_id.time_zone_name if user.time_zone_id else None,
        })
    return JsonResponse({'users': data})

def getTimeZones(request):
    timezones = TimeZone.objects.all()
    data = []
    for tz in timezones:
        data.append({
            'time_zone_id': tz.time_zone_id,
            'time_zone_name': tz.time_zone_name,
        })
    return JsonResponse({'timezones': data})

@csrf_exempt
def book(request):
    if request.method == 'POST':
        return bookClass(request)
    elif request.method == 'GET':
        return getBookings(request)
    else:
        return JsonResponse({'error': 'request method not supported'}, status=400)

import pytz
from datetime import datetime       
def getBookings(request):
    user_id = request.GET.get('user_id')

    if not user_id or not str(user_id).strip():
        return JsonResponse({'error': 'user_id is required'}, status=400)

    try:
        user = User.objects.get(user_id=int(user_id))
    except (User.DoesNotExist, ValueError):
        return JsonResponse({'error': 'Invalid user_id'}, status=404)

    bookings = Booking.objects.filter(user_id=user)
    data = []

    for booking in bookings:
        class_obj = booking.class_id
        timezone_str = class_obj.time_zone_id.time_zone_name

        # Convert epoch to datetime in specified timezone
        try:
            tz = pytz.timezone(timezone_str)
        except pytz.UnknownTimeZoneError:
            tz = pytz.utc

        class_datetime = datetime.fromtimestamp(class_obj.date_time, tz)
        formatted_time = class_datetime.strftime('%Y-%m-%d %H:%M:%S %Z')

        data.append({
            'booking_id': booking.booking_id,
            'user_id': booking.user_id.user_id,
            'user_name': booking.user_id.user_name,
            'class_id': class_obj.class_id,
            'class_name': class_obj.class_name,
            'class_time': formatted_time,
        })

    return JsonResponse({'bookings': data})

def populate(request):
    Booking.objects.all().delete()
    Class.objects.all().delete()
    User.objects.all().delete()
    TimeZone.objects.all().delete()

    tz1 = TimeZone.objects.create(time_zone_name='Asia/Kolkata')
    tz2 = TimeZone.objects.create(time_zone_name='America/New_York')

    user1 = User.objects.create(user_name='Alice', user_email='alice@example.com')
    user2 = User.objects.create(user_name='Bob', user_email='bob@example.com')

    import time
    now_epoch = int(time.time())
    class1 = Class.objects.create(class_name='Yoga Basics', instructor='John Doe', date_time=now_epoch, no_of_slots=5, time_zone_id=tz1)
    class2 = Class.objects.create(class_name='Advanced Pilates', instructor='Jane Smith', date_time=now_epoch, no_of_slots=2, time_zone_id=tz2)
    class3 = Class.objects.create(class_name='HIIT Training', instructor='Mike Lee', date_time=now_epoch, no_of_slots=3, time_zone_id=tz1)

    Booking.objects.create(user_id=user1, class_id=class1)
    Booking.objects.create(user_id=user1, class_id=class2)
    Booking.objects.create(user_id=user2, class_id=class1)
    Booking.objects.create(user_id=user2, class_id=class3)
    Booking.objects.create(user_id=user1, class_id=class3)

    print("Database populated successfully!")