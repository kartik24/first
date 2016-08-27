#from django.contrib.admin.templatetags.admin_list import pagination
from django.shortcuts import render
from django.utils import timezone
from .models import pathlab
from .models import pathlabinfo
from django.template import RequestContext
from django.template import Context
from django.http import HttpResponseRedirect

from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import *
from .models import *
from .forms import *
from utility import *
import json,time,ast
from django.views.decorators import csrf
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from django.contrib  import auth
from django.contrib.auth.models import User
from django.shortcuts import render,get_object_or_404,redirect



class GetPathlab(View):
	def get(self,request):
		usr_grp = get_user_grp(request.user)
		id = int(self.request.GET.get('id') or 0)
		delete = int(self.request.GET.get('delete') or 0)
		limit = int(self.request.GET.get('limit') or 10)
		page = int(self.request.GET.get('page') or 1)
		if delete == 1:
			try:
				pathlab.objects.get(Path_Lab_Id = id).delete()
				pathlabinfo.objects.get(Path_Lab_Id = id).delete()
			except :
				pass

		lab_obj = pathlab.objects.all()
		pagination_res = pagination(lab_obj,limit,page)
		return render(request,'pathlab.html',{'active_user':usr_grp,'pagination':pagination_res,'back_url':request.META.get('HTTP_REFERER') or '/'})


class GetPathlabInfo(View):
        def get(self,request):
		usr_grp = get_user_grp(request.user)
                id = int(self.request.GET.get('id') or 0)
                delete = int(self.request.GET.get('delete') or 0)
                limit = int(self.request.GET.get('limit') or 10)
                page = int(self.request.GET.get('page') or 1)
                if delete == 1:
                        try:
                                pathlabinfo.objects.get(id = id).delete()
                        except :
                                pass

                labinfo_obj = pathlabinfo.objects.all()
                pagination_res = pagination(labinfo_obj,limit,page)
                return render(request,'pathlabinfo.html',{'active_user':usr_grp,'pagination':pagination_res,'back_url':request.META.get('HTTP_REFERER') or '/'})

class RegisterPathlab(View):
	def get(self,request):
		usr_grp = get_user_grp(request.user)
		id = self.request.GET.get('id') or ''
		instance = pathlab.objects.get(doc_id=id) if id != '' else None
		pathlab_form = PathlabForm(instance=instance)
		return render(request,'addpathlab.html',{'active_user':usr_grp,'labid':id,'form':pathlab_form,'back_url':request.META.get('HTTP_REFERER') or '/'})
	def post(self,request):
		usr_grp = get_user_grp(request.user)
		id = self.request.POST.get('id') or ''
		instance = pathlab.objects.get(doc_id=id) if id != '' else None
		pathlab_form = PathlabForm(request.POST,instance = instance)
		if pathlab_form.is_valid():
			pathlab_form.save()
			success_msg = "Successfully added a new entry"
			return redirect('/pathlab')
		else:
			error_msg = "Invalid form entries "
			return render(request,'addpathlab.html',{'active_user':usr_grp,'labid':id,'error_msg':error_msg,'form':pathlab_form,'back_url':request.META.get('HTTP_REFERER') or '/'})

class RegisterPathlabInfo(View):
        def get(self,request):
		usr_grp = get_user_grp(request.user)
                id = self.request.GET.get('id') or ''
                instance = pathlabinfo.objects.get(id=id) if id != '' else None
                pathlabinfo_form = PathlabInfoForm(instance=instance)
                return render(request,'addpathlabinfo.html',{'active_user':usr_grp,'labinfoid':id,'form':pathlabinfo_form,'back_url':request.META.get('HTTP_REFERER') or '/'})
        def post(self,request):
		usr_grp = get_user_grp(request.user)
                id = self.request.POST.get('labinfoid') or ''
                instance = pathlabinfo.objects.get(id=id) if id != '' else None
                pathlabinfo_form = PathlabInfoForm(request.POST,instance = instance)
                if pathlabinfo_form.is_valid():
			lab_infolist = pathlabinfo_form.save(commit=False)
			lab_infolist.save()
			pathlabinfo_form.save_m2m()
                        #doctorinfo_form.save()
                        success_msg = "Successfully added a new entry"
                        return redirect('/pathlabinfo')
                else:
                        error_msg = "Invalid form entries "
                        return render(request,'addpathlabinfo.html',{'active_user':usr_grp,'labinfoid':id,'error_msg':error_msg,'form':pathlabinfo_form,'back_url':request.META.get('HTTP_REFERER') or '/'})


class PathlabAPI(View):
        @csrf_exempt
	def dispatch(self, *args, **kwargs):
		# dont worry about the CSRF here
		return super(PathlabAPI, self).dispatch(*args, **kwargs)
	def post(self,request):
		post_data = json.loads(request.body)
		Path_Lab_Name =  post_data.get('Path_Lab_Name') or ''
		lablist = []
		#clinic =  post_data.get('clinic') or ''
		Pathlab  = pathlab()
		Pathlab = Pathlab.apply_filter(Path_Lab_Name = Path_Lab_Name)
		try:
			labdict  = {}
			labdict['name']=Pathlab[0].Path_Lab_Name
			labdict['email']=Pathlab[0].Email_Id
			#labdict['USP']= Pathlab[0].USP
			labdict['info_list'] = []
			labinfoObj = pathlabinfo.objects.filter(Path_Lab_Id=Pathlab[0].Path_Lab_Id)

			####------ fetch all the available day(ex:monday)) for next month----- ####
			for info in labinfoObj:
				lab_info = {}
				lab_info['Test_Day'] = []
				x =  ast.literal_eval(info.Test_Day.lower())
				days =  x.keys() 
				for day in days:	
					day1  =  day[:3].capitalize()
					d = datetime.datetime.now()
					day_time = next_weekday(d, time.strptime(day1,'%a').tm_wday)
					for count in range(0,5):
						info_day = {}
						info_day['date'] = str(day_time.date())
						info_day['time']= x[day]
						lab_info['Test_Day'].append(info_day)
						day_time += datetime.timedelta(days=7)
				#lab_info['status'] = info.status
				lab_info['pathlab_name'] = info.Path_Lab_Name
				lab_info['pathlab_contact'] = info.Basic_Contact_number
				lab_info['price']  = info.Price
				#lab_info['recommendations'] = info.recommendations
				lab_info['address'] = info.Address_No1_Plot_Number + ","+ info.Address_No2_Sub_Locality
				labdict['info_list'].append(lab_info)
			lablist.append(labdict)
			return HttpResponse(json.dumps(lablist))
		except Exception as e:
			return HttpResponse(json.dumps({'result':e}))