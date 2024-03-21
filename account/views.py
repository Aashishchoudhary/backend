from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from django.contrib.auth import get_user_model
User=get_user_model()
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated , AllowAny ,IsAdminUser, IsAuthenticatedOrReadOnly 


from rest_framework_simplejwt.tokens import RefreshToken

from .models import PhoneOTP
from .serializer import CreateUserSerialzier ,ChangePasswordSerializer ,ForgotPasswordSerializer ,PhoneOtpSerlizer ,CustomUserSerlizer ,SendRegisterOtpSerliazer ,ValidateRegisterOtp

from django.db.models import Q

from .email import send_otp_via_mail
# import http.client
# conn = http.client.HTTPSConnection("2factor.in")





#for genrating jwt custom token



def get_token_for_user(user):
    refresh=RefreshToken.for_user(user)
    return {
        'refresh':str(refresh),
        'access':str(refresh.access_token)
    }




    


# view for login with otp

class OtpBasedLogin(APIView):
    permission_classes=[AllowAny]
    def post(self , request):
        username=request.data.get('username')
        otp=request.data.get('otp')
        user=authenticate(request ,username=username , otp=otp)
        print(user)
        if user is not None:
          
            token=get_token_for_user(user)
            return Response(token , status=200)
        return Response({'message':"Otp is Incorrect"} , status= 400)
    

# otp for login with otp
class LoginOTP(APIView):
    permission_classes=[AllowAny]
    def post(self ,request):
        username=request.data.get('username')
        if username:
            username=str(username)
            user=User.objects.filter(Q(username=username)|Q(email=username))
            serlizer = CustomUserSerlizer(user ,many=True).data
            email = serlizer[0]['email']
            phone= serlizer[0]['username']
            if user.exists() ==False:
                return Response({"status":True ,'details':'User not Found kindly register first'} ,status=400)
            else: #for registerd user
                
                otp =send_otp_via_mail(email)
                print(email , otp)
                #if otp alreday exists  then otp counter will increase by one on every otp sent
                if otp :
                    otp=str(otp)
                    old_otp=PhoneOTP.objects.filter(email = email)
                    if old_otp.exists():
                        old_otp=old_otp.first()
                        otp_count=old_otp.count

                        if otp_count>5:
                            return Response({"status":False ,'details':'You have excessed the otp limit so plese contact to cutomer service'},status=400)
                        old_otp.count=otp_count+1 
                        old_otp.otp=otp
                        old_otp.save()
                        return Response({'status':True,"details":"OTP sent successfully"},status=200)                               
                    else:
                        PhoneOTP.objects.create(email= email , phone = phone , 
                                                otp=otp)
                        return Response({'status':True ,'details':'otp sent successfully'},status=200)
                    

                else:
                    return Response({"details":"problem in sending otp please try agin later"} , status=400) 


        else :
            return Response({"details":"kindly check phone number do send request again"},status=400)     



# send otp for registered user
class SendOTP(APIView):
    permission_classes=[AllowAny]
    def post(self , request):
        serlizer_data=SendRegisterOtpSerliazer(data=request.data)
        if serlizer_data.is_valid():
           phone=serlizer_data.data['phone']
           email=serlizer_data.data['email']
   
           if phone and email:
               phone=str(phone)
               user= User.objects.filter(Q(username=phone)|Q(email=email))
               if user.exists() ==True:
                   return Response({'details':'user already exists,  please login' } ,status=400)
               
               else:
                   otp=send_otp_via_mail(email)
                   print(otp)
                   if otp:
                       old_otp=PhoneOTP.objects.filter(Q(phone=phone)|Q(email=email))
                       if old_otp.exists():
                           old_otp=old_otp.first()
                           otp_count=old_otp.count
                           
                           if otp_count>5:
                               return Response({'deatils':"your otp limit exceed from allowed limit so please c   onatct to coustomer"} ,status=400)
                           old_otp.otp=otp
                           old_otp.count =otp_count+1
                           old_otp.save()
                           return Response({'status':True,"details":"OTP sent successfully"} ,status=   200)
   
                       else:
                           PhoneOTP.objects.create(phone=phone,email=email, otp=otp)
                           return Response({'deatils':'otp send successfully'} ,status=200)
                   else:
                       return Response({'details':'otp not send please try agin later'} ,status=400)
                   
           else:
            return Response({'details':"plese provide  phone number , Email and try again"} ,status=400)
        else:
            return Response({"deatils":"please fill the correct data"})



# for validating send phone otp while registering

class ValidatePhoneOtp(APIView):
    permission_classes=[AllowAny]
    def post(self , request):
        serlized_data= ValidateRegisterOtp(data=request.data)
        if serlized_data.is_valid():
            phone=serlized_data.data['phone']
            otp_sent=serlized_data.data['otp']
            email=serlized_data.data['email']
            print('valid')
            if phone and email and otp_sent:            
                old=PhoneOTP.objects.filter(Q(phone=phone)&Q(email=email))
    
                if old.exists():
                    old=old.first()
                    otp=old.otp
    
                    print('exists')
                    if str(otp)==str(otp_sent):
                        old.logged=True
                        print('looged',old.logged)
                        old.save()
                        return Response({'status':True ,'details':"Otp matched kindly proceed for registra    rion"} ,status=200)
                    else:
                        print('otp incorrect')
                        return Response({
                            'status' : False, 
                            'details' : 'OTP incorrect, please try again'
                        } ,status=400)
    
                else:
                    print('phone in')
                    return Response({
                        'status' : False,
                        'details' : 'Incorrect Phone number. Kindly request a new otp with this number'
                    } ,status=400)
    
            else:
                return Response({
                    'status' : 'False',
                    'details' : 'Either phone or otp was not recieved in Post request'
                } ,status=400)
        print('ff')

        return Response({"details":"please fill the correct data"})

  
class Register(APIView):
    permission_classes=[AllowAny]
    def post(self, *args, **kwargs):
        phone = self.request.data.get('phone', False)
        email=self.request.data.get('email', False)
        password = self.request.data.get('password', False)
        
        if phone and password and email:
            phone = str(phone)
            user = User.objects.filter(Q(username=phone)|Q(email=email))

            if user.exists():
                return Response({
                    'status': False, 
                    'details': 'Phone Number already have account associated. Kindly try forgot password'
                    } ,status=400)

            else:
                old = PhoneOTP.objects.filter(Q(phone=phone)|Q(email=email))
                if old.exists():
                    old=old.first()

                    if old.logged:
                        temp_data = {'username':phone,"email":email,'password':password}
                        serializer = CreateUserSerialzier(data=temp_data)
                        serializer.is_valid(raise_exception = True)
                        user = serializer.save()

                        old.delete()
                        return Response({
                            'status' : True, 
                            'details' : 'Congratulations, user has been created successfully.'
                        } ,status=200)

                    else:
                        return Response({
                            'status': False,
                            'details': 'Your otp was not verified earlier. Please go back and verify otp'

                        } ,status=400)

                else:
                    return Response({
                    'status' : False,
                    'details' : 'Phone number not recognised. Kindly request a new otp with this number'
                } ,status=400)

        else:
            return Response({
                'status' : 'False',
                'details' : 'Either phone or password was not recieved in Post request'
            },status=400)

# user login with password view
class UserLoginPassword(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        username=request.data.get('username')
        password=request.data.get('password')
        if username and password:
            try:
               user=authenticate(request , username = username , password =password)
               if user is not None:
                   token=get_token_for_user(user)
                   return Response(token , status=200)
            except:
               return Response({"details":"username or password inccorect"} , status=400)
        return Response({"details":"please check the filled data and try again"})


#change password                 
                


class ChangePasswordView(APIView):
    permission_classes=[IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    # model = User
    # permission_classes = (AllowAny,)

    

    def put(self, request, id):  # Use 'id' as a positional argument, not 'pk'
        print('id' , id)
        try:
        # Retrieve the user object based on the provided id
          self.object = User.objects.get(pk=id)
          print('obj' , self.object)
        except User.DoesNotExist:
           print('user don t exist' )
           return Response({"details": "User not found."}, status=status.HTTP_404_NOT_FOUND)
          
        serializer = ChangePasswordSerializer(data=request.data)
       

        if serializer.is_valid():
            print('valid')
        # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
              return Response({"details": " incorrect old password."}, status=status.HTTP_400_BAD_REQUEST)

        # Set the new password and save the user
            
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            token = RefreshToken(request.data.get('refresh'))
            token.blacklist()
         
            response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'details': 'Password updated successfully',
            'data': []
        }
            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# forgot password serlizer
class ForgotPasswordChange(APIView):
    permission_classes=[AllowAny]
    def post(self, *args, **kwargs):
        username = self.request.data.get('username', False)
        
        password = self.request.data.get('password', False)
        
        if username  and password:
            print(password , username)
            old = PhoneOTP.objects.filter(Q(phone=username)|Q(email=username))
            if old.exists():

                old = old.first()
                if old.forgot_logged:

                    post_data ={
                    
                    'password':password
                    }
                    print('postdata',post_data)
                    user_obj = User.objects.get(Q(username=username)|Q(email=username))
                    serializer = ForgotPasswordSerializer(data = post_data)
                    print('user ',user_obj)
                    if serializer.is_valid():
                        if user_obj:
                            print("password" )
                            user_obj.set_password(serializer.data.get('password'))
                            user_obj.is_active = True
                            user_obj.save()
                            old.delete()
                            return Response({
                            'status' : True,
                            'details' : 'Password changed successfully. Please Login'
                            })
                        return Response({"went wrong"})

                else:
                    return Response({
                    'status' : False,
                    'details' : 'OTP Verification failed. Please try again in previous step'
                    })

            else:
                return Response({
                'status' : False,
                'details' : 'Phone and otp are not matching or a new phone has entered. Request a new otp in forgot password'
            })

        else:
            return Response({
                'status' : False,
                'details' : 'Post request have parameters mising.'
            })



# vaidate phone forgot otp
class ValidatePhoneForgot(APIView):
    permission_classes=[AllowAny]
    def post(self, *args, **kwargs):
        username = self.request.data.get('username')

        if username:
            username = str(username)
            user = User.objects.filter(Q(username=username)|Q(email=username))
            serilized_data= CustomUserSerlizer(user , many=True).data
            email=serilized_data[0]['email']
            phone=serilized_data[0]['username']

            if user.exists()==True:
                otp = send_otp_via_mail(email)
                print(username, otp)

                if otp:
                    otp = str(otp)
                    old = PhoneOTP.objects.filter(Q(phone=username)|Q(email=username))

                    if old.exists():
                        old=old.first()
                        count=old.count

                        if old.count > 10:
                            return Response({
                                'status' : False, 
                                'details' : 'Maximum otp limits reached. Kindly support our customer care or try with different number'
                            } ,status=400)
                        else:
                            old.count = old.count+1
                            old.otp = otp
                            old.save()
                            return Response({'status': True, 'details': 'OTP has been sent for password reset. Limits about to reach.'} ,status=200)

                    else:
                        count = 0
                        count = count + 1
                        PhoneOTP.objects.create(
                            phone=phone,
                            otp=otp,
                            email=email,
                            count=count,
                            forgot=True)
                        return Response({'status': True, 'details': 'OTP has been sent for password reset'} ,status=200)

                else:
                    return Response({
                                    'status': False, 'details' : "OTP sending error. Please try after some time."
                                } ,status=400)


            else:
                return Response({
                    'status' : False,
                    'details' : 'Phone number not recognised. Kindly try a new account for this number'
                } ,status=400)




class ValidateForgotOtp(APIView):
    permission_classes=[AllowAny]
    def post(self, *args, **kwargs):
        username = self.request.data.get('username', False)
        otp_sent = self.request.data.get('otp', False)

        if username and otp_sent:
            old = PhoneOTP.objects.filter(Q(phone=username)|Q(email=username))

            if old.exists():
                old=old.first()

                if old.forgot==False:
                    return Response({
                        'status' : False, 
                        'details' : 'This phone has not received valid otp for forgot password. Request a new otp or contact help centre.'
                    })

                else:
                    otp = old.otp

                    if str(otp) == str(otp_sent):
                        old.forgot_logged = True
                        old.save()
                        return Response({
                        'status' : True, 
                        'details' : 'OTP matched, kindly proceed to create new password'
                        })

                    else:
                        return Response({
                        'status' : False, 
                        'details' : 'OTP incorrect, please try again'
                        })

            else:
                return Response({
                    'status' : False,
                    'details' : 'Phone not recognised. Kindly request a new otp with this number'
                })

        else:
            return Response({
                'status' : 'False',
                'details' : 'Either phone or otp was not recieved in Post request'
            })


class BlacklistRefreshView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request):
        token = RefreshToken(request.data.get('refresh'))
        token.blacklist()
        return Response("Success")


class ViewPhone(APIView):
    permission_classes=[IsAdminUser]
    def get(self , request):
       phone = PhoneOTP.objects.all()
       serPhone=PhoneOtpSerlizer(phone , many=True)
       return Response(serPhone.data , status=200)
    

    def post(self , request):
        serData = PhoneOtpSerlizer(data=request.data)
        if serData.is_valid():
            serData.save()
            return Response(serData.data , status=200)
        return Response(serData.errors , status=400)
    

class EditPhoneOtp(APIView):
    permission_classes=[IsAdminUser]
    def get(self, request ,id):
       phone = PhoneOTP.objects.get(id=id)
       serPhone=PhoneOtpSerlizer(phone )
       return Response(serPhone.data , status=200)
    
    def patch(self, request ,id):
       phone = PhoneOTP.objects.get(id=id)
       serData=PhoneOtpSerlizer(phone ,data=request.data , partial=True )
       if serData.is_valid():
            serData.save()
            return Response(serData.data , status=200)
       return Response(serData.errors , status=400)
       


    
