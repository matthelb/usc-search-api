import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup
from fake_useragent import UserAgent

class InvalidLogin(Exception):


    def __init__(self, username, password):
        super(InvalidLogin, self).__init__(
                'Username %s or password %s rejected.' % (username, password))



class SearchSession:


    FORM_ENCTYPE = 'application/x-www-form-urlencoded'
    SEARCH_URL = 'https://rice.usc.edu/kr-prd/kr/lookup.do?methodToCall=start&businessObjectClassName=org.kuali.rice.kim.bo.Person&docFormKey=88888888&returnLocation=https://rice.usc.edu/kr-prd/portal.do&hideReturnLink=true'
    SSO_REDIRECT_URL = 'https://shibboleth.usc.edu:443/idp/profile/SAML2/Redirect/SSO'
    SSO_URL = 'https://shibboleth.usc.edu:443/idp/Authn/UserPassword'

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.browser = mechanize.Browser()
        self.cookie_jar = cookielib.LWPCookieJar()
        self.browser.set_cookiejar(self.cookie_jar)
        self.browser.set_handle_equiv(True)
        self.browser.set_handle_redirect(True)
        self.browser.set_handle_referer(True)
        self.browser.set_handle_robots(False)
        self.browser.set_handle_refresh(mechanize.HTTPRefererProcessor())
        self.browser.addheaders = [('User-agent', UserAgent().random)]

    def init(self):
        self.browser.open(SearchSession.SEARCH_URL)
        self._login()

    def _login(self):
        self.browser.select_form(nr=0)
        self.browser.form['j_username'] = self.username
        self.browser.form['j_password'] = self.password
        self.browser.submit()
        if self.browser.geturl() == SearchSession.SSO_REDIRECT_URL:
            self.browser.select_form(nr=0)
            self.browser.submit()
        else:
            raise InvalidLogin(self.username, self.password)

    def search(self, request):
        self.browser.open(SearchSession.SEARCH_URL)
        if self.browser.geturl() == SearchSession.SSO_URL:
            self._login()
        self.browser.select_form(nr=0)
        for k, v in request.viewitems():
            self.browser.form[k] = v
        self.browser.form.enctype = SearchSession.FORM_ENCTYPE
        self.browser.submit()
        if self.browser.geturl() == SearchSession.SSO_URL:
            return self.search(request)
        else:
            return SearchSession.parse_search(self.browser.response().read())

    @staticmethod
    def parse_search(html):
        soup = BeautifulSoup(html)
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
        return data

