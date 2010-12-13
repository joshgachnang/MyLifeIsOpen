def MobileTemplate(request):
    if request.is_mobile:
	return {'extend_base': 'mobile_base.html'}
    else:
	return {'extend_base': 'base.html'}