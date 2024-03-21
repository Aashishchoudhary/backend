from .serializer import LibrarySerializer, LibrarySeatSerializer, SeatResSerializer, DelteHistorySerializer, HalfTimerSerlizer, ExtraStudentSerailzer, AmountCollectionSerailzer
from .models import Library, LibrarySeat, SeatReservation, DeletedHistory, HalfTimer, ExtraStudent, AmountCollection
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from datetime import datetime, date
from subscription.subscription_check import check_subscription
from dateutil.relativedelta import relativedelta
from .nearBy import find_nearby_library
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import render
from django.contrib.auth import get_user_model
User = get_user_model()
# from rest_framework.parsers import FileUploadParser


# # # view for nearby library

class NearByLibrary(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        lat = request.data.get('lat')
        lon = request.data.get('lon')
        distance = int(request.data.get('dis'))
        if lat is None or lon is None:
            return Response({'error': 'Latitude and longitude parameters are required.'}, status=400)

        Library = Library.objects.all()
        nearby_Library = []

        for lib in Library:
            lib_lat = lib.latitude
            lib_lon = lib.longitude
            coordinates = [(lib_lat, lib_lon)]  # Create a list of coordinates
            # Convert lat and lon to floats
            if find_nearby_library(float(lat), float(lon), coordinates, distance):
                nearby_Library.append(lib)

        serializer = LibrarySerializer(nearby_Library, many=True)
        return Response(serializer.data)


# add Library


class AddLibrary(APIView):

    permission_classes = [IsAuthenticated ,check_subscription]

    def get(self, request):
        owner = self.request.user
        lib = Library.objects.filter(owner=owner.id).count()
        # ser = LibrarySerializer(lib , many= True)
        return Response({'count': lib})

    def post(self, request):
        owner = self.request.user
        lib = Library.objects.filter(owner=owner.id).count()
        if lib < 5:

            data = {
                "owner": owner.id,
                "name": request.data.get('name'),
                "facilty": request.data.get('facilty'),
                "locality": request.data.get('locality'),
                "city": request.data.get('city'),
                "district": request.data.get('district'),
                "pincode": request.data.get('pincode'),
                "imageOne": request.data.get('imageOne'),
                "imageTwo": request.data.get('imageTwo'),
                "imageThree": request.data.get('imageThree'),
                "imageFour": request.data.get('imageFour'),
                "imageFive": request.data.get('imageFive'),
                "imageSix": request.data.get('imageSix'),
                "imageSeven": request.data.get('imageSeven'),
                "price": request.data.get('price'),
                "mobile_number": request.data.get('mobile_number'),
                "whatsapp_number": request.data.get('whatsapp_number'),
                "longitude": request.data.get('longitude'),
                "latitude": request.data.get('latitude'),
                "total_seat": request.data.get('total_seat'),
            }

            ser = LibrarySerializer(data=data)
            if ser.is_valid():
                ser.save()
                return Response(ser.data, status=status.HTTP_201_CREATED)
            return Response(ser.error_messages, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"deatils":"canot add more libraries , contact to help center"} ,status=400)


#
class LibView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        user = request.user
        print(user.id)
        lib = Library.objects.filter(owner_id=user.id)
        lib_serlizer = LibrarySerializer(lib, many=True)
        return Response(lib_serlizer.data)
# view your library


class LibraryView(APIView):
    permission_classes = [IsAuthenticated, check_subscription]

    def get(self, request, id):
        user = request.user
        lib = Library.objects.filter(owner_id=user.id, id=id)
        lib_serlizer = LibrarySerializer(lib, many=True)
        print(lib_serlizer.data)
        return Response(lib_serlizer.data)

    def patch(self, request, id):
        user = request.user
        lib = Library.objects.get(owner_id=user.id, id=id)

        ser = LibrarySerializer(lib, data=request.data, partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=200)

        return Response(ser.errors, status=400)

    def delete(self, request, id):
        owner = request.user

        lib = Library.objects.filter(owner_id=owner.id, id=id)
        lib.delete()
        return Response({'msg': "delted"}, status=200)


# add seats in library

class AddSeat(APIView):
    permission_classes = [IsAuthenticated, check_subscription]

    def get(self, request, id):
        user = request.user
        lib = Library.objects.filter(owner_id=user.id, id=id)
        ser = LibrarySerializer(lib, many=True)
        libid = ser.data[0]['id']

        seat = LibrarySeat.objects.filter(lib=libid)
        seatser = LibrarySeatSerializer(seat, many=True)
        data = {'library_name': ser.data[0]['name'], 'data': seatser.data}
        return Response(data)

    def post(self, request, id):
        user = request.user.id

        lib = Library.objects.filter(owner_id=user, id=id)
        ser = LibrarySerializer(lib, many=True)
        libid = ser.data[0]['id']
        seat2 = LibrarySeat.objects.filter(lib=libid)
        sea = LibrarySeatSerializer(seat2, many=True)
        data = {

            "lib": libid,
            "seat_num": sea.data[-1]['seat_num']+1,
            "booked": False
        }

        seatser = LibrarySeatSerializer(data=data)
        if seatser.is_valid():
            seatser.save()
            return Response(seatser.data)
        return Response(seatser.errors)


# library seat view

class LibSeatView(APIView):
    permission_classes = [IsAuthenticated, check_subscription]

    def get(self, request, id):
        user = request.user
        lib = Library.objects.filter(owner_id=user, id=id)
        lib_serlizer = LibrarySerializer(lib, many=True)
        libid = lib_serlizer.data[0]['id']
        name = lib_serlizer.data[0]['name']
        total_seat = lib_serlizer.data[0]['total_seat']
        seat = LibrarySeat.objects.filter(lib_id=libid)
        seat_serlizer = LibrarySeatSerializer(seat, many=True)
        response_data = {
            'name': name,
            'total_seat': total_seat,
            'data': seat_serlizer.data}
        return Response(response_data)


# add resvartion

class SeatResView(APIView):
    permission_classes = [IsAuthenticated, check_subscription]

    def get(self, request, lib_id, id):
        try:
            user = request.user
            lib = Library.objects.filter(owner_id=user, id=lib_id)
            lib_serlizer = LibrarySerializer(lib, many=True)
            libid = lib_serlizer.data[0]['id']
            name = lib_serlizer.data[0]['name']
            seat = LibrarySeat.objects.filter(lib_id=libid, seat_num=id)
            seat_serlizer = LibrarySeatSerializer(seat, many=True)
            seatid = seat_serlizer.data[0]['id']

            res = SeatReservation.objects.filter(reserved_seat_id=seatid)
            reser = SeatResSerializer(res, many=True)
            response_data = {
                'library_name': name,
                'seat_num': id,
                'mobile_number': lib_serlizer.data[0]['mobile_number'],
                'seat_data': reser.data
            }
            return Response(response_data, status=200)
        except:
            return Response({'details': "error occured"}, status=400)

    def post(self, request, lib_id, id):
        seat = LibrarySeat.objects.filter(lib_id=lib_id, seat_num=id)
        seat_serlizer = LibrarySeatSerializer(seat, many=True)
        seatid = seat_serlizer.data[0]['id']
        print(seatid)
        data = {
            "reserved_seat": seatid,
            "name": request.data.get('name'),
            "amount": request.data.get('amount'),
            'mobile_number': request.data.get('mobile_number'),
            'start_date': request.data.get('start_date'),
            'end_date': request.data.get('end_date'),
            'adharcard': request.data.get('adharcard'),
            'photo': request.data.get('photo'),
            'adress': request.data.get('adress'),
            'gender': request.data.get('gender'),
            'dob': request.data.get('dob')
        }
        print(data)
        ser=SeatResSerializer(data=data)
        if ser.is_valid():
            ser.save()
            print(ser.data)
            return Response(ser.data)
        return Response(ser.errors)
        # data_save = SeatReservation(**data)
        # data_save.save()
        # return Response({"data": "data saved"})

    def patch(self, request, lib_id, id):
        lib = Library.objects.filter(id=lib_id)
        lib_serlizer = LibrarySerializer(lib, many=True)
        libid = lib_serlizer.data[0]['id']
        seat = LibrarySeat.objects.filter(lib_id=libid, seat_num=id)
        seat_serlizer = LibrarySeatSerializer(seat, many=True)
        seatid = seat_serlizer.data[0]['id']

        res = SeatReservation.objects.get(reserved_seat_id=seatid)

        reser = SeatResSerializer(
            instance=res, data=request.data, partial=True)
        if reser.is_valid():
            reser.save()
            return Response(reser.data, status=200)

        return Response(reser.errors, status=400)

    def delete(self, request, lib_id, id):
        lib = Library.objects.filter(id=lib_id)
        lib_serlizer = LibrarySerializer(lib, many=True)
        libid = lib_serlizer.data[0]['id']
        seat = LibrarySeat.objects.filter(lib_id=libid, seat_num=id)
        seat_serlizer = LibrarySeatSerializer(seat, many=True)
        seatid = seat_serlizer.data[0]['id']
        res = SeatReservation.objects.get(reserved_seat_id=seatid)
        res.delete()
        return Response(status=200)


# Previous user

class PreviousUser(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id):
        user = request.user
        lib = DeletedHistory.objects.filter(owner=id)
        lib_serlizer = DelteHistorySerializer(lib, many=True)
        return Response(lib_serlizer.data)


class PreviousStu(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id, idt):
        user = request.user
        lib = DeletedHistory.objects.filter(owner=id, id=idt)
        lib_serlizer = DelteHistorySerializer(lib, many=True)
        return Response(lib_serlizer.data)

# view for half day students


class HalfTimerView(APIView):
    permission_classes = [IsAuthenticated, check_subscription]

    def get(self, request, id):
        user = request.user

        lib = Library.objects.filter(owner_id=user.id, id=id)
        lib_serlizer = LibrarySerializer(lib, many=True)
        libid = lib_serlizer.data[0]['id']
        print(libid)
        half = HalfTimer.objects.filter(lib_name_id=libid)
        halfs = HalfTimerSerlizer(half, many=True)
        return Response(halfs.data)

    def post(self, request, id):
        user = request.user
        lib = Library.objects.filter(owner_id=user.id, id=id)
        lib_serlizer = LibrarySerializer(lib, many=True)
        libid = lib_serlizer.data[0]['id']
        if lib.count()<25:
            data = {'lib_name': libid, "name": request.data.get('name'),
                    "amount": request.data.get('amount'),
                    'mobile_number': request.data.get('mobile_number'),
                    'start_date': request.data.get('start_date'),
                    'end_date': request.data.get('end_date'),
                    'adharcard': request.data.get('adharcard'),
                    'photo': request.data.get('photo'),
                    'adress': request.data.get('adress'),
                    'gender': request.data.get('gender'),
                    'dob': request.data.get('dob')
                    }
            ser = HalfTimerSerlizer(data=data)
            if ser.is_valid():
                ser.save()
                return Response(ser.data)
            return Response(ser.errors)
        return Response({'details':"can not add more than 25"})


# view to add extra students

class ExtraTimerView(APIView):
    permission_classes = [IsAuthenticated, check_subscription]

    def get(self, request, id):
        user = request.user
        lib = Library.objects.filter(owner_id=user.id, id=id)
        lib_serlizer = LibrarySerializer(lib, many=True)
        libid = lib_serlizer.data[0]['id']
        print(libid)
        half = ExtraStudent.objects.filter(lib_id=libid)
        half_serlizer = ExtraStudentSerailzer(half, many=True)
        return Response(half_serlizer.data)

    def post(self, request, id):
        user = request.user
        lib = Library.objects.filter(owner_id=user.id, id=id)
        lib_serlizer = LibrarySerializer(lib, many=True)
        libid = lib_serlizer.data[0]['id']
        if lib.count()<25:
            data = {'lib': libid, "name": request.data.get('name'),
                    "amount": request.data.get('amount'),
                    'mobile_number': request.data.get('mobile_number'),
                    'start_date': request.data.get('start_date'),
                    'end_date': request.data.get('end_date'),
                    'adharcard': request.data.get('adharcard'),
                    'photo': request.data.get('photo'),
                    'adress': request.data.get('adress'),
                    'gender': request.data.get('gender'),
                    'dob': request.data.get('dob')}
            ser = ExtraStudentSerailzer(data=data)
            if ser.is_valid():
                ser.save()
                return Response(ser.data, status=200)
            return Response(ser.errors, status=400)
        return Response({'details':"can not add more than 25"})


# delete view for half timer

class HalfTimerDelte(APIView):
    permission_classes = [IsAuthenticated, check_subscription]

    def get(self, request, id):
        user = request.user
        lib = Library.objects.filter(owner_id=user.id)
        lib_serlizer = LibrarySerializer(lib, many=True)
        libid = lib_serlizer.data[0]['id']
        libname = lib_serlizer.data[0]['name']
        mob = lib_serlizer.data[0]['mobile_number']
        lib = HalfTimer.objects.filter(lib_name=libid, id=id)
        ser = HalfTimerSerlizer(lib, many=True)
        data = {'library_name': libname,
                "data": ser.data, "mobile_number": mob}
        return Response(data)

    def delete(self, request, id):
        user = request.user
        lib = Library.objects.filter(owner_id=user.id)
        lib_serlizer = LibrarySerializer(lib, many=True)
        libid = lib_serlizer.data[0]['id']
        lib = HalfTimer.objects.filter(lib_name=libid, id=id)
        lib.delete()
        return Response(status=200)

    def patch(self , request, id):
        user= request.user
        lib=Library.objects.filter(owner_id=user.id ) 
        libt=LibrarySerializer(lib , many=True)
        libid=libt.data[0]['id']
        half=HalfTimer.objects.get(lib_name=libid , id =id)
        
        ser=HalfTimerSerlizer(half ,data=request.data , partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data ,status=200)
        return Response(ser.errors ,status=400)

# extra student delete

class ExtraStudentDelte(APIView):
    permission_classes = [IsAuthenticated, check_subscription]

    def get(self, request, id):
        user = request.user
        lib = Library.objects.filter(owner_id=user.id)
        lib_serlizer = LibrarySerializer(lib, many=True)
        libid = lib_serlizer.data[0]['id']
        libname = lib_serlizer.data[0]['name']
        half = ExtraStudent.objects.filter(lib_id=libid, id=id)
        ser = ExtraStudentSerailzer(half, many=True)
        data = {'library_name': libname, "data": ser.data,
                'mobile_number': lib_serlizer.data[0]['mobile_number']}
        return Response(data)

    def delete(self, request, id):
        user = request.user
        lib = Library.objects.filter(owner_id=user.id)
        lib_serlizer = LibrarySerializer(lib, many=True)
        libid = lib_serlizer.data[0]['id']
        print(libid)
        half = ExtraStudent.objects.filter(lib_id=libid, id=id)
        half.delete()
        return Response(status=200)

    def patch(self, request, id):
        user=request.user
        lib=Library.objects.filter(owner_id=user.id )
        lib_serlizer=LibrarySerializer(lib , many=True)
        libid=lib_serlizer.data[0]['id']
        print(libid)
        half=ExtraStudent.objects.get(lib_id=libid ,id=id)
        ser=ExtraStudentSerailzer(half ,data=request.data , partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)
       


class allReservation(APIView):
    permission_classes = [IsAuthenticated, check_subscription]

    def get(self, request, id):
        user = request.user
        lib = Library.objects.filter(owner_id=user.id, id=id)
        lib_serlizer = LibrarySerializer(lib, many=True)
        libid = lib_serlizer.data[0]['id']

        seat = LibrarySeat.objects.filter(lib_id=libid)
        seat_serlizer = LibrarySeatSerializer(seat, many=True)
        # print((seat_serlizer.data[0]['id']))
        # return Response(seat_serlizer.data)
        result = []
        for x in range(len(seat_serlizer.data)):

            seat = LibrarySeat.objects.filter(lib_id=libid, seat_num=x+1)
            sersea = LibrarySeatSerializer(seat, many=True)
            res = SeatReservation.objects.filter(
                reserved_seat_id=sersea.data[0]['id'])
            ser = SeatResSerializer(res, many=True)
            data = {"seat_num": x+1, 'data': ser.data, 'ser': sersea.data}
            result.append(data)
        return Response(result)


class AddRes(APIView):
    permission_classes = [IsAuthenticated, check_subscription]

    def get(self, request, id):
        user = request.user
        res = LibrarySeat.objects.filter(id=id)
        ser = LibrarySeatSerializer(res, many=True)
        libid = Library.objects.filter(id=ser.data[0]['lib'])
        serlibid = LibrarySerializer(libid, many=True)
        if (user.id == serlibid.data[0]['owner']):
            seres = SeatReservation.objects.filter(
                reserved_seat_id=ser.data[0]['id'])
            reser = SeatResSerializer(seres, many=True)
            data = {'library_name': serlibid.data[0]['name'], "data": reser.data,
                    "mobile_number": serlibid.data[0]['mobile_number']}
            return Response(data, status=200)

    def post(self, request , id):
        user = request.user
        res=LibrarySeat.objects.filter(id=id)
        ser = LibrarySeatSerializer(res ,many=True)
        libid=Library.objects.filter(id=ser.data[0]['lib'])
        serlibid=LibrarySerializer(libid ,many=True)
        print(serlibid.data[0]['owner'])
        print(user.id)
        if(user.id==serlibid.data[0]['owner']):
            data={
            "reserved_seat":ser.data[0]['id'],
            "name":request.data.get('name'),
            "month_count":request.data.get('month_count'),
            "amount":request.data.get('amount'),
            'mobile_number':request.data.get('mobile_number'),
            'start_date':request.data.get('start_date'),
            'end_date':request.data.get('end_date'),
            'adharcard':request.data.get('adharcard'),
            'photo':request.data.get('photo'),
            'adress':request.data.get('adress'),
            'gender':request.data.get('gender'),
            'dob':request.data.get('dob')
            }
            ser=SeatResSerializer(data=data)
            if ser.is_valid():
               ser.save()
               return Response(ser.data ,status=200)
            return Response(ser.errors ,status=400)
        
    def delete(self, request, id):
        user = request.user
        res = LibrarySeat.objects.filter(id=id)
        ser = LibrarySeatSerializer(res, many=True)
        libid = Library.objects.filter(id=ser.data[0]['lib'])
        serlibid = LibrarySerializer(libid, many=True)
        print(serlibid.data[0]['owner'])
        print(user.id)
        if (user.id == serlibid.data[0]['owner']):
            seres = SeatReservation.objects.filter(
                reserved_seat_id=ser.data[0]['id'])
            seres.delete()
            return Response(status=200)

    def patch(self, request, id):
        user = request.user
        res = LibrarySeat.objects.filter(id=id)
        ser = LibrarySeatSerializer(res, many=True)
        libid = Library.objects.filter(id=ser.data[0]['lib'])
        serlibid = LibrarySerializer(libid, many=True)
        print(serlibid.data[0]['owner'])
        print(user.id)
        if (user.id == serlibid.data[0]['owner']):
            reserve = SeatReservation.objects.get(
                reserved_seat_id=ser.data[0]['id'])
            ser = SeatResSerializer(reserve, data=request.data, partial=True)
            if ser.is_valid():
                ser.save()
                return Response(ser.data, status=200)
            return Response(ser.errors, status=400)


# for payment view price discovery

class paymentViewPriceDiscoveryModel(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        user = request.user
        current_year = datetime.now().year
        current_month = datetime.now().month
        current_month_start = date(current_year, current_month, 1)

        library = Library.objects.filter(owner_id=user.id)
        library_serlizer = LibrarySerializer(library, many=True)
        result_data = []
        total_amount = 0
        print(library_serlizer.data[0]['id'])
        for i in range(len(library_serlizer.data)):

            amount_collection_model_data = AmountCollection.objects.filter(library_id=library_serlizer.data[i]['id'], collection_month__gte=current_month_start,
                                                                           collection_month__lt=current_month_start + relativedelta(days=32))
            amount_collecttion_serlised_data = AmountCollectionSerailzer(
                amount_collection_model_data, many=True)
            total_amount += amount_collecttion_serlised_data.data[0]['amount']
            result_data.append(amount_collecttion_serlised_data.data)

        print(total_amount)
        return Response(result_data, status=200)


# total amount view of all libraries
class total_amount_labraries(APIView):
    # permission_classes=[IsAuthenticated ,check_subscription ]
    permission_classes = [AllowAny]

    def get(self, request):
        user = request.user

        lib = Library.objects.filter(owner_id=user.id)
        lib_serlizer = LibrarySerializer(lib, many=True)
        return Response(lib_serlizer.data)


class TotalAmount_library_wise(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id):
        user = request.user
        current_year = datetime.now().year
        current_month = datetime.now().month
        current_month_start = date(current_year, current_month, 1)

        lib = Library.objects.filter(owner_id=user.id, id=id)
        lib_serlizer = LibrarySerializer(lib, many=True)

        amount = AmountCollection.objects.filter(library_id=lib_serlizer.data[0]['id'], collection_month__gte=current_month_start,
                                                 collection_month__lt=current_month_start + relativedelta(days=32))
        amser = AmountCollectionSerailzer(amount, many=True)

        return Response(amser.data, status=200)

    def post(self, request, id):
        user = request.user
        lib = Library.objects.filter(owner_id=user, id=id)
        lib_serlizer = LibrarySerializer(lib, many=True)
        libid = lib_serlizer.data[0]['id']
        data = {
            'library': libid,
            'collection_month': request.data.get('collection_month'),
            'amount': request.data.get('amount'),
            'cost': request.data.get('cost'),
            'finalCost': request.data.get('finalCost'),
        }
        amountSer = AmountCollectionSerailzer(data=data)
        if amountSer.is_valid():
            amountSer.save()
            return Response(amountSer.data, status=200)
        return Response(amountSer.errors, status=400)


# individual amount view
# not in work may be removed
class IndiAmountView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id, idt):
        user = request.user

        # lib=Library.objects.filter(id=id)
        # lib_serlizer=LibrarySerializer(lib , many=True)
        # libid=lib_serlizer.data[0]['id']
        # print(libid )
        amount = AmountCollection.objects.filter(library_id=id, id=idt)
        amser = AmountCollectionSerailzer(amount, many=True)
        return Response(amser.data, status=200)

    def patch(self, request, id, idt):
        amount = AmountCollection.objects.get(library_id=id, id=idt)

        amoSer = AmountCollectionSerailzer(
            amount, data=request.data, partial=True)
        if amoSer.is_valid():
            amoSer.save()
            return Response(amoSer.data, status=200)
        return Response(amoSer.errors, status=400)


# al amount view

class TotalAmount(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id):
        user = request.user

        lib = Library.objects.filter(owner_id=user, id=id)
        libt = LibrarySerializer(lib, many=True)
        libid = libt.data[0]['id']
        print(libid)
        amount = AmountCollection.objects.filter(library_id=libid)
        amser = AmountCollectionSerailzer(amount, many=True)
        return Response(amser.data, status=200)

    def post(self, request, id):
        user = request.user
        lib = Library.objects.filter(owner_id=user, id=id)
        libt = LibrarySerializer(lib, many=True)
        libid = libt.data[0]['id']
        data = {
            'library': libid,
            'collection_month': request.data.get('collection_month'),
            'amount': request.data.get('amount'),
            'cost': request.data.get('cost'),
            'finalCost': request.data.get('finalCost'),
        }
        amountSer = AmountCollectionSerailzer(data=data)
        if amountSer.is_valid():
            amountSer.save()
            return Response(amountSer.data, status=200)
        return Response(amountSer.errors, status=400)


# individual amount view

class IndiAmountView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id, idt):
        user = request.user

        # lib=Library.objects.filter(id=id)
        # libt=LibrarySerializer(lib , many=True)
        # libid=libt.data[0]['id']
        # print(libid )
        amount = AmountCollection.objects.filter(library_id=id, id=idt)
        amser = AmountCollectionSerailzer(amount, many=True)

        return Response(amser.data, status=200)

    def patch(self, request, id, idt):
        amount = AmountCollection.objects.get(library_id=id, id=idt)

        amoSer = AmountCollectionSerailzer(
            amount, data=request.data, partial=True)
        if amoSer.is_valid():
            amoSer.save()
            return Response(amoSer.data, status=200)
        return Response(amoSer.errors, status=400)
