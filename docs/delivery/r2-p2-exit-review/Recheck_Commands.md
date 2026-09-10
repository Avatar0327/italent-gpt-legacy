# 本轮独立核验命令与证据

仅固定Git对象、文档解析/生成及符号计算。产品测试、数据库、迁移、构建、部署、浏览器/CDP和业务接口执行均为0。生成脚本只在临时副本写文档；新独立脚本只在本评审目录保存Recheck记录。

## 初始归属与不可变引用

在`/workspace/sites/italent-hris-r2-p2-exit-review-20260910`执行：

```bash
git worktree list --porcelain
git status --short --branch
git rev-parse HEAD
git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}'
git cat-file -t dc6dd896fbf388b70069ecb756547f85ee89d08a
git cat-file -t a7a23d6bff024f4660fd14b0c22f47a6d40d928f
git cat-file -t 7ff3a28c7660dac658d5243d7c4535a9c8037fc2
git cat-file -t 8b3daf9270181ffe2e77015be723da8e611d83a5
git rev-parse a7a23d6bff024f4660fd14b0c22f47a6d40d928f^
git diff --name-status dc6dd896fbf388b70069ecb756547f85ee89d08a a7a23d6bff024f4660fd14b0c22f47a6d40d928f
git diff --name-status 8b3daf9270181ffe2e77015be723da8e611d83a5 a7a23d6bff024f4660fd14b0c22f47a6d40d928f
git ls-remote r2-p2-origin refs/heads/review/r2-p2-exit-20260910 refs/heads/design/r2-p2-20260910
```

初始结果：评审bd976480、设计a7a23d6，本地/远端一致，评审工作区干净；5个固定提交可读取。主分支22be3a7、R1设计e152372未被本窗口改动。R1在制分支推进单独只读记录。

## 隔离依赖与复算

本轮临时目录为`/workspace/scratch/a94fcceed57f/r2-recheck.AzRoIc`。使用独立venv，不向产品安装任何依赖，不修改产品manifest/锁文件。安装jsonschema 4.23.0初期遇到代理超时重试，最后由缓存wheel成功安装；另曾只读复制已有任务缓存准备离线回退，但最终三个核验程序均使用成功安装的新venv，未使用该回退副本。

```bash
python3 -m venv /workspace/scratch/a94fcceed57f/r2-recheck.AzRoIc/validator-env
/workspace/scratch/a94fcceed57f/r2-recheck.AzRoIc/validator-env/bin/python -m pip install jsonschema==4.23.0
PYTHONDONTWRITEBYTECODE=1 /workspace/scratch/a94fcceed57f/r2-recheck.AzRoIc/validator-env/bin/python docs/delivery/r2-p2-exit-review/recheck_forward.py --record
PYTHONDONTWRITEBYTECODE=1 /workspace/scratch/a94fcceed57f/r2-recheck.AzRoIc/validator-env/bin/python docs/delivery/r2-p2-exit-review/recheck_reverse.py --record
PYTHONDONTWRITEBYTECODE=1 /workspace/scratch/a94fcceed57f/r2-recheck.AzRoIc/validator-env/bin/python docs/delivery/r2-p2-exit-review/recheck_generation.py
```

实际venv由已有Python 3.12运行时创建；恢复时可用相同版本在新临时目录重建，不必依赖临时路径长期存在。程序的固定SHA写在源码中，不跟随设计分支。正反两轮不调用产品，不导入设计窗口检查器，也不互相导入。它们共享标准JSON Schema库与固定输入，不共享分组或拓扑算法。

第一轮：2199项检查0失败；第二轮：963项0失败。34例9接受25拒绝（15结构、10语义查表）；16例5允许11抑制；55节点165边0环；76命令、49额外完整Command探针、3适配和6 LIMIT均符合预期。

重建单独调用已审阅的build_inventory/build_scenarios/build_schemas、文档样例检查、build_resolution/build_handoff、基础适配/DAG文档检查，`GIT_DIR`仅供读取既有Git对象；工作目录固定为新临时副本。75个非证据/非清单文档源与派生文件逐字节无漂移。没有运行含工作树浮动diff判断的设计方check_repair，也未将设计方自检作为独立结论。

## 哈希核验方法

`recheck_forward.py`逐个`git show <固定SHA>:<path>`读取原字节，再执行SHA256，不重序列化JSON。44项proposal引用核dc6dd896；Artifact_Manifest分别在dc6dd896/a7a23d6/7ff3a28/8b3daf9各自对象核清单条目。清单不包含自身或evidence输出，避免循环；包装的动态清单不与固定内容清单交叉比较。

78个Source_Manifest条目、11个Repair_Record独立评审来源及各LIMIT输入/证据链同法核验。`Recheck_Input_Hashes.json`保留实际读取对象的字节数与SHA256；`Recheck_Limits.json`含每项probe、输入/证据摘要和完整后续责任；`Recheck_Verification.json`索引本轮独立证据，不含自身哈希。

## 交付检查与推送

```bash
PYTHONDONTWRITEBYTECODE=1 /workspace/scratch/a94fcceed57f/r2-recheck.AzRoIc/validator-env/bin/python docs/delivery/r2-p2-exit-review/record_recheck.py --record
PYTHONDONTWRITEBYTECODE=1 python3 docs/delivery/r2-p2-exit-review/record_recheck.py --check
git diff --check
git diff --name-only bd976480fad9822ee52ecb4b00a080360772b0f3
git log --format='%H %s' bd976480fad9822ee52ecb4b00a080360772b0f3..HEAD
git push r2-p2-origin HEAD:refs/heads/review/r2-p2-exit-20260910
git ls-remote r2-p2-origin refs/heads/review/r2-p2-exit-20260910
git status --porcelain
git rev-list --left-right --count HEAD...r2-p2-origin/review/r2-p2-exit-20260910
```

网络Git使用项目正常配置的短期凭据，仅命令级认证；凭据不写仓库或本记录、不启用publish-on-push。若未知推送结果，先ls-remote核实，不能强推。最终提交/远端回执以`Recheck_Delivery_Record.json`与包含其后续回执的Git HEAD为准，避免自指哈希。
