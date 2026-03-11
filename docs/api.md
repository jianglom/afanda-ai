# API 文档

## AFanDa 类

主类，用于创建阿-凡达实例。

### 初始化

```python
from afanda import AFanDa

ai = AFanDa(
    name="我的小凡",      # AI的名字
    user_id="user_001",   # 用户ID，用于情感记忆
    data_dir="./afanda_data"  # 数据存储目录
)


核心方法
think(user_input)
处理用户输入，返回回应。

python
response = ai.think("冬天买凉鞋合适吗？")
print(response)
get_emotion_state(target_type, target)
获取情感状态。

python
state = ai.get_emotion_state("thing", "凉鞋")
print(state)  # {"value": -75, "level": "scarred"}
authorize(domain)
申请专业授权。

python
ai.authorize("法律")
get_health()
获取健康状态。

python
health = ai.get_health()
print(health)  # {"state": "healthy", "alignment": 92.5}
save()
手动保存状态。

python
ai.save()