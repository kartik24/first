from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.translation import ugettext as _
from django.db.models import SmallIntegerField
import datetime

def next_weekday(d, weekday):
	days_ahead = weekday - d.weekday()
	if days_ahead <= 0: # Target day already happened this week
		days_ahead += 7
	return d + datetime.timedelta(days_ahead)
DAYS_OF_WEEK = (
('1', 'Monday'),
('2', 'Tuesday'),
('3', 'Wednesday'),
('4', 'Thursday'),
('5', 'Friday'),
('6', 'Saturday'),
('7', 'Sunday'),
)

DOC_STATUS = (

(1,'Available'),
(2, 'Not Available'),
(3, 'Booked')
)
def pagination(obj,limit,page=1):
        paginator = Paginator(obj,limit)
        try:
                pagination_res = paginator.page(page)
        except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                pagination_res = paginator.page(1)
        except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                pagination_res = paginator.page(paginator.num_pages)
        return pagination_res


Grp = {
'Superuser':0,
'Admin':1,
'Operator':2,
'Readonly':3
}
USER_GRP = {
'Admin' : 'auth.delete_user',
'Operator' :'',
'ReadOnly':''
}
def  login_required(user):
        if  not user.is_authenticated()  or  user.is_anonymous():
                return True
        else:
                return False
def get_user_grp(user):
        perm = user.get_group_permissions()
        if user.is_superuser:
                user_grp = Grp['Superuser']
        elif USER_GRP['Admin'] in  perm:
                user_grp = Grp['Admin']
        elif len(perm)> 0:
                user_grp = Grp['Operator']
        else:
                user_grp = Grp['Readonly']
        return user_grp



