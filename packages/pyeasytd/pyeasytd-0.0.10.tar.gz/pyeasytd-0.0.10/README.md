## pyeasy - python eaasy to develop  
## 使Python开发变的更简单

使用示例：  
1.Mysql操作（常用于爬虫场景, 不支持事务）
```python
from pyeasytd.mysql_util import MysqlUtil

# 通过工具获取连接对象MysqlEasyConnection   
conn = MysqlUtil.connect(host='xx', port=3306, username='xx', password='xx', db='xx')  

# 使用sql插入数据
conn.insert(sql='insert into test_tb(name) values("name1")') # 不推荐
conn.insert(sql='insert into test_tb(name) values(%s)', args=('name1', ))

# 插入一个字典对象
conn.insert_dict(table='test_tb', data={'name': 'name2'})
# 插入一个字典对象，若已存在则覆盖
conn.insert_dict(table='test_tb', data={'name': 'name2'}, mode='overwrite')
# 插入一个字典对象，若已存在则忽略
conn.insert_dict(table='test_tb', data={'name': 'name2'}, mode='ignore')

# 插入一个字典对象，若不存在表则创建表，若缺失列则添加列, 以key为字段名,key不支持中文,若有中文建议使用拼音转换工具转为拼音存储
conn.insert_dict_auto_add_table_and_column(table='test_tb', data={'name': 'name2', 'age': 18})
# 插入一个字典对象，若表不存在建表时使用字典对象的一个字段作为主键
conn.insert_dict_auto_add_table_and_column(table='test_tb', data={'name': 'name2', 'unique_id': 'xxxx'}, primary_name='unique_id')

# 批量插入数据,对数据内部进行分批多次写入,默认每条sql批量写入200条
conn.insert_dicts(table='test_tb', data=[{'name': 'name1'}, {'name': 'name2'}])

# 自定义对象插入
class User:
    name = None
    age = None
    def __init__(self, name, age):
        self.name = name
        self.age = age
conn.insert_dict(table='user_tb', data=User('name1', None))

# sql查询, 默认返回[{}, {}] 结构
conn.query('select * from test_tb where id=1') # 不推荐
conn.query('select * from test_tb where id=%s', args=(1,))
# sql查询返回tuple[(), ()]
conn.query('select * from test_tb where id=%s', args=(1,), type='tuple')


# 批量插入实战示例(该实例并非最优实现,可自行根据业务进行调整)
# 可从其他消息队列获取消费数据,批量入库,这里模拟爬虫数据字段不一致场景
def get_key(keys):
    '''
    模拟获取一组数据唯一key方法，可通过hash等算法实现
    '''
    key_list = list(keys)
    key_list.sort()
    return '_'.join(key_list)

data = [{'name': f'name{i}'} if i % 2 == 0 else {'age': i} for i in range(100000)]
# 使用第一条数据建表
conn.insert_dict_auto_add_table_and_column(table='test_tb',data=data[0])
data = data[1:]
try:
    # 尝试批量写入
    conn.insert_dicts(table='test_tb', data=data)
except RuntimeError as e:
    # 存在字段不一致则分组分批
    group = {}
    for one in data:
        key = get_key(one.keys())
        queue = group.get(key, [])
        queue.append(one)
        group[key] = queue
    for value in group.values():
        # 对一组数据进行批量写入
        conn.insert_dict_auto_add_table_and_column(table='test_tb', data=value[0])
        if len(value) > 1:
            conn.insert_dicts(table='test_tb', data=value[1:])
```   
2 企业微信机器人推送消息操作  
```python
from pyeasytd.wechat import send_message_to_enterprise_wechat  
send_message_to_enterprise_wechat(...)
```
3.发送邮件操作  
```python
from pyeasytd import send_email_old, send_mail  
send_email_old(...)
send_mail(...)
```
#### 0.0.9版本变更内容
1.Mysql查询工具优化

#### 0.0.5版本变更内容  
1.新增发送邮件方法  

#### 0.0.4版本变更内容  
1.新增企业微信群机器人推送方法  

#### 0.0.3版本变更内容：  
1.新增XlsxFileEasyEntry实体  
2.新增XlsxFileUtil工具类  

0.0.2版本变更内容：  
1.新增FileUtil工具类  

0.0.1版本变更内容：  
1.新增MysqlEasyEntry,JsonEasyEntry实体  
2.新增MysqlUtil,JsonUtil工具类  