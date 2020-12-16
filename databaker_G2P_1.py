import os
import re
import numpy as np
from tqdm import tqdm



def write_metadata(metadata, out_dir):
	os.makedirs(out_dir, exist_ok=True)
	with open(os.path.join(out_dir, 'train.txt'), 'w', encoding='utf-8') as f:
		for m in tqdm(metadata):
			f.write('|'.join([str(x) for x in m]) + '\n')
		print('len:', len(metadata))
	return True



def build_from_path_CN(input_path, use_prosody):
	content = _read_labels(input_path)
	# databaker:
	# 002387	毛#2一般#1为#1白色#3只是#1两个#1耳壳#3眼圈#3肩部#3四肢#1为#1黑色#4
	# 			mao2 yi4 ban1 wei2 bai2 se4 zhi3 shi4 liang3 ge5 er3 ke2 yan3 quan1 jian1 bu4 si4 zhi1 wei2 hei1 se4
	metadata = []
	num = int(len(content)//2)
	for idx in range(num):
		res = _parse_cn_prosody_label(content[idx*2], content[idx*2+1], use_prosody)
		if res is not None:
			basename, text = res
			metadata.append([basename, text])
		break
	return metadata



def _read_labels(input_path):
	# 从多个文件读入, 改为指定一个文件读入, 因此有些冗余
	files = []
	files.append(input_path)
	
	# load from all files
	labels = []
	for item in files:
		with open(item, 'r', encoding='utf-8') as f:
			for line in f:
				line = line.strip()
				if line != '': labels.append(line)
	return labels



def _parse_cn_prosody_label(text, pinyin, use_prosody=False):
	"""
	Parse label from text and pronunciation lines with prosodic structure labelings
	
	Input text:    100001 妈妈#1当时#1表示#3，儿子#1开心得#2像花儿#1一样#4。
	Input pinyin:  ma1 ma1 dang1 shi2 biao3 shi4 er2 zi5 kai1 xin1 de5 xiang4 huar1 yi2 yang4
	Return sen_id: 100001
	Return pinyin: ma1-ma1 dang1-shi2 biao3-shi4, er2-zi5 kai1-xin1-de5 / xiang4-huar1 yi2-yang4.

	Args:
		- text: Chinese characters with prosodic structure labeling, begin with sentence id for wav and interval file
		- pinyin: Pinyin pronunciations, with tone 1-5
		- use_prosody: Whether the prosodic structure labeling information will be used

	Returns:
		- (sen_id, pinyin&tag): latter contains pinyin string with optional prosodic structure tags
	"""

	text = text.strip()
	pinyin = pinyin.strip()
	if len(text) == 0:
		return None

	# remove punctuations
	text = re.sub('[“”、，。：；？！—…#（）]', '', text)

	# split into sub-terms
	sen_id, texts  = text.split()
	phones = pinyin.split()

	# prosody boundary tag (SYL: 音节, PWD: 韵律词, PPH: 韵律短语, IPH: 语调短语, SEN: 语句)
	SYL = '-'
	PWD = ' '
	PPH = ' / ' if use_prosody==True else ' '
	IPH = ', '
	SEN = '.'

	# parse details
	pinyin = ''
	i = 0 # texts index
	j = 0 # phones index
	b = 1 # left is boundary
	while i < len(texts):
		if texts[i].isdigit():
			if texts[i] == '1': pinyin += PWD  # Prosodic Word, 韵律词边界
			if texts[i] == '2': pinyin += PPH  # Prosodic Phrase, 韵律短语边界
			if texts[i] == '3': pinyin += IPH  # Intonation Phrase, 语调短语边界
			if texts[i] == '4': pinyin += SEN  # Sentence, 语句结束
			b  = 1
			i += 1
		elif texts[i]!='儿' or j==0 or not _is_erhua(phones[j-1][:-1]): # Chinese segment
			if b == 0: pinyin += SYL  # Syllable, 音节边界（韵律词内部）
			pinyin += phones[j]
			b  = 0
			i += 1
			j += 1
		else: # 儿化音
			i += 1

	return (sen_id, pinyin)

def _is_erhua(pinyin):
	"""
	Decide whether pinyin (without tone number) is retroflex (Erhua)
	"""
	if len(pinyin)<=1 or pinyin == 'er':
		return False
	elif pinyin[-1] == 'r':
		return True
	else:
		return False


