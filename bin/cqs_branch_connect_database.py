# -*- coding: utf-8 -*-
# 2016/7/20 15:37
"""
-------------------------------------------------------------------------------
Function:   支管连接表的数据库程序
Version:    1.0
Author:     SLY
Contact:    slysly759@gmail.com 
 
-------------------------------------------------------------------------------
"""
import cx_Oracle
from openpyxl import load_workbook
def get_connectionid():
    conn = cx_Oracle.connect("apps/apps@192.168.15.94:1539/NRCRP2")
    cur =conn.cursor()
    r= cur.execute("select max(connection_id) from CUX.CUX_CQS_BRANCH_CONNECT_HIS_T")
    conn_id=[]
    for row in cur:
        conn_id.extend(row)
    print('数据库中最大的Conn_ID为')
    print(max(conn_id))
    return max(conn_id)

def get_batch_id():
    conn = cx_Oracle.connect("apps/apps@192.168.15.94:1539/NRCRP2")
    cur =conn.cursor()
    r= cur.execute("select max(batch_id) from CUX.CUX_CQS_BRANCH_CONNECT_HIS_T")
    result=cur.fetchone()
    new_result=list(result)
    return new_result[0]

def get_order_number():
    conn = cx_Oracle.connect("apps/apps@192.168.15.94:1539/NRCRP2")
    cur =conn.cursor()
    r= cur.execute("select conn_order_number from CUX.CUX_CQS_BRANCH_CONNECT_HIS_T")
    conn_id=[]
    for row in cur:
        conn_id.extend(row)
    print('数据库中最大的conn_order_number为')
    print(max(conn_id))
    return max(conn_id)

def insert_db(row):
    conn = cx_Oracle.connect("apps/apps@192.168.15.94:1539/NRCRP2")
    cur =conn.cursor()
    r=cur.execute("truncate table CUX.CUX_CQS_BRANCH_CONNECT_T")
    r=cur.executemany(" INSERT INTO CUX.CUX_CQS_BRANCH_CONNECT_T values (:CONNECTION_ID,:BATCH_ID,:CONN_ORDER_NUMBER,:PIPING_MATL_CLASS,:BRANCH_DN,:HEADER_DN,:CONNECTION_TYPE,:CREATED_BY,to_date(:CREATION_DATE,'yyyy/mm/dd'),:LAST_UPDATED_BY,to_date(:LAST_UPDATE_DATE,'yyyy/mm/dd'),:LAST_UPDATE_LOGIN,:ATTRIBUTE_CATEGORY,:ATTRIBUTE1,:ATTRIBUTE2,:ATTRIBUTE3,:ATTRIBUTE4,:ATTRIBUTE5,:ATTRIBUTE6,:ATTRIBUTE7,:ATTRIBUTE8,:ATTRIBUTE9,:ATTRIBUTE10,:ATTRIBUTE11,:ATTRIBUTE12,:ATTRIBUTE13,:ATTRIBUTE14,:ATTRIBUTE15)", row)
    r=cur.execute("insert into  CUX.CUX_CQS_BRANCH_CONNECT_HIS_T select * from CUX.CUX_CQS_BRANCH_CONNECT_T")
    conn.commit()
    print('数据已经导入成功')

def insert_batch_db(today_time):
    header_name=['BATCH_ID', 'COMMENTS', 'CREATION_DATE', 'LAST_UPDATE_DATE', 'CREATED_BY',
                 'LAST_UPDATED_BY', 'LAST_UPDATE_LOGIN', 'ATTRIBUTE_CATEGORY', 'ATTRIBUTE1', 'ATTRIBUTE2',
                 'ATTRIBUTE3', 'ATTRIBUTE4', 'ATTRIBUTE5', 'ATTRIBUTE6', 'ATTRIBUTE7', 'ATTRIBUTE8',
                 'ATTRIBUTE9', 'ATTRIBUTE10', 'ATTRIBUTE11', 'ATTRIBUTE12', 'ATTRIBUTE13',
                 'ATTRIBUTE14', 'ATTRIBUTE15']
    COMMENTS=input('请输入一段描述方便自己日后恢复数据,如果是续传请随意填写不会导入到数据库:')
    BATCH_ID=get_batch_id()
    CREATION_DATE=today_time;LAST_UPDATE_DATE=today_time
    data=[]
    CREATED_BY=0;LAST_UPDATED_BY=0
    LAST_UPDATE_LOGIN=1
    data.append(BATCH_ID);data.append(COMMENTS);data.append(CREATION_DATE);data.append(LAST_UPDATE_DATE)
    data.append(CREATED_BY);data.append(LAST_UPDATED_BY);data.append(LAST_UPDATE_LOGIN)#目前没想到追加的好方式，打算自己造一个轮子批量append
    row=dict(zip(header_name,data))
    print(row)
    conn = cx_Oracle.connect("apps/apps@192.168.15.94:1539/NRCRP2")
    cur =conn.cursor()
    r=cur.execute(" insert into cux.cux_cqs_batchs_t(BATCH_ID,COMMENTS,CREATION_DATE,LAST_UPDATE_DATE,CREATED_BY,LAST_UPDATED_BY,LAST_UPDATE_LOGIN) values (:BATCH_ID,:COMMENTS,to_date(:CREATION_DATE,'yyyy/mm/dd'),to_date(:LAST_UPDATE_DATE,'yyyy/mm/dd'),:CREATED_BY,:LAST_UPDATED_BY,:LAST_UPDATE_LOGIN)", row)
    conn.commit()
    print('数据已经导入成功')








