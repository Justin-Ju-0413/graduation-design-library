# -*- coding: utf-8 -*-
import pandas as pd
df = pd.read_excel('C:/Users/16084/Desktop/sample_courseEng_xq/2026042621592917_filled.xlsx')
print('=== 前10行预览 ===')
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)
pd.set_option('display.max_colwidth', 40)
print(df.head(10).to_string())
print(f'\n总行数: {len(df)}')
print(f'英文课程名非空: {df["英文课程名"].notna().sum()}')
print(f'英文分数非空: {df["英文分数"].notna().sum()}')
print(f'英文学分非空: {df["英文学分"].notna().sum()}')
print(f'英文学时非空: {df["英文学时"].notna().sum()}')
print(f'英文课程类别非空: {df["英文课程类别"].notna().sum()}')

# 按学期分组统计
print('\n=== 各学期课程数 ===')
for term, group in df.groupby('中文学期'):
    print(f'{term}: {len(group)}门')
