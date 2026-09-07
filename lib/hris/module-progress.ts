export type ModuleProgress={done:string;remaining:string;links:{label:string;href:string}[]};
const link=(label:string,href:string)=>({label,href});
export const moduleProgress:Record<string,ModuleProgress>={
 '组织员工':{done:'组织人员、岗位职级、入转调离、编制、合同、自定义字段',remaining:'字段分组与条件必填、兼岗、复杂再入职及法人变更',links:[link('组织员工','/employees'),link('编制合同','/workforce'),link('档案字段','/employee-fields')]},
 '审批中心':{done:'人事顺序审批、独立复核、撤回及历史',remaining:'管理员委托、复杂条件分支及其他模块待办汇集',links:[link('人事审批','/approvals'),link('跨模块待办','/work-inbox')]},
 '干部管理2.0':{done:'提名审议、已批准调动的任用核对、考察述职',remaining:'完整干部档案、评委会和原站详细规则核实',links:[link('干部提名与考察','/cadres')]},
 '任职资格':{done:'标准版本、能力证据、独立认证、到期与撤销',remaining:'任职类别层级及复杂认证委员会',links:[link('任职资格','/qualifications')]},
 '薪酬社保':{done:'核定工资录入、独立复核、工资条、异议及补差',remaining:'自动核算、税社保、薪资档案、支付及企业规则验证',links:[link('工资批次','/payroll'),link('工资异议与补差','/payroll-adjustments')]},
 '假勤管理':{done:'固定班次、打卡、补卡、请假、人工余额及覆盖报表',remaining:'弹性轮班、设备、加班、跨班请假、自动结转与封账',links:[link('假勤管理','/attendance')]},
 '招聘管理系统':{done:'需求审批、候选人、面试评价、录用确认和原子入职',remaining:'渠道门户、简历解析、面试日历、电子签和AI能力',links:[link('招聘与入职','/recruitment')]},
 '绩效管理':{done:'目标权重、自评、独立评价、结果发布、申诉与更正',remaining:'完整OKR、组织绩效、多级校准审批和企业申诉时限',links:[link('绩效管理','/performance')]},
 '继任与发展':{done:'盘点、人才池、后备提名、发展计划与学习衔接',remaining:'复杂梯队、健康度模型和带教管理',links:[link('人才与发展','/development')]},
 '在线盘点':{done:'标准、盘点项目、九宫格快照、人才池及继任记录',remaining:'盘点校准会、报告模板和多维模型',links:[link('人才与发展','/development')]},
 '360度评估':{done:'指定评估人、量表答卷、分组阈值与冻结报告',remaining:'多种题型、提醒催办与完整活动运营',links:[link('360度评估','/feedback')]},
 '学习管理':{done:'课程考试、培训项目、排期出勤、学分及讲师认证',remaining:'完整师资档案、外聘讲师、班级运营、学分到期折抵',links:[link('学习中心','/learning'),link('培训场次','/training-sessions'),link('学分','/learning-credits'),link('讲师认证','/instructors')]},
 '员工调查':{done:'实名问卷模板、发布名单、答卷及统计',remaining:'匿名模式、完整调查报告与行动计划',links:[link('实名问卷','/surveys')]},
 '问卷调查':{done:'实名量表和单选、模板版本、填报撤回与结项',remaining:'复杂题型、分类、条件跳转及匿名模式',links:[link('实名问卷','/surveys')]},
 '报表':{done:'当前权限范围报表、分页查询和审计导出',remaining:'自助设计器、完整领域覆盖、大规模查询与历史快照',links:[link('人事报表','/reports')]},
 '人才标准':{done:'能力标准版本、行为锚点及岗位要求',remaining:'复杂指标组合、多维模型和标准审批机制',links:[link('能力标准','/development')]},
 '员工自助':{done:'本人档案、融入计划、假勤、学习、问卷、工资和申请进度',remaining:'日程、日报、完整OKR与统一消息',links:[link('员工自助','/self-service'),link('融入计划','/onboarding')]},
};
