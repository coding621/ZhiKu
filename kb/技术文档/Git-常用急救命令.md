# 常用 Git 拯救手册

## 误提交但未推送

```bash
git commit --amend            # 修改最近一次提交信息或内容
git reset --soft HEAD~1       # 撤销最近一次提交，改动保留在暂存区
```

## 误推送（需团队协商后使用）

```bash
git revert <commit>           # 生成反向提交，历史安全，首选
git push --force-with-lease   # 比 --force 安全：远端有新提交时会拒绝
```

## 找回丢失的提交

```bash
git reflog                    # 所有 HEAD 移动记录
git reset --hard <sha>        # 回到指定状态
```

## 暂存手头改动去修线上 bug

```bash
git stash push -m "wip: feature x"
git stash list
git stash pop
```

## 忽略已跟踪的文件

```bash
git rm --cached <file>        # 只从索引移除，保留本地文件
# 然后把路径加进 .gitignore
```

> 原则：**已分享的历史用 revert，未分享的历史用 reset/amend。**
