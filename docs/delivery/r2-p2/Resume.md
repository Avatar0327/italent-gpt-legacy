# R2 P2恢复检查点

本窗口独立工作树`/workspace/sites/italent-hris-r2-p2-20260910`，分支`design/r2-p2-20260910`，远端`r2-p2-origin`（Sites源码仓库，仅推设计分支，无publish-on-push）。main启动固定`22be3a7e366d6787180d4f593a30f5984c70e03a`。当前材料的外部包标识以该分支实际完整Git HEAD为准，不把自身commit SHA写入自身文件制造循环依赖。

已完成：共用架构→M37→M06→M26→M18→M17→M03→六基础→两轮自检；无在制模块。下一步是所有者P2退出评审及总控受理登记提案，本窗口不自动实施P3。P2退出批准=false，P3进入=false，产品/部署/迁移/真实服务均未执行。

恢复步骤：

1. 只读`git worktree list`、当前分支/HEAD/status及远端对应ref，确认仍为本人工作树；若有后续合法提交先比较、保留，不reset或覆盖。
2. 读取Design_Checkpoint.json、Exit_Review.md、Review_Round1/2.md、Source_Manifest.json及Controller_Proposal.json；Scope仍仅总控可写，批准原文以启动固定Git对象核验。
3. 如只需复核，运行`python docs/delivery/r2-p2/check_design.py --unit resume-doc-check --final`，它只写本目录artifact manifest/evidence；不运行仓库P1检查器、产品测试、build、迁移或部署。
4. 如编辑生成源，按顺序运行build_inventory.py → build_resolution.py → build_scenarios.py → build_schemas.py → build_handoff.py，再check_design.py；所有输出仅本目录。原始方案设计在各Markdown、manual数组及生成脚本中；不得直接改派生数量掩盖未解决引用。
5. 完成授权的文档修改后检查diff范围、独立commit、正常push设计分支、用ls-remote核完整HEAD。短效凭据到期经Sites续取无发布凭据，不保存token，不在失败时强推。

每个实质单元有独立commit和对应evidence文件；evidence.atHeadBeforeCommit是检查时父HEAD，不是最终提交自身。历史检查应从相同Git提交读取相应Artifact_Manifest，当前清单不代表过去版本。当前sourceRequest均未执行，LIMIT原6组仍受限；不能把138个场景文件存在当测试通过。

禁止事项沿启动授权：不改main/P1/R1/R3或产品、不迁移/部署/新增访问者/真实外发/原站CDP/子代理，不自批P2退出，不进入R2 P3。R1 P3工作树期间有其他窗口合法推进，只观察Git元数据，不纳入本窗口完成证据或写入边界。
