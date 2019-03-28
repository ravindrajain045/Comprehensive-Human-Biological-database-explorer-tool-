import urllib
import json
import os
base_url="http://amp.pharm.mssm.edu/Harmonizome"

def openweb(web):
	a=urllib.urlopen(web)
	b=a.read().decode()
	c= json.loads(b)
	return c
def mirna():
	import urllib
	from bs4 import BeautifulSoup
	print"Hi , Please wait . Its loading..."
	baseurl='http://www.mirbase.org'
	url1 = "http://www.mirbase.org/cgi-bin/mirna_summary.pl?org=hsa"
	page=urllib.urlopen(url1)
	soup = BeautifulSoup(page, "html.parser")
	a=soup.find_all('a')
	x=str()
	y=str()
	q=[]
	w=[]
	for i in a:
	    if i.text.startswith('hsa'):
	        x=str(i.text)
	        q.append(x)
	for i in a:
	    if i.text.startswith('MI0'):
	        y=str(i.text)
	        w.append(y)
	rpm=[]
	b=soup.find_all('td', {'class':'readCol'})
	for i in b:
	    j=i.text
	    if j=='RPM':
	        continue
	    rpm.append(j)

	chro=[]
	start=[]
	end=[]
	strand=[]
	ch=[]
	c=soup.find_all('td' , {'class':'chrCol', } )
	for i in c:
	    ch.append(i.text)
	for i in range(4, len(ch), 4):
	    chro.append(ch[i])
	for i in range(5, len(ch), 4):
	    start.append(ch[i])
	for i in range(6, len(ch), 4):
	    end.append(ch[i])
	for i in range(7, len(ch), 4):
	    strand.append(ch[i])

	lin=[]
	l=[]
	link= [a['href'] for a in soup.find_all('a', href=True)]
	for i in link:
	    if i.startswith('mirna'):
	        j= str(i)
	        lin.append(j)
	for i in range(0, len(lin) , 2):
	    l.append(lin[i])
	web=[]
	for i in range(len(l)):
		j='http://www.mirbase.org/cgi-bin/'+l[i]
		web.append(j)


	i=0

	for j,k,l,m,n,o,p,q in zip(q,w,rpm,chro,start,end,strand,web):
		print "Index no. :", i
		print"Id:" ,j
		print"Accession:" ,k
		print"RPM:" ,l
		print"Chromosome:" ,m
		print"Start:" ,n
		print"End:" ,o
		print"Strand:" ,p
		print"Wesbite:" ,q,'\n'

		i=i+1

	choose=int(raw_input(" Enter 1 to see the sequence \n Enter 2 to see the allignment of two sequences: "))
	try:
		if choose==1:
			response=int(raw_input("Enter the index number of the list of mirna to proceed:\n"))
			res=int(raw_input(" Enter the response to choose the options to output: \n Enter 1 for form= stem loop sequence, view = unaligned fasta format \n Enter 2 for form= mature, view = unaligned fasta format :  "))
			form=str()
			view=str()
			try:
				if res==1:
					view='fasta'
					form='precursor'
				if res==2:
					view='fasta'
					form='mature'
				else:
					print"wrong input"
			except:
				print" Wrong input. Please try again.\n"
			url= baseurl+'/cgi-bin/sequence_get.pl?accs='+ w[response] +'&type=' + form + '&view=' + view + '&FetchSequences=Fetch+Sequences&.cgifields=accs'
			data=urllib.urlopen(url).read()
			y=raw_input("Do you write this data to text file. If yes enter 'y' If no enter any key:")
			if y=='y':
				fn=w[response]+'.text'
				if os.path.isfile(fn):
					print "The file already exists in the working directory. If you write the data again delete the existing file\n"
				else:
					print"The file has been written and saved in your working directory\n"
					f=open(fn,'a')
					print data
					print>>f, data
			else:
				print data
		if choose==2:
			response1=int(raw_input("Enter the index number of the  first mirna for alignment\n"))
			response2=int(raw_input("Enter the index number of the second mirna for alignment:\n"))
			res=int(raw_input(" Enter the response to choose :\n 1 for stemloop mirna- stemloop mirna sequence pairwise alignment \n 2 for mature mirna - mature mirna sequence pairwise alignment: "))
			form=str()
			view=str()
			try:
				if res==1:
					view='fasta'
					form1='precursor'
					form2='precursor'
				if res==2:
					view='fasta'
					form1='mature'
					form2='mature'
				else:
					print"wrong input"
			except:
				print" Wrong input. Please try again.\n"
			url1= baseurl+'/cgi-bin/sequence_get.pl?accs='+ w[response1] +'&type=' + form1 + '&view=' + view + '&FetchSequences=Fetch+Sequences&.cgifields=accs'
			url2= baseurl+'/cgi-bin/sequence_get.pl?accs='+ w[response2] +'&type=' + form2 + '&view=' + view + '&FetchSequences=Fetch+Sequences&.cgifields=accs'
			data1=urllib.urlopen(url1).readlines()
			data2=urllib.urlopen(url2).readlines()
			for i,j in enumerate(data1):
				if i==1:
					seq1=j
			for i,j in enumerate(data2):
				if i==1:
					seq2=j
			print "mirna sequence 1:",seq1, "\n","mirna sequence 2:",seq2
			select=int(raw_input("Enter 1 for global alignment\nEnter 2 for local alignment: "))
			from Bio import pairwise2
			from Bio.pairwise2 import format_alignment
			try:
				if select==1:
					for a in pairwise2.align.globalxx(seq1, seq2):
						print(format_alignment(*a))
				if select==2:
					for a in pairwise2.align.globalxx(seq1, seq2):
						print(format_alignment(*a))
				else:
					print"wrong input"
			except:
				print" Wrong input. Please try again.\n"

		else:
			print"Wrong input, Try again"
	except:
		print"Wrong input. Please try again\n"



def protein():
	protname=raw_input("Enter the protein name (Protein name is alpha-numeric and alphabets should be in capital , and also enter the Organism name[ Currently available organisms are HUMAN and MOUSE] separated by '_' . eg. A1CF_HUMAN):")
	if protname=='':
		print"Your input is blank. Please try again"
		protein()
		return
	url=base_url+"/api/1.0/protein/"+protname
	datas=openweb(url)
	for i,j in datas.items():
		if i=="gene":
			print i ,":", j['symbol'], "\n"
			continue
		print i, " : " ,j,"\n"

def gene():
	genename=raw_input("Enter the gene name (Gene name is alpha-numeric and alphabets should be in capital):")
	if genename=='':
		print"Your input is blank. Please try again"
		gene()
		return
	url=base_url+"/api/1.0/gene/"+genename
	datas=openweb(url)
	for i,j in datas.items():
		if i=="proteins":
			for n in j:
				print i ,":", n['symbol'], "\n"
				continue
			continue
		if i=="hgncRootFamilies":
			print i ,":",
			for n in j:
				print  n['name'] ," |" ,
			continue
		if i=="synonyms":
			print"\n"
			print i ,":",
			for n in j:
				print  n," |" ,
			continue
		if i=="name":
			print "\n"
		print i, " : " ,j,"\n"

def genesets(link, fname):
	datas = openweb(link)
	data=datas.get("associations")
	res=raw_input("Do you want write the data in csv file format? If yes press 'y' , if no press any other key:")

	if res=='y':
		f=fname+".csv"
		fn=f.replace('/' , '-')
		if os.path.isfile(fn):
			print "The data file already exist in the working directory. If you want to write once again please delete the existing file"
		else:
			print"Your file has been written and saved in your working directory "
			f=open(fn, 'a')
			for n , k in enumerate(data):
				symbol=k["gene"].get("symbol")
				t=k.get("thresholdValue")
				s=k.get("standardizedValue")
				print>>f , n+1, ",", symbol, ",",  t ,",",  s
				print n+1, ",", symbol, ",",  t ,",",  s
	else:
		for n , k in enumerate(data):
			symbol=k["gene"].get("symbol")
			t=k.get("thresholdValue")
			s=k.get("standardizedValue")
			print n+1, ",", symbol, ",",  t ,",",  s



def datasets():
	a=[]
	b=[]
	url=base_url+"/api/1.0/dataset"
	datas=openweb(url)
	data=datas.get("entities")
	for n, k in enumerate(data):
		print n ,(k["name"])
		a.append(k["name"])
		b.append(k["href"])
	response=int(raw_input("Enter the index number of the dataset you want to open:"))
	url=base_url+b[response]
	a=[]
	b=[]
	datas= openweb(url)
	data=datas.get("geneSets")
	print "The description of the slected dataset is :\n","name:",datas["name"],"\n","association:",datas["association"],"\n","description:", datas["description"],"\n", "measurement:",datas["measurement"],"\n", "attributeGroup:", datas["attributeGroup"], "\n" ,"attributeType:",datas["attributeType"], "\n","pubMedIds:", datas["pubMedIds"]
	for n, k in enumerate(data):
		print n ,(k["name"])
		a.append(k["name"])
		b.append(k["href"])
	response=int(raw_input("Enter the index number of the gene sets you want to open:"))
	url=base_url+b[response]
	genesets(url, a[response])

print("Hi Welcome to Integrated Database for Human Genes, Proteins and miRNAs\nYou can search for :\n1. Datasets\n2. Gene \n3. Proteins \n4. miRNA")
repeat="y"
while(repeat=="y"):
	try:
		response=int(raw_input("Please Enter 1 for Datasets , 2 for Gene , 3 for Protein and 4 for miRNA:"))
		if response==1:
			datasets()
		elif response==2:
			gene()
		elif response==3:
			protein()
		elif response==4:
			mirna()
		else:
			print"Wrong input try again"
	except ValueError:
		print" Wrong input , please enter a number"

	repeat=raw_input('To make fresh search enter"y"  or enter any key to exit: ')
