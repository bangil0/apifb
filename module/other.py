from module import Module
from flask import request
from bs4 import BeautifulSoup as parser
import json


mo = Module()
def like_post(sts):
	output = {"status":{}, "data":{}}
	kuki = request.form.get("kuki")
	if kuki == None and request.args.get("kuki") != None:
		kuki = request.args.get("kuki")
	url = mo.buka(f"https://mbasic.facebook.com/ufi/reaction/profile/browser/?ft_ent_identifier={sts}&refid=18", kuki)
	output["status"]["cookie"] = mo.status_kuki
	url = parser(url, "html.parser")
	try:
		url = url.find("a", href = lambda x: "?view=permalink&id=" in x or "story.php?" in x or "photo.php?" in x or "/photos/" in x)
		url = "https://mbasic.facebook.com" + url["href"]
		url = mo.buka(url, kuki)
		url = parser(url, "html.parser")
		url = url.find("a", href = lambda x: "/like.php" in x)
		if url == None:
			output["data"]["status"] = "liked"
		else:
			url = "https://mbasic.facebook.com" + url["href"]
			mo.buka(url, kuki)
			output["data"]["status"] = "success"
		output["data"]["url"] = url
	except KeyError:
		output["data"]["status"] = "terjadi error"
	return json.dumps(output)
