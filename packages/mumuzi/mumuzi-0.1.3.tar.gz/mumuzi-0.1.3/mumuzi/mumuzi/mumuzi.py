import base64
from . import py3base92
import binascii
import re
import random
import zipfile
import os
from .taoshenyulu import taoshenyulu


layer_pattern = re.compile(b'^This_is_layer_.*?_of_Matryoshka:')


def enc_to_txt_file(input_file,output_file,method):
	#output_file_type=txt,1 base64 2 base92 3 base85 4 文件hex	
	with open(input_file,'rb')as f:
		input_data=f.read()
	with open(output_file,'w')as f:
		if method==1:
			#1 base64
			f.write("This_is_layer_"+str(mumuzi.tao_layer)+"_of_Matryoshka:"+base64.b64encode(input_data).decode())
		elif method==2:
			#3 base85
			f.write("This_is_layer_"+str(mumuzi.tao_layer)+"_of_Matryoshka:"+base64.a85encode(input_data).decode())
		elif method==3:
			#2 base92
			f.write("This_is_layer_"+str(mumuzi.tao_layer)+"_of_Matryoshka:"+py3base92.base92_encode(input_data))
		elif method==4:
			# 文件hex
			f.write("This_is_layer_"+str(mumuzi.tao_layer)+"_of_Matryoshka:"+binascii.b2a_hex(input_data).decode())


def enc_to_zip_file(input_file,output_file,method):
	#output_file_type=zip,1 随机加密密码为可见3位随机字符 2 伪加密 
	layer="This_is_layer_"+str(mumuzi.tao_layer)+"_of_Matryoshka:"
	if method==1:
		password=''.join(random.sample('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',k=3))
		cmd='zip -P '+password+' '+output_file+' '+input_file
		#print(cmd)
		os.system(cmd)
		with open(output_file,'rb+')as f:
			old = f.read()
		with open(output_file,'wb')as f:
			f.write(layer.encode()+old)
	elif method==2:
		cmd='zip '+output_file+' '+input_file
		os.system(cmd)
		with open(output_file, 'rb') as f:
			r_all = f.read()
			r_all = bytearray(r_all)
			#  504B0304后的第3、4个byte改成0900
			index = r_all.find(b'PK\x03\x04')
			if not index:
				i = index + 4
				r_all[i + 2:i + 4] = b'\x09\x00'
			 #  504B0102后的第5、6个byte改成0900
			index1 = r_all.find(b'PK\x01\x02')
			if index1:
				print()
				i = index1 + 4
				r_all[i + 4:i + 6] = b'\x09\x00'
		with open(output_file, 'wb') as f1:
			f1.write(r_all)
		






def dec_txt_file(input_data,output_file):
	try:
		result=py3base92.base92_decode(input_data.replace(b'\\\\',b'\\').decode())
		if re.match(layer_pattern,result.encode()):
			with open(output_file,'wb')as f:
				f.write(result.encode())
		else:
			raise Exception('not base92')
	except:
		try:
			result=base64.a85decode(input_data)
			if re.match(layer_pattern,result):
				with open(output_file,'wb')as f:
					f.write(result)
			else:
				raise Exception('not base85')
		except:
			try:
				result=base64.b64decode(input_data)
				if re.match(layer_pattern,result):
					with open(output_file,'wb')as f:
						f.write(result)
				else:
					raise Exception('not base64')
			except:
				try:
					result=binascii.b2a_hex(input_data)
					if re.match(layer_pattern,result):
						with open(output_file,'wb')as f:
							f.write(result)
					else:
						raise Exception('not base16')
				except:
					pass


class mumuzi:
	'大家最爱的mumuzi'
	tao_layer=0
	talk_count=0
	name="mumuzi"
	description="我是大家最爱的mumuzi，你可以叫我ctf全栈全自动解题姬哟~"
	def __init__(self):
		print(mumuzi.description)

	def talk(self):
		'跟神说话'
		print(random.choice(taoshenyulu))
		mumuzi.talk_count=mumuzi.talk_count+1

	def tao(self,input_file,layer):
		'套题'
		
		if mumuzi.tao_layer>mumuzi.talk_count:
			print('mumuzi:\n\t麻了\nmumuzi:\n\t还要冲一次\nmumuzi:\n\t腿已经软了')
			return
		print("This_is_layer_"+str(mumuzi.tao_layer)+"_of_Matryoshka")
		mumuzi.tao_layer=mumuzi.tao_layer+1
		output_file_type=random.choice(['zip','txt'])

		#output_file_type='txt'
		output_file=input_file.split('.')[0]+'.tao'+str(mumuzi.tao_layer)
		#output_file_type=PNG,1 文件尾后额外字符串 2 随机顺序隐写LSB 3 全文件按字节XOR 4 全文件倒序 
		#output_file_type=zip,1 随机加密密码为可见3位随机字符 2 伪加密 3 全文件按字节XOR 4 全文件倒序 
		#output_file_type=txt,1 base64 2 base92 3 base85 4 文件hex
		if output_file_type=='txt':
			if mumuzi.tao_layer>50:
				enc_to_txt_file(input_file,output_file,random.randint(1,4))
			else:
				enc_to_txt_file(input_file,output_file,random.randint(2,3))
			return(output_file)
		if output_file_type=='zip':
			enc_to_zip_file(input_file,output_file,random.randint(1,2))
			return(output_file)
	
	def solve(self,input_file):
		"解决套题"
		if mumuzi.tao_layer>mumuzi.talk_count:
			print('mumuzi:\n\t麻了\nmumuzi:\n\t还要冲一次\nmumuzi:\n\t腿已经软了')
			return
		mumuzi.tao_layer=mumuzi.tao_layer+1
		with open(input_file,'rb') as f:
			layer_data_b=f.read()
			re_result=re.match(layer_pattern,layer_data_b).group(0)
		if re_result:
			current_layer=re_result.decode().split('_')[3]
		else:
			answers=['你菜',"给你一棍子","洗洗睡"]
			print('mumuzi:\n\t'+random.choice(answers))
			return
		output_file=input_file.split('.')[0]+'.layer'+str(int(current_layer)-1)
		print('Solving_'+current_layer+'_layer...')
		file_data_b=layer_data_b.lstrip(re_result)
		bins=binascii.b2a_hex(file_data_b[:20]).decode()
		if bins[:12]=='504b03041400':
			file_type='zip'
		elif bins[:16]=='89504e470d0a1a0a':
			file_type='png'
		else:
			file_type='txt'
		print('This_layer_seems_to_be_'+file_type+'...')
		if file_type=='txt':
			dec_txt_file(input_data=file_data_b,output_file=output_file)
			return(output_file)

#taoshen=mumuzi
#taoshen.solve(0,'flag.tao4')
#flag='flag.txt'
#for i in range(50):
#	taoshen.talk(0)
#	flag=taoshen.tao(0,flag,1)
