"""
电商用户数据分析
数据：69,555 条用户行为日志（浏览/收藏/购买）
目标：拆解 GMV 结构，比较营收贡献与流量贡献的差异
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

DATA = 'UserBehavior_2025.csv'

#1.数据读取
try:
    df = pd.read_csv(DATA, encoding = 'utf-8')
except UnicodeDecodeError:
    df = pd.read_csv(DATA, encoding = 'gbk')

#2.数据质量检查
print('形状（行，列）：', df.shape)
print('缺失值总数：',df.isna().sum().sum())
print('完全重复行',df.duplicated().sum())
print('\n行为分布：')
print(df['行为类型'].value_counts().to_string())

#3.时间处理
df['时间'] = pd.to_datetime(df['时间戳'], unit='s') + pd.Timedelta(hours=8)
df['日期'] = df['时间'].dt.strftime('%Y-%m-%d')
df['月份'] = df['时间'].dt.strftime('%Y-%m')
print('\n时间范围：',df['时间'].min(),'~',df['时间'].max())

#4.核心指标
buy = df[df['行为类型'] == 'buy'].copy()
gmv = buy['售价'].sum()
orders = len(buy)

print('\n核心指标')
print(f'成交笔数：{orders:,}')
print(f'GMV：{gmv:,.0f}元（{gmv/1e8:.2f}亿）')
print(f'客单价：{gmv/orders:,.2f}元')

#5.品类结构
cat = buy.groupby('商品类别')['售价'].agg(GMV='sum',笔数= 'count').sort_values('GMV',ascending=False)
cat['GMV占比%'] = (cat['GMV']/gmv*100).round(1)
cat['笔数占比%'] = (cat['笔数']/orders*100).round(1)
print('\n品类结构')
print(cat.to_string())

#6.月度GMV趋势
os.makedirs('output',exist_ok=True)
monthly = buy.groupby('月份')['售价'].sum().reset_index()

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

plt.figure(figsize=(12,6))
plt.plot(monthly['月份'],monthly['售价'],marker='o',linewidth=2)
plt.title('每月GMV趋势')
plt.xlabel('月份')
plt.ylabel('GMV（元）')
plt.xticks(rotation=0)
plt.grid(True,linestyle='--',alpha=0.5)
plt.tight_layout()
plt.savefig('output/UserBehavior_2025.png',dpi=150,bbox_inches='tight')
plt.show()