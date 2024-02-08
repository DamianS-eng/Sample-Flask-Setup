import os
import re
import json
from flask import Flask, send_from_directory, url_for, request
from flask_restful import Api
from urllib.request import urlretrieve
#
app = Flask(__name__)
api = Api(app)

# 
# # File imported consists of a list of one, parse with json
# # holding two items: first is the list of key descriptors, second is the list of scenarios.
# # 
# 

portno = 10633
# Adjust port number in html template if this changes.
filename = "sample"
webpage_template = "web_template.html"
webpage = '''<!DOCTYPE html>
<html lang="en"><head><title>Unable To Retrieve</title></head><body><h1>Unretrieved</h1></body></html>'''
fav_path = 'favicon.ico'
ps_url = (
  "http://localhost/here"
)

def get_list_elements(stuff):
  li_insert = ""
  for i in stuff:
    li_insert += """\t\t\t\t\t<li>""" +str(i[0]) + """</li>\n\t\t\t\t"""
  return li_insert

def get_select_elements(stuff):
  select_insert = """\t\t\t\t\t<label for="in-form">Choose one</label>\n
  \t\t\t\t\t<select title="select_option" id="in-form" name="in-form"> \n"""
  for i in stuff:
    select_insert += """\t\t\t\t\t\t<option value=""" + str(i[0]) + """/> """ + str(i[0]) + """ </option> \n"""
  select_insert += """\t\t\t\t\t </select> \n 
\t\t\t\t\t<br />\n
\t\t\t\t\t<input type="submit" value="Submit"/> \n\t\t\t\t"""
  return select_insert

# Create List of dictionaries
def getDict():
  outlist = []
  with open(filename, "r") as f:
    retrieve_data = tuple(json.load(f))
  descr = retrieve_data[0]
  stuff = retrieve_data[1]
  for s in range(len(stuff)):
    sc_dict = {}
    for i in range(len(stuff[s])):
      sc_dict.update({descr[i]:stuff[s][i]})
    out_list.append(sc_dict)
  return(out_list, sim_list)

def generate():
  try:
    urlretrieve(ps_url, filename)
  except:
    print("Cannot retrieve remote list")
    return(webpage)

  stuff, slist = getDict()

  # Append form to template
  with open(webpage_template) as f:
    webpage = f.read()
  form = re.search(r"<select", webpage).span()[0] 
  endform = webpage.find("</form")
  webpage_front = webpage[:form - 1]
  webpage_end = webpage[endform:]
  webpage = webpage_front + get_seleect_elements(slist) + webpage_end
  
  # Append list to template
  ul = re.search(r"<ul", webpage).span()[1]
  endul = webpage.find("</ul")
  webpage_front = webpage[:ul + 1]
  webpage_end = webpage[endul:]
  webpage = webpage_front + get_list_elements(slist) + webpage_end
  return webpage

@app.route('/', methods=['GET'])
def index():
  return(webpage, 200)

@app.route('/favicon.ico/', methods=['GET'])
def favicon():
  print(send_from_directory(os.path.join(app.root_path, 'static'), fav_path))
  return send_from_directory(os.path.join(app.root_path, 'static'),
      fav_path)

@app.route('/desc/', methods=['GET'])
def desc():
  with open(filename, "r") as f:
    basic_list = json.load(f)
  descr = basic_list[0]
  return (descr,  200)

@app.route('/length/', methods=['GET'])
def scenarios_len():
  s_dict, scenarios = getDict()
  return (str(len(scenarios)) + " scenarios have been found.", 200)

@app.route('/form/')
def get_data():
  num = request.args.get('in-form')[:-1]
  print(num)
  if (not num):
    return("No scenario is provided.", 422)
  stuff, slist = getDict()
  index = next((i for i, x in enumerate(stuff) if x['TITLE'] == num), None)
  if(index == None):
    return ("Invalid Selection, maybe...", 510)
  return (stuff[index], 200)

if __name__ == '__main__':
  webpage = generate()
  app.run(host='0.0.0.0', port=portno, debug=True)
