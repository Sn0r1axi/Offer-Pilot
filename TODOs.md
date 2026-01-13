PART I  ------  Ingestion based on Crawl4AI  多模态数据采集与清洗模块
1.一键实时爬取 QS Ranking
2.获取 QS Rangking对应学校网站
3.生成爬取网站列表
4.支持细化每个学校网站的爬取路径（避免算力浪费，Attention Distraction etc.
5.开爬


PART II ------ Retrieval 混合索引构建与知识图谱生成
1.GraphRAG生成
GraphRAG (Graph-based Retrieval-Augmented Generation) 是2024-2025年RAG领域的重大突破 。它利用LLM从文档中提取实体（Entities）和关系（Relationships），构建知识图谱。
e.g.
实体节点： 具体的大学（University）、专业（Program）、申请要求（Requirement）、截止日期（Deadline）。
关系边： University --offers--> Program，Program --requires--> TOEFL_Score，Program --belongs_to--> STEM_List。

2.基于GraphRAG的复杂问题处理

PART III------ API based on FastAPI
异构数据输入支持（文本、图片等）
高并发请求处理与优化

PART IV ------ Frontend
1.基于Streamlit的用户界面（前后端分离）
2.前端实现：qs排名获取，爬取路径定制，爬取进度展示，对话界面等
2.多轮对话支持
3.结果可视化与导出功能

业务流程
1.用户通过前端界面提交QS排名爬取请求。
2.后端接收请求，调用爬虫模块进行数据采集。
3.爬取的数据经过预处理后，构建GraphRAG知识图谱
4.用户通过前端界面提交查询请求。
5.后端基于GraphRAG进行多跳检索与Agentic RAG，生成回答。
6.前端展示回答结果，并支持多轮对话与结果导出。