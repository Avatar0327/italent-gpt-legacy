# 浏览器并发检查

RUN_ID：R1-ORIGIN-20260910-100019

浏览器CDP 1；启动已有tab1=about:blank，未触碰。自建tab2主操作、tab3查询检查。仅本窗口两个标签页，并非两个独立真人或独立认证会话。

环境：srworkshopbj.italent.cn，已登录管理员会话（脱敏身份标记ORIGIN-ADMIN-01，未新增账号）；原站同仓库既有入口，Controller_Resume.md记录测试租户授权。本轮未见生产提示；未修改既有组织/员工，混有旧记录时仅筛本轮前缀。

1. tab2名称查询ZZ_R1_R1-ORIGIN-20260910-100019_，空集；tab3独立名称查询同前缀M01_QUERY_B，tab2原筛选保留。
2. tab2开启未提交组织草稿，tab3无该草稿；tab3切职位页后tab2未改变页面或筛选。取消草稿也未改变tab3查询。
3. 未发现登录互踢、误标签页或同名记录污染。但草稿名称输入经fill和可见DOM输入均未能回读确认，getAttribute超时，跨域iframe只读不可取得contentDocument，截图两次Page.captureScreenshot timeout；无保存/确定提交。
4. 结论：标签页/查询隔离已有局部证据；表单内容隔离未证，不把失败归咎并发，也不宣布项目只能单浏览器。只暂停本窗口M01弹层提交和依赖写入；其他模块只读继续。

证据：R1-ORIGIN-20260910-100019/M01/M01-query.json及M01-query.jpg。无截取原站认证值/他人资料到正式证据；页面查询参数含会话标识，证据只存origin与页面名称。
