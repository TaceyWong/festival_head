#  Festival Head节日头像

当前，控制台：

```bash
python console_app.py xxx.jpg
```

例1：单个人头
原图:![](1.jpg)
```bash
#输出
Find  1 face(s)
Result:
 -relpath: ./665b2e1a-4b8d-44dc-aa51-ba64635fd46a.png
 -abspath: /home/tacey/PycharmProjects/festival_head/665b2e1a-4b8d-44dc-aa51-ba64635fd46a.png
 ```
 生成结果：![](665b2e1a-4b8d-44dc-aa51-ba64635fd46a.png)

例2：多个人头
原图：![](2.jpg)
```bash
Find  5 face(s)
Result:
 -relpath: ./c0ae5035-95c1-4f0b-b7af-7c057fa60046.png
 -abspath: /home/tacey/PycharmProjects/festival_head/c0ae5035-95c1-4f0b-b7af-7c057fa60046.png
 ```
 生成结果：![](c0ae5035-95c1-4f0b-b7af-7c057fa60046.png)





### 第一阶段目标

完成基础核心节日头像生成功能，控制台应用


###  第二阶段目标

提供Web API 功能，图片保留一段时间，加调度任务定时删除。



### 第三阶段目标



+ 一种选择：提供一般Web界面进行操作
+ 另一种选择：提供web公众号服务
