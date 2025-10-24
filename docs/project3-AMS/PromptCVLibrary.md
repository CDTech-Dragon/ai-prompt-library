
2025-10-22  12：10
--------------------------
## 我们现在建立了一个这样的目录（D:\AI\Project3_EMS\ems_web\ems_web\server\iot-sync），就放入相关的脚本 文件，主要功能是通过运行ems_web\server\iot-sync\iot_sync_service.js这个主服务，来实现对IOT系统同步接口数据到定时存放到指定服务器的功能：
#### 1、第一步：阅读其文件夹中所有文件的内容，熟悉其功能；
#### 2、第二步：先测试iot_sync_service.js能否在这个环境中实现功能；
#### 3、第三步：我需要在主页面九宫格的第三格建立 AMS（智能警报系统），是否能将对应的服务功能放在/servr/下的ems_web\server\pcmonitor-service.js中一并撰写脚本，还是要单独写一个iot_sync类的脚本；
#### 4、第四步：最后无论是pcmonitor-service.js还是单独写的iot_sync.js脚本，我们需要把iot_sync_service.js这个同步脚本放在主服务脚本中运行，这样我们就不用运行太多多的服务！
最后，这些步骤一步步确认成功后，再执行下一步，另外在第三个九宫格的位置在链接前端页面时，类似iot_sync.vue文件暂不要写具体的代码，等获取数据成功后和接口创建后我再单独给实施步骤和详细要求


#### 1、现在在主页面九宫格的第三格建立 AMS（智能警报系统），如果后段涉及要增加的服务是否还是可以建立ems_web\server\pcmonitor-service.js中；
#### 2、前端页面主要实现的显示标准字段以及前后字段对应关系有：
       警灯编号               警灯位置                  报警时长                                                 报警次数                                                           更新时间                                         //前端名字
        dut_id                 device_id                 duration               需要分别统计device_id在查询时间范围的出现次数                     updated                                        //后端对应
## 特别要求：
2.1：警灯位置/ device_id（需要映射devices表中device_name用来显示中文；其他字段在alarms表中获取对应数据；
2.2：报警次数/ 需要分别统计device_id在查询时间范围的出现次数（需要针对yellow和red实现分开统计），具体实现yellow和red可以在页头标准设定  yellow和red以及All的圆色控键对应 颜色报警数据的对应显示 ; 
3、标题菜单要有按警灯位置、警灯编号的模糊查找功能；
4、具体返回主页面按钮 和导出CSV功能按钮；要有时间起止选择框功能，默认时间为前一天的00:00:00到今天日期的23:59:59，全部使用标准北京时间格式设定与查询；
5、a、针对 报警时长 可以实现双击点开查询详情页对应alarms表中的具体 发生 `type` 、`start`、`end`、duration、updated信息；b、而针对报警次数要有去重功能，只显示对应alarms表中在设定查询时间范围内的具体 条目数的合计，同样要有双击可以查看详情页功能：
并对应可以查看： `start`、`end`、duration、updated信息；c、因为报警次数有去重机制，所以报警时长 在记录行首页只能显示当前   device_id 当前查询时间范围内报警时长最长的一条记录；
6、所有前端字段可以实现单击升降排序功能；
7、整体页面科技感风格可以与http://localhost/pcmonitor页面风格保持类似；

==========================
## UI要求
-----------------------------------------------
请充分参考ems_web\src\views\pcmonitor\index.vue文件中css的界面风格完成当前http://localhost/ams-alarm页面的UI，主要要求有：
#### 1、页面 主系统名称的 抬头的字体大小 ，蓝底白字主格调；
#### 2、前端页面主标准字段的大小 ，蓝底白字要求；
#### 3、分页功能要求与样式一样参考过来；
-----------------------------------------------
现问题了！.env.development中VITE_APP_BASE_API设置为'/dev-api'，但我们的API代理是直接使用'/api/ams-alarm'。让我修改index.vue，在API调用中添加配置跳过baseURL。

ems_web\src\views\ams-alarm\index.vue
