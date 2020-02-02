from mechanize import Browser
from bs4 import BeautifulSoup as parser
from base64 import b64decode, b64encode
from requests import Session
# from module import lib
ua = "Mozilla/5.0 (Linux; Android 8.1.0; Redmi 5A Build/OPM1.171019.026; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.99 Mobile Safari/537.36"

class Module(Browser):
	def new_br(self):
		super().__init__()
		self.set_handle_robots(False)

	def viewing_html(self):
		self._factory.is_html = True

	def first(self, url, x, bytes = False):
		self.new_br()
		self.addheaders = [("user-agent", ua), ("cookie", x)]
		if bytes: data = self.open(url).read()
		else: data = self.open(url).read().decode()
		self.viewing_html()
		self.html = data
		return True if "refsrc" in str(data) else False

	def get_info_people(self, html):
		try:
			nama = parser(html, "html.parser").find("title").text
			if "/allactivity?refid=" in html:
				id_ = parser(html, "html.parser").find("a", href = lambda x: "allactivity" in x).get("href").split("/")[1]
			else:
				id_ = parser(html, "html.parser").find("a", href = lambda x: "owner_id=" in x and "/more" in x).get("href").split("=")[1]
			img = parser(html, "html.parser").find("img", alt=nama).get("src")
			if "/removefriend.php?friend_id=" in html:
				friend = True
			else:
				friend = False
			id_ = id_.replace("?", "").replace("&", "").replace("refid", "")
			return nama, id_, img, friend
		except:
			return None, None, None, None

	def get_grup(self, html):
		try:
			data = parser(self.html, "html.parser").find_all("a", href = lambda  x: "groups" in x and x.count("=") == 1)
			output = []
			for x in data:
				isi = {}
				isi["name"] = x.text
				# print(x['href'])
				isi["id"] = x["href"].split("/")[2].replace("?refid=27", "")
				output.append(isi)
		except:
			output = None
		return output

	def get_info_grup(self, html):
		try:
			data = parser(html, "html.parser")
			nama = data.find("title").text
			jumlah_m = data.find("span", id="u_0_0").text
			member = True if "/group/leave/" in html else False
			return nama, jumlah_m, member
		except:
			return None, None, None

	def get_member_group(self, html, selanjutnya = False):
		try:
			output = []
			data = parser(html, "html.parser")
			member = data.find_all("a", class_="bk" if selanjutnya else "bm")
			for x in member:
				isi = {}
				isi["name"] = x.text
				# print(x['href'])
				isi["id"] = str(x.get("href")).replace("/", "", 1).replace("profile.php?id=", "").replace("fref=fr_tab", "").replace("&", "").replace("?", "").replace("refid=17", "")
				output.append(isi)
			return output
		except:
			return None

	def next_members(self, html):
		try:
			data = parser(html, "html.parser")
			next = data.find("div", id="m_more_item")
			next = b64encode(next.find("a")["href"].encode()).decode()
			return next
		except Exception as e:
			return None

	def get_friend_list(self, html):
		try:
			output = []
			data = parser(html, "html.parser")
			teman = data.find_all("a", href = lambda x: "=fr_tab" in x)
			for x in teman:
				isi = {}
				isi["name"] = x.text
				# print(x['href'])
				isi["id"] = str(x.get("href")).replace("/", "", 1).replace("profile.php?id=", "").replace("fref=fr_tab", "").replace("&", "").replace("?", "").replace("refid=17", "")
				output.append(isi)
			return output
		except:
			return None

	def next_friends(self, html):
		try:
			data = parser(html, "html.parser")
			next = data.find("div", id="m_more_friends")
			next = b64encode(next.find("a")["href"].encode()).decode()
			return next
		except Exception as e:
			return None

	def next_likes(self, html):
		try:
			data = parser(html, "html.parser")
			next = data.find("a", href = lambda x: "/ufi/reaction/profile" in x and "shown_ids=" in x)["href"]
			next = next.replace("=10", "=1000", 1)
			next = b64encode(next.encode()).decode()
			return next
		except Exception as e:
			return None

	def buka(self, url, kuki, bytes = False):
		try: kuki = b64decode(kuki)
		except: kuki = ""
		if bytes: data = self.first(url, kuki, bytes = True)
		else: data = self.first(url, kuki)
		if data:
			self.status_kuki = "cookies invalid"
		else:
			self.status_kuki = "ok"
		return self.html

	def generate_kuki(self, u, p):
		output = {}
		try:
			ses = Session()
			data = ses.post("https://mbasic.facebook.com/login", data={"email":u, "pass":p, "login":"submit"})
			url = data.url
			if "save-device" in url or "m_sess" in url or "home.php" in url:
				output["msg"] = "success"
				kuki = ";".join([str(x).replace("<Cookie ", "").split(" ")[0] for x in ses.cookies]).encode()
				# print(kuki)
				output["encoded_cookies"] = b64encode(kuki).decode()
			elif "checkpoint" in url:
				output["msg"] = "akun ente checkpoint"
				output["encoded_cookies"] = None
			else:
				raise KeyError
		except:
			output["msg"] = "Username/Password Salah!"
			output["encoded_cookies"] = None
		return output

