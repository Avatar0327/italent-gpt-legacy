# R2 原站行为对照

原站本轮实测单列；P1/P2设计断言不冒充原站事实，旧实现静态证据不冒充R2 P3。

|编号|模块|操作与原站结果|P1|P2|旧实现/四方对照|分类|
|---|---|---|---|---|---|---|
|R2-OBS-M37-001|M37|创建名称STD01、分类/模型空，保存后空四维标准可回读，初始停用。启用→确认后状态启用，无独立审核操作。|M37-SPEC-02/03；目录与用途就绪分层；独立审批为已批准选择|M37_Design.md target/purposeReadiness及独立审批|main 22be3a7 development.ts standard anchors.length(5)，create默认active（仅静态，不是R2 P3）|INTENTIONAL_DIFFERENCE|
|R2-OBS-M37-002|M37|指标库新增表单三类型能力/潜力/经历；说明上限500。LIB01保存后进入空指标列表。|M37-SPEC-01 三库四子集|M37_Design.md indicator_library|旧standard模型无独立library；P2已计划补齐，非新实施缺陷|MATCH|
|R2-OBS-M37-003|M37|含RUN_ID连字符编码保存被拦截：首字符必须是字母，且只能包含字母数字下划线；本次拒绝无创建。|M37-SPEC-01 1–200字/trim/库内区分大小写唯一，未规定此字符集|M37_Design.md及Contract_Repair编码规则未要求此正则|旧development.ts code=text 1–200，无该字符集（静态）|NEED_OWNER_DECISION|
|R2-OBS-M37-004|M37|单等级、行为关键点+描述、行动建议类型+描述、面试关键点+问题均各保存1行并回读；等级不强制五级。|M37-SPEC-01/03；AC02/08|IndicatorChild包含subsetName/description；逐等级alias/elementText已覆盖；非等级关键点/建议类型的映射尚未明确|旧anchors固定5且无上述四类对象，P2已识别旧模型改造|DESIGN_GAP|
|R2-OBS-M37-005|M37|权重-1/101/0均出现请输入0-100之间的数字；回填合法1、失焦、键盘输入且目标1后仍同提示。提示与合法输入矛盾，未确认服务端权重边界，未产生引用。|M37-SPEC-02显式0排除聚合、有限非负，不规定100上限|M37_Design.md标准行weight≥0；零分母不得计算|旧模型没有权重字段；未运行产品|ENV_BLOCKED|
