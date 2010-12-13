# -*- coding: utf-8 -*-
MOBILE_USERAGENTS = ("2.0 MMP","240x320","400X240","AvantGo","BlackBerry",
    "Blazer","Cellphone","Danger","DoCoMo","Elaine/3.0","EudoraWeb",
    "Googlebot-Mobile","hiptop","IEMobile","KYOCERA/WX310K","LG/U990",
    "MIDP-2.","MMEF20","MOT-V","NetFront","Newt","Nintendo Wii","Nitro",
    "Nokia","Opera Mini","Palm","PlayStation Portable","portalmmm","Proxinet",
    "ProxiNet","SHARP-TQ-GX10","SHG-i900","Small","SonyEricsson","Symbian OS",
    "SymbianOS","TS21i-10","UP.Browser","UP.Link","webOS","Windows CE",
    "WinWAP","YahooSeeker/M1A1-R2D2","iPhone","iPod","Android",
    "BlackBerry9530","LG-TU915 Obigo","LGE VX","webOS","Nokia5800",)
    
user_agents_test = ("w3c ", "acs-", "alav", "alca", "amoi", "audi",
		    "avan", "benq", "bird", "blac", "blaz", "brew",
		    "cell", "cldc", "cmd-", "dang", "doco", "eric",
		    "hipt", "inno", "ipaq", "java", "jigs", "kddi",
		    "keji", "leno", "lg-c", "lg-d", "lg-g", "lge-",
		    "maui", "maxo", "midp", "mits", "mmef", "mobi",
		    "mot-", "moto", "mwbp", "nec-", "newt", "noki",
		    "xda",  "palm", "pana", "pant", "phil", "play",
		    "port", "prox", "qwap", "sage", "sams", "sany",
		    "sch-", "sec-", "send", "seri", "sgh-", "shar",
		    "sie-", "siem", "smal", "smar", "sony", "sph-",
		    "symb", "t-mo", "teli", "tim-", "tosh", "tsm-",
		    "upg1", "upsi", "vk-v", "voda", "wap-", "wapa",
		    "wapi", "wapp", "wapr", "webc", "winw", "winw",
		    "xda-",)

import re


class MobileDetectionMiddleware(object):
    """
    Useful middleware to detect if the user is
    on a mobile device.
    """

    def process_view(self, request, view_func, view_args, view_kwargs):
        is_mobile = False;

        if request.META.has_key('HTTP_USER_AGENT'):
            user_agent = request.META['HTTP_USER_AGENT']
            # Test common mobile values.
            pattern = "(up.browser|up.link|mmp|symbian|smartphone|midp|wap|phone|windows ce|pda|mobile|mini|palm|netfront)"
            prog = re.compile(pattern, re.IGNORECASE)
            match = prog.search(user_agent)

            if match:
                is_mobile = True;
            else:
                # Nokia like test for WAP browsers.
                # http://www.developershome.com/wap/xhtmlmp/xhtml_mp_tutorial.asp?page=mimeTypesFileExtension

                if request.META.has_key('HTTP_ACCEPT'):
                    http_accept = request.META['HTTP_ACCEPT']

                    pattern = "application/vnd\.wap\.xhtml\+xml"
                    prog = re.compile(pattern, re.IGNORECASE)

                    match = prog.search(http_accept)

                    if match:
                        is_mobile = True

            if not is_mobile:
                # Now we test the user_agent from a big list.
                if user_agent in MOBILE_USERAGENTS:
		    is_mobile = True

                test = user_agent[0:4].lower()
                if test in user_agents_test:
                    is_mobile = True
        request.is_mobile = is_mobile