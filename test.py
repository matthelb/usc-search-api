import usc_search_api

ss = usc_search_api.SearchSession('USERNAME', 'PASSWORD')
ss.init()

sr = usc_search_api.SearchRequest()
sr.set_last_name('Burke')
print ss.search(sr)
sr.set_campus_code('UPC')
print ss.search(sr)
sr['firstName'] = 'Matthew'
print ss.search(sr)
