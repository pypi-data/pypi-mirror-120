# CHK141 个人专用日志输出包
## 使用方法
### 导入包

```python
from Loggings import Loggings
```
### 初始化

```python
from Loggings import Loggings
loggings = Loggings.Loggings()
```

### 调用方法

```python
loggings = Loggings.Loggings()
logger = loger.Loggings()
if __name__ == '__main__':
    loggings.info("中文test")
    loggings.debug("中文test")
    loggings.warning("中文test")
    loggings.error("中文test")
    loggings.success("中文test")
```

### 输出结果
```sybase
2021-09-16 17:22:36.117 | INFO     | __main__:info:21 - 中文test
2021-09-16 17:22:36.117 | DEBUG    | __main__:debug:24 - 中文test
2021-09-16 17:22:36.117 | WARNING  | __main__:warning:27 - 中文test
2021-09-16 17:22:36.117 | ERROR    | __main__:error:30 - 中文test
2021-09-16 17:22:36.118 | SUCCESS  | __main__:success:33 - 中文test
```


