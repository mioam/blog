---
title: Hydra和Omegaconf
date: 2026-03-09 00:00:00
tags: []
categories: 学习笔记
---

最近写代码，模型需要的配置越来越复杂，所以需要看看有没有合适的现成的config。

(Omegaconf)[https://omegaconf.readthedocs.io/en/latest/usage.html] 和hydra (https://hydra.cc/docs/intro/) 都是非常常用的配置管理库。其中hydra是基于 Omegaconf 的。这篇文章主要记录一下 Omegaconf 提供的功能。

### Omegaconf

Omegaconf 的核心就是实现了一个 Omegaconf 类, 支持 str, int, bool, float bytes, 和 Enum 作为字典的关键字。这个类可以是dict，也可以是list。

```python
from omegaconf import OmegaConf
conf = OmegaConf.create({"k" : "v", "list" : [1, {"a": "1", "b": "2", 3: "c"}]})
```

同时支持对象风格和dict风格的访问，也支持修改。

```python
conf.server.port
conf['log']['rotation']
conf.users[0]
conf.get('missing_key', 'a default value')
```

Omegaconf 支持与 YAML、dot-list 、piclkle 等的转换

```python
conf = OmegaConf.create({"foo": 10, "bar": 20, 123: 456})
with tempfile.NamedTemporaryFile() as fp:
    OmegaConf.save(config=conf, f=fp.name)
    loaded = OmegaConf.load(fp.name)
    assert conf == loaded
```

也可以直接从命令行参数中获得 Omegaconf。

```python
conf = OmegaConf.from_cli()
```

structured config
支持运行时类型安全和静态类型标注

支持interpolation，使用 `${xxx}` 引用其他配置的值。也支持自定义resolver

```python
cfg = OmegaConf.create(
   {
       "plans": {
           "A": "plan A",
           "B": "plan B",
       },
       "selected_plan": "A",
       "plan": "${plans[${selected_plan}]}",
   }
)
```

支持合并

```python
conf = OmegaConf.merge(base_cfg, model_cfg, optimizer_cfg, dataset_cfg)
```

可以设置只读或struct

```python
OmegaConf.set_readonly(conf, True)
OmegaConf.set_struct(conf, True)
```
