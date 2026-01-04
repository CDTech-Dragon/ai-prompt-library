# 设备告警监控系统 - 项目提示词整理

## 🛠️ 技术栈
- **后端**: Node.js + Express.js
- **数据库**: MySQL 8.0
- **前端**: HTML5 + Bootstrap 5 + JavaScript
- **服务器端口**: 3003
- **数据库连接池**: mysql2

## 2024-12-18 会话记录 报警首页实现
请开发“Cdtech机台报警监控系统”页面，以下是界面与功能的详细文字描述（需100%还原）：

### 一、页面顶部区域（固定导航栏，背景色为深蓝色#1E40AF）
1. **左侧标题**：白色文字“Cdtech机台报警监控系统”，字体加粗。
2. **返回主页按钮**：紧邻标题右侧，浅蓝色背景#3B82F6、白色文字“返回主页”，带小房子图标。
3. **日期范围选择器**：
   - 标签文字“日期范围:”（白色），后跟两个输入框，默认显示“2025-12-01 00:00:00”至“2025-12-22 16:48:48”，输入框为白色背景，带日历图标。
4. **筛选下拉框组**（白色背景、灰色边框）：
   - 标签“车间:” + 下拉框（默认选中“全部”）；
   - 标签“线别:” + 下拉框（默认选中“全部线别”）；
   - 标签“机型:” + 下拉框（默认选中“全部机型”）；
5. **搜索区域**：
   - 标签“搜索:” + 输入框（提示文字“机台、资产编号、责任人、线别、机型...”），右侧带放大镜图标。
6. **快捷筛选标签栏**（白色背景）：
   - 标签“地域:” + 三个标签按钮（“全部”“SZ”“HN”，默认选中“全部”，选中时背景为深蓝色#1E40AF、文字白色）；
   - 标签“类型:” + 四个标签按钮（“全部”“SMT”“测试”“其它”，默认选中“全部”）；
   - 标签“状态:” + 三个标签按钮（“全部”“在用”“未用”，默认选中“全部”）；
7. **操作按钮组**：
   - 蓝色“查询”按钮、灰色“清除”按钮、红色“报障”按钮（右上角带红色数字“3”提示角标）；
8. **右上角时间**：橙色背景、白色文字“上午好! 12/22 11:09”。


### 二、数据表格区域（白色背景，外框1px灰色边框）
1. **表格统计行**：左侧灰色背景条带，显示“记录: 186”（黑色文字）。
2. **表头行**（背景色#E8F4FC，文字加粗、居中）：
   列依次为：序号、机台名称、资产编号、地域、责任人、车间、线别、机型、生产数量、黄灯最长报警时间、红灯最长报警时间、黄灯次数、红灯次数、报警总数、问题点、落实状态、更新时间。
3. **表格内容行（共20行，为第1-20条数据）**：
   - 行1：
     序号1 | 机台名称“小Y轴” | 资产编号“ZLT-3519” | 地域“SZ” | 责任人“李光” | 车间“B41” | 线别“A1-10” | 机型“未知” | 生产数量“0” | 黄灯最长“00:00:00” | 红灯最长“00:00:00” | 黄灯次数“0”（绿色） | 红灯次数“5290”（红色） | 报警总数“5290” | 问题点“1” | 落实状态“NG”（红色文字+红点前缀） | 更新时间“2025-12-22 10:37:59”
   - 行2：
     序号2 | 机台名称“小Y轴带飞达” | 资产编号“HNZ-01330” | 地域“HN” | 责任人“向学” | 车间“HN” | 线别“A1-14” | 机型“未知” | 生产数量“0” | 黄灯最长“00:00:00” | 红灯最长“00:00:00” | 黄灯次数“0”（绿色） | 红灯次数“1925”（红色） | 报警总数“1925” | 问题点“2” | 落实状态“NG”（红色） | 更新时间“2025-12-22 16:48:48”
   - 行3：
     序号3 | 机台名称“小Y轴” | 资产编号“ZLT-3524” | 地域“SZ” | 责任人“李光” | 车间“B41” | 线别“A1-05” | 机型“未知” | 生产数量“0” | 黄灯最长“00:00:00” | 红灯最长“00:00:00” | 黄灯次数“0”（绿色） | 红灯次数“213”（红色） | 报警总数“213” | 问题点“0” | 落实状态“无问题”（绿色文字+绿点前缀） | 更新时间“2025-12-21 08:26:25”
   - 行4至行20：数据与上述格式一致，需按截图中字段值完整填充（如行5：机台名称“01159-26号机”、黄灯次数“67”（粉色）、红灯次数“125”（红色）等）。


### 三、页面底部区域
1. **分页栏**（居中显示）：
   - 左侧文字“共186条记录，第1-20条”；
   - 中间下拉框“20条/页”；
   - 右侧按钮：“首页”“上一页”（置灰）、页码“1”（红底白字）“2”“3”“4”“5”“-”“10”、“下一页”；


## 2024-12-18 会话记录 报警首页数据展示接口

### 接口地址
`http://localhost:3003/api/alarms`

### SQL脚本
```sql
SELECT 
    ANY_VALUE(v1.device_name) AS device_name,
    v1.dev_assetno,
    ANY_VALUE(v1.dev_area) AS dev_area,
    ANY_VALUE(v1.dev_firstperson) AS dev_firstperson,
    ANY_VALUE(v1.dev_workshop) AS dev_workshop,
    ANY_VALUE(v1.dev_line) AS dev_line,
    ANY_VALUE(v1.Model) AS Model,
    SUM(v1.Qty255) AS Qty255,  
    SEC_TO_TIME(SUM(v1.yellowduration)) AS yellowduration,
    SEC_TO_TIME(SUM(v1.redduration)) AS redduration,
    SUM(v1.yellowcount) AS yellowcount,
    SUM(v1.redcount) AS redcount,
    SUM(v1.sumcount) AS sumcount,
    MAX(v1.updated) AS updated
FROM (

    SELECT 	
        SUBSTRING_INDEX(SUBSTRING_INDEX(d.device_name, '_', 4), '_',-1) AS device_name,
        d.dev_assetno, d.dev_area, d.dev_firstperson, d.dev_workshop, d.dev_line,
        vv4.Model Model, vv4.Qty255 Qty255, vv1.yellowduration, vv1.redduration, vv1.yellowcount, vv1.redcount, vv1.sumcount, vv1.updated ,san.FType
    FROM devices d LEFT JOIN (	
        SELECT 
            a.dut_id,
            SUM(CASE WHEN a.type LIKE 'yellow' THEN 1 ELSE 0 END) AS yellowcount,
            SUM(CASE WHEN a.type LIKE 'red' THEN 1 ELSE 0 END) AS redcount,
            SUM(CASE WHEN a.type LIKE 'yellow' THEN 1 ELSE 0 END) + SUM(CASE WHEN a.type LIKE 'red' THEN 1 ELSE 0 END) AS sumcount,
            MAX(CASE WHEN a.type LIKE 'yellow' THEN a.duration END) AS yellowduration,
            MAX(CASE WHEN a.type LIKE 'red' THEN a.duration END) AS redduration,
            MAX(a.start) updated
        FROM alarms a 
        WHERE 1 = 1  
        AND a.start >= ?
        AND a.start <= ?
        GROUP BY a.dut_id
    ) vv1 ON vv1.dut_id = d.dtu_sn	
     left join smt_assets_new_sz_sync san on san.FNumber = d.dev_assetno	
     left join (	
     	select mls.id,mls.lineName from mes_lineinfo_sz_sync mls 
     ) vv3 on d.dev_line = vv3.lineName
     left join (
     	SELECT t.max_id AS id,t.lineid,t.Qty255,mpss2.model AS Model,mlss.linename
		FROM (
		    SELECT mpss.lineid,SUM(mpss.qty255) AS Qty255,MAX(mpss.id) AS max_id
		    FROM mes_plan_sz_sync mpss 
		    WHERE mpss.fdate >= ?
		        AND mpss.fdate <= ?
		    GROUP BY mpss.lineid  
		) t	LEFT JOIN mes_plan_sz_sync mpss2 ON t.max_id = mpss2.id left join mes_lineinfo_sz_sync mlss on t.lineid = mlss.id
     ) vv4 on vv4.lineid = vv3.id
     where d.dev_area = 'SZ'
    union all
    SELECT 	
        SUBSTRING_INDEX(SUBSTRING_INDEX(d.device_name, '_', 4), '_',-1) AS device_name,
        d.dev_assetno, d.dev_area, d.dev_firstperson, d.dev_workshop, d.dev_line,
        vv4.Model Model, vv4.Qty255 Qty255, vv1.yellowduration, vv1.redduration, vv1.yellowcount, vv1.redcount, vv1.sumcount, vv1.updated ,san.FType
    FROM devices d LEFT JOIN (	
        SELECT 
            a.dut_id,
            SUM(CASE WHEN a.type LIKE 'yellow' THEN 1 ELSE 0 END) AS yellowcount,
            SUM(CASE WHEN a.type LIKE 'red' THEN 1 ELSE 0 END) AS redcount,
            SUM(CASE WHEN a.type LIKE 'yellow' THEN 1 ELSE 0 END) + SUM(CASE WHEN a.type LIKE 'red' THEN 1 ELSE 0 END) AS sumcount,
            MAX(CASE WHEN a.type LIKE 'yellow' THEN a.duration END) AS yellowduration,
            MAX(CASE WHEN a.type LIKE 'red' THEN a.duration END) AS redduration,
            MAX(a.start) updated
        FROM alarms a 
        WHERE 1 = 1  
        AND a.start >= ?
        AND a.start <= ?
        GROUP BY a.dut_id
    ) vv1 ON vv1.dut_id = d.dtu_sn	
     left join smt_assets_new_hn_sync san on san.FNumber = d.dev_assetno	
     left join (	
     	select mls.id,mls.lineName from mes_lineinfo_hn_sync mls 
     ) vv3 on d.dev_line = vv3.lineName
     left join (
     	SELECT t.max_id AS id,t.lineid,t.Qty255,mpss2.model AS Model,mlss.linename
		FROM (
		    SELECT mpss.lineid,SUM(mpss.qty255) AS Qty255,MAX(mpss.id) AS max_id
		    FROM mes_plan_hn_sync mpss 
		    WHERE mpss.fdate >= ?
		        AND mpss.fdate <= ?
		    GROUP BY mpss.lineid  
		) t	LEFT JOIN mes_plan_hn_sync mpss2 ON t.max_id = mpss2.id left join mes_lineinfo_hn_sync mlss on t.lineid = mlss.id
     ) vv4 on vv4.lineid = vv3.id
     where d.dev_area = 'HN'
    UNION ALL
    SELECT 
        CASE
            WHEN san.FName LIKE '全自动测试设备%' THEN san.FModel
            ELSE san.FName
        END AS device_name,
        san.FNumber dev_assetno,
        'SZ' dev_area,
        san.FUser dev_firstperson,
        CASE
            WHEN san.FStation REGEXP 'B43|三楼|3楼|3F' THEN 'B43'
            WHEN san.FStation REGEXP 'B41|一楼|1楼|smt|SMT|1F' THEN 'B41'
            ELSE '其它'
        END AS dev_workshop ,
        vv2.dev_line dev_line,
        vv4.Model Model, vv4.Qty255 Qty255, 0 yellowduration, 0 redduration, 0 yellowcount, vv2.sumcount redcount, vv2.sumcount, vv2.updated ,san.FType 
    FROM smt_assets_new_sz_sync san left join (
		SELECT 
		    REPLACE(SUBSTRING_INDEX(macs.line_no, '_', 1), 'SZ', 'ZLT-') AS line_no_new,
		    SUBSTRING(macs.line_no, LOCATE('_', macs.line_no) + 1) AS dev_line,
		    COUNT(macs.line_no) sumcount,
		    MAX( macs.alarm_time) updated
		FROM mes_alarm_content_sz_sync macs 
		where macs.alarm_time >= ?  and macs.alarm_time <= ?
		group by line_no_new,line_no
	) vv2 on vv2.line_no_new = san.FNumber
	left join (	
     	select mls.id,mls.lineName from mes_lineinfo_sz_sync mls 
     ) vv3 on vv2.dev_line = vv3.lineName
     left join (
     	SELECT t.max_id AS id,t.lineid,t.Qty255,mpss2.model AS Model,mlss.linename
		FROM (
		    SELECT mpss.lineid,SUM(mpss.qty255) AS Qty255,MAX(mpss.id) AS max_id
		    FROM mes_plan_sz_sync mpss 
		    WHERE mpss.fdate >= ?
		    AND mpss.fdate <= ?
		    GROUP BY mpss.lineid  
		) t	LEFT JOIN mes_plan_sz_sync mpss2 ON t.max_id = mpss2.id left join mes_lineinfo_sz_sync mlss on t.lineid = mlss.id
     ) vv4 on vv4.lineid = vv3.id
	where san.FType in ('镭雕机', '平行移载', '印刷机', '分板机', '全自动测试设备', 'AOI', 'SPI') 
	and san.FAStatus = 1	
	union all 
	SELECT 
	    CASE
	        WHEN san.FName LIKE '全自动测试设备%' THEN san.FModel
	        ELSE san.FName
	    END AS device_name,
	    san.FNumber dev_assetno,
	    'HN' dev_area,
	    san.FUser dev_firstperson,
	    'HN' dev_workshop ,
	    vv2.dev_line dev_line,
	    vv4.Model Model, vv4.Qty255 Qty255, 0 yellowduration, 0 redduration, 0 yellowcount, vv2.sumcount redcount, vv2.sumcount, vv2.updated ,san.FType 
	FROM smt_assets_new_hn_sync san left join (
	    SELECT 
			REPLACE(SUBSTRING_INDEX(macs.line_no, '_', 1), 'HNZ', 'HNZ-') AS line_no_new,
			SUBSTRING(macs.line_no, LOCATE('_', macs.line_no) + 1) AS dev_line,
			COUNT(macs.line_no) sumcount,
			MAX( macs.alarm_time) updated
		FROM mes_alarm_content_hn_sync macs 
		where macs.alarm_time >= ?  and macs.alarm_time <= ?
		group by line_no_new,line_no
	) vv2 on vv2.line_no_new = san.FNumber
	left join (	
     	select mls.id,mls.lineName from mes_lineinfo_hn_sync mls 
     ) vv3 on vv2.dev_line = vv3.lineName
     left join (
     	SELECT t.max_id AS id,t.lineid,t.Qty255,mpss2.model AS Model,mlss.linename
		FROM (
		    SELECT mpss.lineid,SUM(mpss.qty255) AS Qty255,MAX(mpss.id) AS max_id
		    FROM mes_plan_hn_sync mpss 
		    WHERE mpss.fdate >= ?
		    AND mpss.fdate <= ?
		    GROUP BY mpss.lineid  
		) t	LEFT JOIN mes_plan_hn_sync mpss2 ON t.max_id = mpss2.id left join mes_lineinfo_hn_sync mlss on t.lineid = mlss.id
     ) vv4 on vv4.lineid = vv3.id
	where san.FType in ('镭雕机', '平行移载', '印刷机', '分板机', '全自动测试设备', 'AOI', 'SPI') 
	and san.FAStatus = 1	
) v1
```

### 报警首页数据需要加载从当前时间开始往前推近24小时数据，带时分秒显示

## 2024-12-18 会话记录 报警明细显示

### 黄灯报警明细显示

### 接口地址
`http://localhost:3003/api/yellow-alarm-details`

### SQL脚本
```sql
SELECT a.dut_id dut_id,
                   d.device_name device_name,	
                   d.dev_assetno dev_assetno,
                   d.dev_firstperson dev_firstperson,
                   d.dev_workshop dev_workshop,
                   d.dev_area dev_area,
                   d.dev_line dev_line,
                   a.\`start\` as startTime,
                   a.\`end\` as endTime,
                   a.duration duration,
                   'yellow' alarm_item ,
                   '黄灯报警' alarm_content,
                   a.start updated
                   FROM alarms a left join devices d on a.dut_id = d.dtu_sn 
                   WHERE 1=1
                   AND a.start >= ? 
                   AND a.start <= ?
                   AND d.dev_assetno = ? 
                   AND a.\`type\` = ?
                   ORDER BY a.start DESC
```


### 红灯报警明细显示

### 接口地址
`http://localhost:3003/api/red-alarm-details`

### SQL脚本
```sql
SELECT a.dut_id dut_id,
            d.device_name device_name,	
            d.dev_assetno dev_assetno,
            d.dev_firstperson dev_firstperson,
            d.dev_workshop dev_workshop,
            d.dev_area dev_area,
            d.dev_line dev_line,
            a.\`start\` as startTime,
            a.\`end\` as endTime,
            a.duration duration,
            'red' alarm_item ,
            '红灯报警' alarm_content,
            a.start updated
        FROM alarms a left join devices d on a.dut_id = d.dtu_sn 
        WHERE 1=1
        AND a.start >= ?
        AND a.start <= ?
        AND d.dev_assetno = ?
        AND a.\`type\` = 'red'

        union all	
        SELECT 
            '-' dut_id ,
            macs.device_name device_name,
            REPLACE(SUBSTRING_INDEX(macs.line_no, '_', 1), 'SZ', 'ZLT-') AS dev_assetno,
            san.FUser dev_firstperson ,
            CASE
                WHEN san.FStation REGEXP 'B43|三楼|3楼|3F' THEN 'B43'
                WHEN san.FStation REGEXP 'B41|一楼|1楼|smt|SMT|1F' THEN 'B41'
                ELSE '其它'
            END AS dev_workshop ,
            'SZ' dev_area ,
            SUBSTRING_INDEX(SUBSTRING_INDEX(macs.line_no, '_', 2), '_', -1) AS dev_line ,
            '-' startTime ,
            '-' endTime ,
            '-' duration ,
            macs.alarm_item alarm_item ,
            macs.alarm_content alarm_content,
            macs.alarm_time updated
        FROM mes_alarm_content_sz_sync macs left join smt_assets_news san on REPLACE(SUBSTRING_INDEX(macs.line_no, '_', 1), 'SZ', 'ZLT-') = san.FNumber
        where macs.alarm_time >= ?
        and macs.alarm_time <= ?
        AND REPLACE(SUBSTRING_INDEX(macs.line_no, '_', 1), 'SZ', 'ZLT-') = ?

        union all	
        SELECT 
            '-' dut_id ,
            macs.device_name device_name,
            REPLACE(SUBSTRING_INDEX(macs.line_no, '_', 1), 'HNZ', 'HNZ-') AS dev_assetno,
            san.FUser dev_firstperson ,
            'HN' dev_workshop ,
            'HN' dev_area ,
            SUBSTRING_INDEX(SUBSTRING_INDEX(macs.line_no, '_', 2), '_', -1) AS dev_line ,
            '-' startTime ,
            '-' endTime ,
            '-' duration ,
            macs.alarm_item alarm_item ,
            macs.alarm_content alarm_content,
            macs.alarm_time updated
        FROM mes_alarm_content_hn_sync macs left join smt_assets_news san on REPLACE(SUBSTRING_INDEX(macs.line_no, '_', 1), 'HNZ', 'HNZ-') = san.FNumber
        where macs.alarm_time >= ?
        and macs.alarm_time <= ?
        AND REPLACE(SUBSTRING_INDEX(macs.line_no, '_', 1), 'HNZ', 'HNZ-') = ?
        ORDER BY updated DESC
```

### 报警总数明细显示

### 接口地址
`http://localhost:3003/api/total-alarm-details`

### SQL脚本
```sql
SELECT a.dut_id dut_id,
            d.device_name device_name,	
            d.dev_assetno dev_assetno,
            d.dev_firstperson dev_firstperson,
            d.dev_workshop dev_workshop,
            d.dev_area dev_area,
            d.dev_line dev_line,
            a.\`start\` as startTime,
            a.\`end\` as endTime,
            a.duration duration,
            CASE
                WHEN a.\`type\` = 'red' THEN 'red'
                WHEN a.\`type\` = 'yellow' THEN 'yellow'
            END AS alarm_item ,
            CASE
                WHEN a.\`type\` = 'red' THEN '红灯报警'
                WHEN a.\`type\` = 'yellow' THEN '黄灯报警'
            END AS alarm_content ,
            a.start updated
        FROM alarms a left join devices d on a.dut_id = d.dtu_sn 
        WHERE 1=1
        AND a.start >= ?
        AND a.start <= ?
        AND d.dev_assetno = ?

        union all	
        SELECT 
            '-' dut_id ,
            macs.device_name device_name,
            REPLACE(SUBSTRING_INDEX(macs.line_no, '_', 1), 'SZ', 'ZLT-') AS dev_assetno,
            san.FUser dev_firstperson ,
            CASE
                WHEN san.FStation REGEXP 'B43|三楼|3楼|3F' THEN 'B43'
                WHEN san.FStation REGEXP 'B41|一楼|1楼|smt|SMT|1F' THEN 'B41'
                ELSE '其它'
            END AS dev_workshop ,
            'SZ' dev_area ,
            SUBSTRING_INDEX(SUBSTRING_INDEX(macs.line_no, '_', 2), '_', -1) AS dev_line ,
            '-' startTime ,
            '-' endTime ,
            '-' duration ,
            macs.alarm_item alarm_item ,
            macs.alarm_content alarm_content,
            macs.alarm_time updated
        FROM mes_alarm_content_sz_sync macs left join smt_assets_news san on REPLACE(SUBSTRING_INDEX(macs.line_no, '_', 1), 'SZ', 'ZLT-') = san.FNumber
        where macs.alarm_time >= ?
        and macs.alarm_time <= ?
        AND REPLACE(SUBSTRING_INDEX(macs.line_no, '_', 1), 'SZ', 'ZLT-') = ?

        union all	
        SELECT 
            '-' dut_id ,
            macs.device_name device_name,
            REPLACE(SUBSTRING_INDEX(macs.line_no, '_', 1), 'HNZ', 'HNZ-') AS dev_assetno,
            san.FUser dev_firstperson ,
            'HN' dev_workshop ,
            'HN' dev_area ,
            SUBSTRING_INDEX(SUBSTRING_INDEX(macs.line_no, '_', 2), '_', -1) AS dev_line ,
            '-' startTime ,
            '-' endTime ,
            '-' duration ,
            macs.alarm_item alarm_item ,
            macs.alarm_content alarm_content,
            macs.alarm_time updated
        FROM mes_alarm_content_hn_sync macs left join smt_assets_news san on REPLACE(SUBSTRING_INDEX(macs.line_no, '_', 1), 'HNZ', 'HNZ-') = san.FNumber
        where macs.alarm_time >= ?
        and macs.alarm_time <= ?
        AND REPLACE(SUBSTRING_INDEX(macs.line_no, '_', 1), 'HNZ', 'HNZ-') = ?
        ORDER BY updated DESC
```

## 2024-12-18 会话记录 问题条推送

---
### 需求描述 当天报警总数>设定的阈值时，会自动生成一条问题条，当天只生成一条

### 问题条规则显示

### 接口地址
`http://localhost:3003/api/alarm-rules`

### SQL脚本
```sql
SELECT 
                DATE_FORMAT(create_time, '%Y-%m-%d %H:%i:%s') as create_time,
                rule_code,
                rule_content
            FROM alarm_rule 
            WHERE alarm_level = ?
            ORDER BY create_time DESC
```

### 问题条推送

### 接口地址
`http://localhost:3003/api/push-alarm-info`

### SQL脚本
```sql
INSERT IGNORE INTO alarm_info (
                                    pc_number, mac_address, location, responsible_person, 
                                    alarm_message, alarm_level, alarm_type, hour_interval, 
                                    status, push_status, model
                                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
```

### 问题条明细显示

### 接口地址
`http://localhost:3003/api/api/problem-details`

### SQL脚本
```sql
SELECT 
                id,
                pc_number as assetNo,
                mac_address,
                location,
                responsible_person,
                alarm_message as problemContent,
                alarm_level,
                alarm_type,
                hour_interval,
                status as implementation,
                created_at as createdTime,
                updated_at as updatedTime,
                resolved_at,
                improvement_direction,
                improver,
                improvement_time,
                confirmer,
                push_status,
                model
            FROM alarm_info 
            WHERE alarm_level = '设备报警监测系统' and status = 'NG'
```

### TOP3 问题显示

### 接口地址
`http://localhost:3003/api/top3-problems`

### SQL脚本
```sql
SELECT v1.alarm_content, COUNT(v1.alarm_content) alarm_content_count
            FROM (
                SELECT a.dut_id dut_id,
                    d.device_name device_name,	
                    d.dev_assetno dev_assetno,
                    d.dev_firstperson dev_firstperson,
                    d.dev_workshop dev_workshop,
                    d.dev_area dev_area,
                    d.dev_line dev_line,
                    a.\`start\` as startTime,
                    a.\`end\` as endTime,
                    a.duration duration,
                    CASE
                        WHEN a.\`type\` = 'red' THEN 'red'
                        WHEN a.\`type\` = 'yellow' THEN 'yellow'
                    END AS alarm_item,
                    CASE
                        WHEN a.\`type\` = 'red' THEN '红灯报警'
                        WHEN a.\`type\` = 'yellow' THEN '黄灯报警'
                    END AS alarm_content,
                    a.start updated
                FROM alarms a LEFT JOIN devices d ON a.dut_id = d.dtu_sn 
                WHERE 1=1
                AND a.start >= ?
                AND a.start <= ?
                AND d.dev_assetno = ?

                UNION ALL
                
                -- 深圳鸿义通设备报警明细
                SELECT 
                    '-' dut_id,
                    macs.device_name device_name,
                    REPLACE(SUBSTRING_INDEX(macs.line_no, '_', 1), 'SZ', 'ZLT-') AS dev_assetno,
                    san.FUser dev_firstperson,
                    CASE
                        WHEN san.FStation REGEXP 'B43|三楼|3楼|3F' THEN 'B43'
                        WHEN san.FStation REGEXP 'B41|一楼|1楼|smt|SMT|1F' THEN 'B41'
                        ELSE '其它'
                    END AS dev_workshop,
                    'SZ' dev_area,
                    SUBSTRING_INDEX(SUBSTRING_INDEX(macs.line_no, '_', 2), '_', -1) AS dev_line,
                    '-' startTime,
                    '-' endTime,
                    '-' duration,
                    macs.alarm_item alarm_item,
                    macs.alarm_content alarm_content,
                    macs.alarm_time updated
                FROM mes_alarm_content_sz_sync macs 
                LEFT JOIN smt_assets_news san ON REPLACE(SUBSTRING_INDEX(macs.line_no, '_', 1), 'SZ', 'ZLT-') = san.FNumber
                WHERE macs.alarm_time >= ?
                AND macs.alarm_time <= ?
                AND REPLACE(SUBSTRING_INDEX(macs.line_no, '_', 1), 'SZ', 'ZLT-') = ?

                UNION ALL
                
                -- 湖南鸿义通设备报警明细
                SELECT 
                    '-' dut_id,
                    macs.device_name device_name,
                    REPLACE(SUBSTRING_INDEX(macs.line_no, '_', 1), 'HNZ', 'HNZ-') AS dev_assetno,
                    san.FUser dev_firstperson,
                    'HN' dev_workshop,
                    'HN' dev_area,
                    SUBSTRING_INDEX(SUBSTRING_INDEX(macs.line_no, '_', 2), '_', -1) AS dev_line,
                    '-' startTime,
                    '-' endTime,
                    '-' duration,
                    macs.alarm_item alarm_item,
                    macs.alarm_content alarm_content,
                    macs.alarm_time updated
                FROM mes_alarm_content_hn_sync macs 
                LEFT JOIN smt_assets_news san ON REPLACE(SUBSTRING_INDEX(macs.line_no, '_', 1), 'HNZ', 'HNZ-') = san.FNumber
                WHERE macs.alarm_time >= ?
                AND macs.alarm_time <= ?
                AND REPLACE(SUBSTRING_INDEX(macs.line_no, '_', 1), 'HNZ', 'HNZ-') = ?
                ORDER BY updated DESC
            ) v1 
            GROUP BY v1.alarm_content 
            ORDER BY COUNT(v1.alarm_content) DESC 
            LIMIT 3
```

## 2024-12-18 会话记录

---

## [2024-12-18 15:30] - 报警信息界面优化与分页功能实现

### 需求描述
1. 调小报警信息表格的行间距
2. 固定表格标题头，滚动时保持可见
3. 为报警信息增加分页功能（不影响现有功能）
4. 调整分页控件布局（居中显示，增加上间距）
5. 调整两排筛选条件对齐
6. 规则按钮显示问题条总数量徽章
7. 徽章根据地域筛选（SZ显示ZLT开头，HN显示HNZ开头）
8. 报警抽屉也要根据地域筛选显示
9. 修复综合报警记录中只有秒数的持续时间显示问题

### 实现方案

#### 1. 表格行间距优化
- 减小表头和数据行的 padding
- 报警信息表格：表头 `6px 8px`，数据行 `5px 8px`
- 报警规则表格：表头和数据行均为 `6px 8px`

#### 2. 固定表头实现
- 为 `.alarm-info-table thead th` 添加 `position: sticky; top: 0; z-index: 10;`
- 为 `.alarm-table-wrapper` 添加 `position: relative;`

#### 3. 分页功能完整实现
**新增变量：**
```javascript
let alarmInfoData = [];           // 完整数据
let alarmInfoCurrentPage = 1;     // 当前页码
let alarmInfoPageSize = 10;       // 每页10条
```

**核心函数：**
- `renderAlarmInfoPage()` - 渲染当前页数据
- `updateAlarmInfoPagination()` - 更新分页控件
- `generatePageNumbers()` - 智能生成页码（最多显示5个）
- `goToAlarmInfoPage(page)` - 跳转指定页
- `initAlarmInfoPagination()` - 初始化事件监听

**HTML结构：**
```html
<div class="alarm-pagination">
    <div class="pagination-info">
        <span>共 <span id="alarmTotalCount">0</span> 条</span>
    </div>
    <div class="pagination-controls">
        <button class="pagination-btn" id="alarmFirstPage">首页</button>
        <button class="pagination-btn" id="alarmPrevPage">上一页</button>
        <div class="pagination-pages" id="alarmPageNumbers"></div>
        <button class="pagination-btn" id="alarmNextPage">下一页</button>
        <button class="pagination-btn" id="alarmLastPage">尾页</button>
    </div>
</div>
```

#### 4. 分页控件布局调整
```css
.alarm-pagination {
    display: flex;
    justify-content: center;  /* 居中 */
    align-items: center;
    padding: 12px 20px;
    margin-top: 15px;         /* 上间距 */
    gap: 40px;                /* 信息与按钮间距 */
}
```

#### 5. 筛选条件对齐优化
- 为 `.form-row` 统一添加 `padding-left: 30px`
- 移除各行独立的 `margin-left` 设置
- 确保两排左侧完美对齐

#### 6. 规则按钮徽章功能
**CSS样式：**
```css
.alert-btn {
    position: relative;
    width: auto;
    min-width: 69.3px;
    padding-right: 40px;
}

.alert-btn-badge {
    position: absolute;
    top: -8px;
    right: -8px;
    background: #ff4d4f;
    color: white;
    border-radius: 10px;
    padding: 2px 6px;
    font-size: 11px;
    font-weight: 700;
    border: 2px solid white;
    box-shadow: 0 2px 4px rgba(255, 77, 79, 0.4);
}
```

**HTML：**
```html
<button class="alert-btn">
    规则
    <span class="alert-btn-badge" id="mainAlarmBadge">0</span>
</button>
```

#### 7. 按地域筛选徽章统计
```javascript
// 在 renderTable() 中根据地域筛选统计
const totalProblemItems = currentData.reduce((sum, item) => {
    const assetNo = item.assetNo || '';
    const problemItems = item.problemItems || 0;
    
    if (currentRegion === 'SZ') {
        // 只统计ZLT开头的资产
        if (assetNo.startsWith('ZLT')) {
            return sum + problemItems;
        }
    } else if (currentRegion === 'HN') {
        // 只统计HNZ开头的资产
        if (assetNo.startsWith('HNZ')) {
            return sum + problemItems;
        }
    } else {
        // 全部地域
        return sum + problemItems;
    }
    return sum;
}, 0);

updateMainAlarmBadge(totalProblemItems);
```

#### 8. 报警抽屉地域筛选
```javascript
function renderAlarmInfo(alarmData) {
    // 根据地域筛选数据
    let filteredData = alarmData;
    
    if (currentRegion === 'SZ') {
        filteredData = alarmData.filter(item => {
            const assetNo = item.assetNo || '';
            return assetNo.startsWith('ZLT');
        });
    } else if (currentRegion === 'HN') {
        filteredData = alarmData.filter(item => {
            const assetNo = item.assetNo || '';
            return assetNo.startsWith('HNZ');
        });
    }
    
    alarmInfoData = filteredData;
    // ... 后续渲染逻辑
}
```

#### 9. 修复持续时间转换问题
**问题：** `formatAlarmDuration()` 无法处理 "XX秒" 格式

**解决方案：**
```javascript
function formatAlarmDuration(duration) {
    // ... 其他格式处理
    
    // 新增：处理 XX秒 格式（只有秒）
    if (durationStr.includes('秒') && !durationStr.includes('分')) {
        const match = durationStr.match(/(\d+)秒/);
        if (match) {
            const totalSeconds = parseInt(match[1]);
            return secondsToDuration(totalSeconds);
        }
    }
    
    // ... 其他逻辑
}

function durationToSeconds(durationStr) {
    // ... 其他格式处理
    
    // 新增：处理 XX秒 格式
    const secondMatch = duration.match(/(\d+)秒/);
    if (secondMatch) {
        return parseInt(secondMatch[1]);
    }
    
    // ... 其他逻辑
}
```

### 修改文件
- `index.html`: 
  - 添加分页控件HTML结构
  - 调整表格行间距CSS
  - 添加固定表头样式
  - 添加分页样式
  - 调整筛选条件布局
  - 添加徽章样式和HTML

- `app.js`:
  - 新增分页相关变量和函数
  - 修改 `renderTable()` 添加徽章统计逻辑
  - 修改 `renderAlarmInfo()` 添加地域筛选
  - 修改 `openAlarmDrawer()` 重置分页状态
  - 修复 `formatAlarmDuration()` 和 `durationToSeconds()` 函数
  - 在 `DOMContentLoaded` 中初始化分页事件

### 关键特性

#### 分页功能特点
- ✅ 每页显示10条数据
- ✅ 显示总条数
- ✅ 首页/上一页/下一页/尾页按钮
- ✅ 智能页码显示（页数多时显示省略号）
- ✅ 当前页高亮
- ✅ 按钮禁用状态处理
- ✅ 序号连续显示（跨页递增）
- ✅ 不影响现有功能

#### 地域筛选逻辑
- **SZ地域**: 只显示/统计 ZLT 开头的资产
- **HN地域**: 只显示/统计 HNZ 开头的资产  
- **全部地域**: 显示/统计所有资产

#### 时间格式支持
- ✅ `00:00:00` (HH:MM:SS)
- ✅ `5分30秒` → `00:05:30`
- ✅ `30秒` → `00:00:30` (新增)
- ✅ `45` (纯数字) → `00:00:45`

### 效果说明
1. 表格更紧凑，同等空间显示更多内容
2. 滚动时表头固定，方便对照列名
3. 分页控件美观居中，操作便捷
4. 徽章实时显示对应地域问题总数，醒目直观
5. 抽屉数据与主界面地域选择联动
6. 所有持续时间格式正确显示

---

## [2024-12-18 16:00] - 结束时间默认值优化

### 需求描述
将原先固定的结束时间 `23:59:59` 修改为当前时间的时分秒，使查询时间范围更准确。

### 实现方案

#### 修改初始化时间设置
**修改前：**
```javascript
// 设置结束时间为当天的23:59:59
const endDate = new Date(today);
endDate.setHours(23, 59, 59, 999); // 固定为23:59:59
```

**修改后：**
```javascript
// 设置结束时间为当前时间（不再固定为23:59:59）
const endDate = new Date(today);
// 直接使用当前时间的时分秒
```

#### 修改清除按钮重置逻辑
**修改前：**
```javascript
if (endTimeInput) {
    // 设置结束时间为当天的23:59:59
    const resetEndDate = new Date(endDate);
    resetEndDate.setHours(23, 59, 59, 999);
    endTimeInput.value = formatDateTimeForInput(resetEndDate);
}
```

**修改后：**
```javascript
if (endTimeInput) {
    // 设置结束时间为当前时间（不再固定为23:59:59）
    endTimeInput.value = formatDateTimeForInput(endDate);
}
```

### 修改文件
- `app.js`:
  - 修改 `initializeDateTimeInputs()` 函数，移除固定23:59:59的逻辑
  - 修改 `clearFilters()` 函数中的时间重置逻辑

### 效果说明
- ✅ 页面加载时：结束时间 = 当前实际时间（如 15:30:45）
- ✅ 点击清除按钮：结束时间重置为当前实际时间
- ✅ 开始时间仍为往前推24小时
- ✅ 查询时间范围更精确，避免遗漏当天未到23:59:59的数据

**示例：**
- 如果现在是 `2024-12-18 15:30:45`
- 默认查询范围：`2024-12-17 15:30:45` 至 `2024-12-18 15:30:45`
- 之前是：`2024-12-17 15:30:45` 至 `2024-12-18 23:59:59`（会包含未来时间）

---



