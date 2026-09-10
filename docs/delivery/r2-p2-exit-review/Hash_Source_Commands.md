# 哈希、来源与核验命令记录

被审最终HEAD：`8b3daf9270181ffe2e77015be723da8e611d83a5`；固定设计内容HEAD：`7ff3a28c7660dac658d5243d7c4535a9c8037fc2`。最终HEAD是固定HEAD的直接子提交。
启动main：`22be3a7e366d6787180d4f593a30f5984c70e03a`；R1共享设计：`e15237281ff19f04f08a354fd9455c518b24ae47`。
设计从main到最终HEAD共59个变更文件，全部位于docs/delivery/r2-p2。固定到最终仅9个包装/检查证据文件变化，核心设计正文不变。

## 固定引用11项

|路径|验证Git对象|SHA256|
|---|---|---|
|docs/delivery/r2-p2/Exit_Review.md|7ff3a28c7660dac658d5243d7c4535a9c8037fc2|545e646f166e5a4707ccb6dcca2f6893093c23cb107ddfc7b5849d955cbaf847|
|docs/delivery/r2-p2/Architecture.md|7ff3a28c7660dac658d5243d7c4535a9c8037fc2|9024938e6ec13f68a7055da673e56095ca6adf27f63e73aaaa794d70b50e34bd|
|docs/delivery/r2-p2/Cross_Module_Contracts.md|7ff3a28c7660dac658d5243d7c4535a9c8037fc2|fb0ddb062db795e023b460545863fe36b389e1e660bf752467630cad5540565e|
|docs/delivery/r2-p2/Requirements_Trace.json|7ff3a28c7660dac658d5243d7c4535a9c8037fc2|859fc8e1d9884c63973abc071627b6ce7b402a53f2a867461de5d1ec5759e7bc|
|docs/delivery/r2-p2/Limit_Resolution.json|7ff3a28c7660dac658d5243d7c4535a9c8037fc2|940d83dfa66eca97d1054e0524e6bb769cace346d8f809f53ae4bc662a56d4e9|
|docs/delivery/r2-p2/Acceptance_Scenarios.json|7ff3a28c7660dac658d5243d7c4535a9c8037fc2|a55b147c631fb87aa3c6db0e10c17d2b94a2be8ff86091ee7775a3bfae4d9d99|
|docs/delivery/r2-p2/P3_Work_Packages.json|7ff3a28c7660dac658d5243d7c4535a9c8037fc2|194b475503820bc471e8a59dbf105015c41fd6f18009f87b81a64d6283d6b513|
|docs/delivery/r2-p2/Source_Manifest.json|7ff3a28c7660dac658d5243d7c4535a9c8037fc2|98d9d5c7369c04b64722859ede12146a6a8c63dc1870f46941f7b5258fb470f6|
|docs/delivery/r2-p2/Artifact_Manifest.json|7ff3a28c7660dac658d5243d7c4535a9c8037fc2|a935f358c0c10af430d32db719ec84b1d978398ccc02b845c20e8a6d53cd45d0|
|docs/delivery/r2-p2/Review_Round1.md|7ff3a28c7660dac658d5243d7c4535a9c8037fc2|a15f6d41604aa68695906d8a8ac3b51676b307a2073d96a6532c7b4fcfa7e3e7|
|docs/delivery/r2-p2/Review_Round2.md|7ff3a28c7660dac658d5243d7c4535a9c8037fc2|316c31928556257878e6f99e02ca1755e0c8a950bc32558b5e4318313d11dc16|

固定Artifact_Manifest在固定HEAD逐项核；最终包装Artifact_Manifest在最终HEAD逐项核。没有把最终动态清单字节与固定清单哈希混比。
两个清单均排除自身和evidence，未发现循环哈希；Source_Manifest的78个来源引用全部存在，SHA256/字节数一致；7项批准记录与Scope原记录一致，含6模块批准及进入P2批准。
33项批准原文逐项与Scope及批准记录比对；12项（每模块首末SPEC）反查原评审包原文和批准时所读包SHA。
638项独立文档检查无失败；5个生成器在临时副本重建无字节漂移。未发现手改派生数量、重复ID、失效锚点或状态提升。

## 已执行的核验类别

|命令/方式|结果与范围|
|---|---|
|git worktree list --porcelain；git status --porcelain=v1；git branch -vv；git rev-parse HEAD|先查真实工作树、归属、分支、HEAD及跟踪；原设计干净，R1在制修改保留|
|git worktree add -b review/r2-p2-exit-20260910 <独立路径> 8b3daf9270181ffe2e77015be723da8e611d83a5|创建本窗口独立工作树；原分支不修改|
|git merge-base --is-ancestor；git rev-parse <final>^；git diff --name-only <base> <final>|父子关系及文档范围核对|
|git show <精确SHA>:<文件>；hashlib.sha256(bytes)|186个Git对象阅读/解析与来源清单验证；详见Read_Hash_Manifest.json|
|python docs/delivery/r2-p2-exit-review/verify_review.py|638项只读文档核验；非产品测试|
|临时目录副本顺序运行build_inventory/build_resolution/build_scenarios/build_schemas/build_handoff.py|5个生成器均成功；输出与最终包无字节漂移；只读Git对象|
|JSON duplicate-key拒绝解析、ID去重、引用及GWT比对|33/295/149/24/78/16/17/5/46/138和52责任子项均独立核算|
|python docs/delivery/r2-p2-exit-review/record_audit.py|闭合schema属性比对、符号分组表、来源反查和独立结论记录|
|git ls-remote <已授权仓库> <design-ref> <review-ref>|首次无凭据读失败；普通Sites仓库凭据读成功，设计远端精确等于最终HEAD，评审远端初始不存在；后续推送见提交记录|

未直接运行check_design.py：该脚本会重写被评审清单/证据，且检查设计分支名。独立脚本核其必要不变量并复建纯文档生成源，避免改动被审材料。
JSON Schema做了全部本地引用、required、封闭对象、正则及76个条件动作绑定核对；环境无jsonschema库，未声称通过第三方完整元schema验证。明确的属性缺失反例不依赖该库。
未运行npm、产品单元/业务测试、构建、迁移、部署、浏览器/CDP或真实接口；历史TAP中的116/98/247/123等计数仅来源，均不计本轮执行。
评审产物不嵌入自身最终Git SHA，不制造循环哈希。最终提交和远端一致性由Git提交图及最终答复报告。
