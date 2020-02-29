import re
import sqlite3

def wordToNum(s,e):
	i = 0
	n = 0
	z = 0
	while i < len(s):
		if i in e:
			pass
		elif i > 0 and s[i-1].lower() == s[i].lower():
			if s[i].lower() == "c" and i < len(s)-1 and s[i+1].lower() in "eiy":
				n *= 10
				if n == 0:
					z += 1
		elif s[i].lower() == "b":
			if not(i > 0 and s[i-1].lower() == "m" and (i == len(s)-1 or (i < len(s)-2 and s[i+2] == " "))):
				n = 10*n+9
		elif s[i].lower() == "c":
			if i < len(s)-1 and s[i+1].lower() in "eiy":
				if not(i > 0 and s[i-1].lower() == "s"):
					n *= 10
					if n == 0:
						z += 1
			elif i < len(s)-1 and s[i+1].lower() == "h":
				if i < len(s)-2 and s[i+2].lower() in "bcdfgjklmnpqrstvwxz":
					n = 10*n+7
				else:
					n = 10*n+6
				i += 1
			else:
				n = 10*n+7
		elif s[i].lower() == "d":
			if i < len(s)-2 and s[i+1].lower() == "g" and s[i+2].lower() in "eiy":
				i += 2
				n = 10*n+6
			else:
				n = 10*n+1
		elif s[i].lower() == "f":
			n = 10*n+8
		elif s[i].lower() == "g":
			if i > 0 and s[i-1:i+1] == "ng":
				pass
			elif i < len(s)-1 and s[i+1].lower() in "eiy":
				n = 10*n+6
			elif i < len(s)-1 and s[i+1].lower() == "h":
				n = 10*n+8
				i += 1
			elif not(i < len(s)-1 and s[i+1].lower() == "n" and ((i == 0 or s[i-1] == " ") or (i == len(s)-2 or s[i+2] == " "))):
				n = 10*n+7
		elif s[i].lower() == "j":
			n = 10*n+6
		elif s[i].lower() == "k":
			if i == 0 or s[i-1].lower() != "c":
				n = 10*n+7
		elif s[i].lower() == "l":
			n = 10*n+5
		elif s[i].lower() == "m":
			n = 10*n+3
		elif s[i].lower() == "n":
			if not(i > 0 and s[i-1].lower() == "m" and (i == len(s)-1 or s[i+1] == " ")):
				n = 10*n+2
		elif s[i].lower() == "p":
			if i < len(s)-1 and s[i].lower() == "h":
				i += 1
				n = 10*n+8
			else:
				n = 10*n+9
		elif s[i].lower() == "q":
			n = 10*n+7
		elif s[i].lower() == "r":
			n = 10*n+4
		elif s[i].lower() == "s":
			if i < len(s)-1 and s[i+1].lower() == "h":
				i += 1
				n = 10*n+6
			elif i < len(s)-2 and s[i:i+3].lower() == "sch":
				i += 2
				n = 10*n+6
			else:
				n *= 10
				if n == 0:
					z += 1
		elif s[i].lower() == "t":
			if i < len(s)-1 and s[i+1].lower() == "h":
				i += 1
				n = 10*n+8
			elif not(i < len(s)-2 and s[i:i+3] == "tch"):
				n = 10*n+1
		elif s[i].lower() == "v":
			n = 10*n+8
		elif s[i].lower() == "x":
			if i == 0 or s[i-1] == " ":
				n *= 10
				if n == 0:
					z += 1
			else:
				n = 100*n+70
		elif s[i].lower() == "z":
			n *= 10
			if n == 0:
				z += 1
		i += 1
	if n == 0:
		z -= 1
	return (n,z)

def getCommand(conn):
	c = conn.cursor()
	r = input("| ")
	if str.isdigit(r):
		z = re.search("[^0]",r).start()
		q = c.execute("SELECT * FROM mnemonic WHERE number=? AND zero=?", (int(r),z))
		for i in q.fetchall():
			print(str(i[1])+", ",end="")
	elif r[:2] == "<<":
		fin = open(r[2:].strip(),"r")
		f = fin.read()
		for i in f.split("\n"):
			(n,z) = wordToNum(i,{})
			q = c.execute("SELECT COUNT(*) FROM mnemonic WHERE word=?", (i.strip(),))
			if q.fetchone()[0] == 0:
				c.execute("INSERT INTO mnemonic (word,number,zero) VALUES (?,?,?)", (i.strip(),n,z))
		conn.commit()
	elif r[0] == "?":
		q = c.execute("SELECT * FROM mnemonic WHERE word=?", (r[1:].strip(),))
		row = q.fetchone()
		if row is not None:
			if row[3] >= 0:
				print("0"*row[3]+str(row[2])+", ",end="")
	if r == "exit":
		return False
	else:
		return True

r = input("Enter database file")
conn = sqlite3.connect(r)
while getCommand(conn):
	pass
