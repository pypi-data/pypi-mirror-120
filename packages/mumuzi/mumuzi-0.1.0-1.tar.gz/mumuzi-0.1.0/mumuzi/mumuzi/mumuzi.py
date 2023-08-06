import base64
from . import py3base92
import binascii
import random



def enc_to_txt_file(input_file,output_file,method):
	#output_file_type=txt,1 base64 2 base92 3 base85 4 文件hex	
	with open(input_file,'rb')as f:
		input_data=f.read()
	with open(output_file,'w')as f:
		if method==1:
			#1 base64
			f.write("This_is_layer_"+str(mumuzi.tao_layer)+"_of_Matryoshka:"+base64.b64encode(input_data).decode())
		elif method==2:
			#2 base92
			f.write("This_is_layer_"+str(mumuzi.tao_layer)+"_of_Matryoshka:"+py3base92.base92_encode(input_data))
		elif method==3:
			#3 base85
			f.write("This_is_layer_"+str(mumuzi.tao_layer)+"_of_Matryoshka:"+base64.a85encode(input_data).decode())
		elif method==4:
			# 文件hex
			f.write("This_is_layer_"+str(mumuzi.tao_layer)+"_of_Matryoshka:"+binascii.b2a_hex(input_data).decode())


def dec_txt_file(input_file,output_file,method):
	pass

class mumuzi:
	'大家最爱的mumuzi'
	version='0.1.0'
	name="mumuzi"
	tao_layer=0
	description="我是大家最爱的mumuzi，你可以叫我ctf全栈全自动解题姬哟~"
	def __init__(self):
		print(mumuzi.description)

	def talk(self):
		'跟神说话'
		taoshenyulu=["mumuzi:\n\t你阳寿没了",
		"mumuzi:\n\t你阳寿阴寿都没了",
		"mumuzi:\n\t哈哈,大家聊了这么多啊，刚刚在厕所奖励了自己12个小时晕过去了,现在刚醒，看到群里发的涩图又得奖励自己了"
		]
		print(random.choice(taoshenyulu))

	def tao(self,input_file,layer):
		'套题'
		print("This_is_layer_"+str(mumuzi.tao_layer)+"_of_Matryoshka")
		mumuzi.tao_layer=mumuzi.tao_layer+1
		#out_put_file_type=random.choice(['png','zip','txt'])
		output_file_type='txt'
		output_file=input_file.split('.')[0]+'.tao'+str(mumuzi.tao_layer)
		#output_file_type=PNG,1 文件尾后额外字符串 2 随机顺序隐写LSB 3 全文件按字节XOR 4 全文件倒序 
		#output_file_type=zip,1 随机加密密码为可见3位随机字符 2 伪加密 3 全文件按字节XOR 4 全文件倒序 
		#output_file_type=txt,1 base64 2 base92 3 base85 4 文件hex
		if output_file_type=='txt':
			enc_to_txt_file(input_file,output_file,random.randint(1,4))
			return(output_file)


