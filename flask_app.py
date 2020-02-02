from flask import Flask, request, render_template
from module import Module, setting, other
from bs4 import BeautifulSoup as parser
from base64 import b64decode
import json
mo = Module()
app = Flask(__name__)

@app.route('/')
def index():
	# return other.oh()
	return render_template("index.html", url=setting.url)

@app.route('/me/')
def me():
	output = {"status":{}, "data":{}}
	kuki = request.args.get("kuki")
	data = mo.buka(f"https://mbasic.facebook.com/me/", kuki)
	output["status"]["cookie"] = mo.status_kuki
	output["data"]["name"], output["data"]["id"], output["data"]["profile_picture"], output["status"]["friend"] = mo.get_info_people(data)
	return json.dumps(output)

@app.route('/me/groups/')
def me_group():
	output = {"status":{}, "data":{}}
	kuki = request.args.get("kuki")
	data = mo.buka(f"https://mbasic.facebook.com/groups/?seemore", kuki)
	output["status"]["cookie"] = mo.status_kuki
	output["data"] = mo.get_grup(data)
	return json.dumps(output)

@app.route("/me/friends/")
def myfriend_list():
	id_ = "me"
	output = {"status":{}, "data":{}}
	kuki = request.args.get("kuki")
	next = request.args.get("next")
	try:
		if next == None:
			data = mo.buka(f"https://mbasic.facebook.com/{id_}", kuki)
			# return data
			data = parser(data, "html.parser")
			url = "https://mbasic.facebook.com" + data.find("a", href = lambda x: "friends" in x and "lst=" in x)["href"]
		else:
			url = "https://mbasic.facebook.com/" + b64decode(next).decode()
			# print(url)
		data = mo.buka(url, kuki)
		output["status"]["cookie"] = mo.status_kuki
		output["data"] = mo.get_friend_list(data)
		next = mo.next_friends(data)
		output["next"] = None if next == None else f"{setting.url}/people/{id_}/friends/?kuki={kuki}&next={next}"
		return json.dumps(output)
	except Exception as e:
		# output["status"]["cookie"] = None
		output["data"], output["next"] = None, None
		return json.dumps(output)

@app.route("/group/<id_>/")
def group(id_):
	output = {"status":{}, "data":{}}
	kuki = request.args.get("kuki")
	data = mo.buka(f"https://mbasic.facebook.com/groups/{id_}?view=info", kuki)
	output["status"]["cookie"] = mo.status_kuki
	output["data"]["name"], output["data"]["members"], output["status"]["member"] = mo.get_info_grup(data)
	return json.dumps(output)

@app.route('/people/<user>/')
def people_info(user):
	output = {"status":{}, "data":{}}
	kuki = request.args.get("kuki")
	data = mo.buka(f"https://mbasic.facebook.com/{user}/", kuki)
	output["status"]["cookie"] = mo.status_kuki
	output["data"]["name"], output["data"]["id"], output["data"]["profile_picture"], output["status"]["friend"] = mo.get_info_people(data)
	return json.dumps(output)

@app.route("/group/<id_>/members/")
def grup_members(id_):
	output = {"status":{}, "data":{}}
	kuki = request.args.get("kuki")
	next = request.args.get("next")
	try:
		url = f"https://mbasic.facebook.com/browse/group/members/?id={id_}" if next == None else "https://mbasic.facebook.com" + b64decode(next).decode()
		data = mo.buka(url, kuki)
		output["status"]["cookie"] = mo.status_kuki
		# print(mo.get_member_group(data, selanjutnya = True if next != None else False))
		output["data"] = mo.get_member_group(data, selanjutnya = True if next != None else False)
		next = mo.next_members(data)
		output["next"] = None if next == None else f"{setting.url}/group/{id_}/members/?kuki={kuki}&next={next}"
		return json.dumps(output)
	except Exception as e:
		output["status"]["cookie"] = None
		output["data"], output["next"] = None, None
		return json.dumps(output)

@app.route("/people/<id_>/friends/")
def friend_list(id_):
	output = {"status":{}, "data":{}}
	kuki = request.args.get("kuki")
	next = request.args.get("next")
	try:
		if next == None:
			data = mo.buka(f"https://mbasic.facebook.com/{id_}", kuki)
			# return data
			data = parser(data, "html.parser")
			url = "https://mbasic.facebook.com" + data.find("a", href = lambda x: "friends" in x and "lst=" in x)["href"]
		else:
			url = "https://mbasic.facebook.com/" + b64decode(next).decode()
			# print(url)
		data = mo.buka(url, kuki)
		output["status"]["cookie"] = mo.status_kuki
		output["data"] = mo.get_friend_list(data)
		next = mo.next_friends(data)
		output["next"] = None if next == None else f"{setting.url}/people/{id_}/friends/?kuki={kuki}&next={next}"
		return json.dumps(output)
	except Exception as e:
		# output["status"]["cookie"] = None
		output["data"], output["next"] = None, None
		return json.dumps(output)

# @app.route("/people/<id_>/<sts>/")
# def post_sts_people(id_, sts):
# 	output = {"status":{}, "data":{}}
# 	kuki = request.args.get("kuki")
# 	data = mo.buka(f"https://mbasic.facebook.com/story.php?story_fbid={sts}&id={id_}", kuki)
# 	# return data
# 	data = parser(data, "html.parser")
# 	output["status"]["cookie"] = mo.status_kuki
# 	try:
# 		output["data"]["name"] = data.find("a", href = lambda x: "mf_story_key" in x).text
# 		output["data"]["status"] = data.find("p").text.replace("<br>", "\n")
# 	except:
# 		output["data"]["name"] = None
# 		output["data"]["status"] = None
# 	return json.dumps(output)

@app.route("/post/<sts>/likes/", methods=["GET", "POST"])
def post_sts_like(sts):
	if request.method == "POST" or request.args.get("method") == "post":
		return other.like_post(sts)
	output = {"status":{}, "data":{}}
	kuki = request.args.get("kuki")
	next = request.args.get("next")
	tipe = request.args.get("type")
	if tipe == None:
		tipe = "1"
		nama_tipe = "like"
	elif tipe == "keren":
		tipe = "3"
		nama_tipe = "wow"
	elif tipe == "ngamuk":
		tipe = "8"
		nama_tipe = "angry"
	elif tipe == "ngakak":
		tipe = "4"
		nama_tipe = "haha"
	elif tipe == "mantapmantap":
		tipe = "2"
		nama_tipe = "love"
	elif tipe == "sadna":
		tipe = "7"
		nama_tipe = "sad :("
	else:
		tipe = "1"
		nama_tipe = "like"
	try:
		if next != None:
			url = "https://mbasic.facebook.com" + b64decode(next).decode()
			print(url)
		else:
			url = f"https://mbasic.facebook.com/ufi/reaction/profile/browser/?&ft_ent_identifier={sts}"
			data = mo.buka(url, kuki)
			data = parser(data, "html.parser")
			url = "https://mbasic.facebook.com" + data.find("a", href = lambda x: f"reaction_type={tipe}" in x)["href"].replace("=10", "=1000", 1)
			# print(url)
		data = mo.buka(url, kuki)
		data = parser(data, "html.parser")
		jelma = []
		for x in data.find_all("a", href = lambda x: not "=" in x and x.count("/") == 1):
			isi = {}
			isi["name"] = x.text
			isi["id"] = x["href"].replace("/", "", 1).replace("profile.php?id=", "")
			jelma.append(isi)
		output["status"]["cookie"] = mo.status_kuki
	except:
		output["status"]["cookie"] = None
	try:
		output["data"]["reaction"] = nama_tipe
		output["data"]["total"] = len(jelma)
		output["data"]["data"] = jelma
		next = mo.next_likes(mo.html)
		output["data"]["next"] = None if next == None else f"{setting.url}/{sts}/likes/?kuki={kuki}&next={next}&type={request.args.get('type')}"
	except:
		output["data"]["reaction"] = None
		output["data"]["total"] = None
	return json.dumps(output)

@app.route("/generate_cookies", methods=["POST"])
def gen_kuki():
	u = request.form.get("user")
	p = request.form.get("pass")
	return json.dumps(mo.generate_kuki(u, p))


# if __name__=='__main__':
# 	app.run(debug=True)