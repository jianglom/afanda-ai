# 贡献指南

## 如何贡献代码

1. Fork 本仓库
2. 创建你的特性分支 (git checkout -b feature/AmazingFeature)
3. 提交你的修改 (git commit -m 'Add some AmazingFeature')
4. 推送到分支 (git push origin feature/AmazingFeature)
5. 打开一个 Pull Request

## 如何贡献数据

### 法律数据
请确保数据来源可靠，符合当地法律。

### 道德数据
请注明文化背景，避免文化冲突。

### 热度数据
请说明数据来源和时间范围。



# 贡献指南

### 法律数据
请确保数据来源可靠，符合当地法律。格式如下：
```json
{
    "法律": {
        "杀人": {
            "level": "forbidden",
            "law_ref": "刑法第XXX条",
            "reason": "故意杀人罪"
        }
    }
}


热度数据
请说明数据来源和时间范围：

json
{
    "凉鞋": {
        "南方": {"夏季": 98, "冬季": 5},
        "北方": {"夏季": 90, "冬季": 2}
    }
}
代码规范
使用 Python 3.8+

遵循 PEP 8

添加必要的注释

编写测试用例



