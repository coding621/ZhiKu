# SQLite FTS5 中文检索要点

做本地知识库搜索时的结论记录。

## 问题

FTS5 默认的 `unicode61` 分词器**不切分中文**，整句会被当作一个 token，
`MATCH '知识'` 永远匹配不到「知识库构建」。

## 两种可用方案

### 1. trigram 分词器

```sql
CREATE VIRTUAL TABLE fts USING fts5(content, tokenize='trigram');
```

- 按 3 字符滑窗建索引，中文、英文、混合文本都能子串匹配
- **限制：查询词必须 ≥ 3 个字符**，`技术`（2 字）查不到
- 适合查询词普遍较长的场景

### 2. LIKE 预筛 + Python 计分（本知识库采用）

```python
rows = conn.execute(
    "SELECT * FROM docs WHERE content LIKE ? ESCAPE '\\'",
    (f"%{term}%",)
)
```

- 个人知识库规模（千级文档）下全表扫描完全够快
- 无分词词典依赖，2 字中文查询也能命中
- 自己控制排序：出现次数、标题命中加权、时间衰减

## 结论

| 场景 | 选择 |
| --- | --- |
| 文档量 < 1 万，查询多为 2 字中文 | LIKE + 自建计分 |
| 文档量大、查询词 ≥ 3 字 | FTS5 trigram |
| 需要同义词/模糊纠错 | 上 jieba + 倒排 或向量检索 |

相关：见 [[学习资料/深度工作-读书笔记]] 中关于检索与记忆的讨论。
