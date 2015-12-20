import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup

br = mechanize.Browser()
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize.HTTPRefreshProcessor())

br.addheaders = [('User-agent', 'Chrome')]

res = br.open('https://rice.usc.edu/kr-prd/kr/lookup.do?methodToCall=start&businessObjectClassName=org.kuali.rice.kim.bo.Person&docFormKey=88888888&returnLocation=https://rice.usc.edu/kr-prd/portal.do&hideReturnLink=true')

br.select_form(nr=0)
br.form['j_username'] = 'USERNAME'
br.form['j_password'] = 'PASSWORD'
res = br.submit()

br.select_form(nr=0)
res = br.submit()

br.select_form(nr=0)
br.form['principalName'] = ''
br.form['principalId'] = ''
br.form['entityId'] = ''
br.form['firstName'] = ''
br.form['middleName'] = ''
br.form['lastName'] = 'Burke'
br.form['emailAddress'] = ''
br.form['phoneNumber'] = ''
br.form['employeeId'] = ''
br.form['campusCode'] = ''
br.form['primaryDepartmentCode'] = ''
br.form['employeeStatusCode'] = ''
br.form['employeeTypeCode'] = ''
br.form['active'] = ['Y'] # *Y, N,
br.form.enctype = 'application/x-www-form-urlencoded'
soup = BeautifulSoup(br.submit().read())

data = []
table = soup.find(id='row')
header = table.find('thead')
data.append([col.text.strip() for col in header.findAll('th')])
tbody = table.find('tbody')
rows = tbody.findAll('tr')
for row in rows:
    cols = row.findAll('td')
    cols = [col.text.strip() for col in cols]
    data.append(cols)
print data
