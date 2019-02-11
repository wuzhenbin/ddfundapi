

from utils import *
from pyecharts import Line

code = '005114'

res = read({'fcode': code})
name = res['title']


attr = [item['FSRQ'] for item in res['time_val_list']]
v1 = [item['DWJZ'] for item in res['time_val_list']]


line = Line(name,width='100%',height=800,renderer='svg')
line.add("单位净值", 
	attr, v1, 
	is_smooth=True, 
	yaxis_max='dataMax',
	yaxis_min='dataMin',
	is_xaxis_boundarygap=False,
	is_yaxis_boundarygap=False
)

line.show_config()
line.render()





