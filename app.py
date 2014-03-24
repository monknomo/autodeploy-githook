from bottle import run, request, post
from subprocess import check_call, CalledProcessError
from json import load
from shutil import copytree, rmtree
p = load(open('props.json'))

@post('/')
def incoming():
	print(request.json['repository']['full_name'])
	if request.json['repository']['owner']['login'] == p['login']:
		try:
			try:
				rmtree(p['clone_dir']+request.json['repository']['full_name'])
			except FileNotFoundError as e:
				print(p['clone_dir']+request.json['repository']['full_name'] + " doesn't exist, but that's ok")
			check_call(["git","clone",request.json['repository']['clone_url'],p['clone_dir']+request.json['repository']['full_name']])
			try:
				copytree(p['clone_dir']+request.json['repository']['full_name'], p['dst_dir'])
			except FileExistsError as e:
				rmtree(p['dst_dir'])
				copytree(p['clone_dir']+request.json['repository']['full_name'], p['dst_dir'])
		except CalledProcessError as e:
			print(e)	

run(host='localhost', port=8080)
