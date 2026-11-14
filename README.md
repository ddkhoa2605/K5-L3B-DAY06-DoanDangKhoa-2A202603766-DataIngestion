# Day 06 · Data Ingestion Engineering

**Lab cá nhân** · **4 giờ** · **Dữ liệu tự chọn**

Biến tài liệu thành kho tri thức có thể truy xuất cho AI agent, rồi đo xem cách chuẩn bị dữ liệu nào hiệu quả nhất.

| 📄 Dữ liệu | 🧩 Chiến lược | 🎯 Benchmark |
|---|---|---|
| Tối thiểu **30 trang nội dung** | Tối thiểu **3 cấu hình** | Tối thiểu **20 câu hỏi** |

## Bắt đầu nhanh

Dùng [starter PostgreSQL + pgvector](starter/README.md) để dựng database và hoàn thiện các hàm TODO, hoặc tự chọn vector store tương đương. Starter chỉ là khung: **bạn tự hiện thực pipeline và benchmark**.

## 1. Xây pipeline

![Đọc tài liệu, chuẩn hóa, chia chunk, tạo vector, lưu và kiểm tra](assets/ingestion-pipeline.svg)

Chọn tài liệu được phép sử dụng; giữ **ID tài liệu, nguồn, trang/vị trí** và metadata phù hợp. Dùng embedding model thật qua API hoặc chạy local; lưu và truy xuất bằng pgvector, Qdrant, Chroma hoặc một store tương đương.

## 2. So sánh và đánh giá

![Ba chiến lược được đánh giá trên cùng corpus và benchmark dev/test](assets/benchmark-workflow.svg)

Dùng cùng dữ liệu, model và câu hỏi cho cả ba cấu hình. Tách **15 câu dev / 5 câu test** trước khi chạy; chọn cấu hình trên dev, rồi đánh giá test sau khi cố định. Mỗi câu hỏi cần có đoạn bằng chứng và trang nguồn; thiết kế bộ câu hỏi và đánh giá theo [BENCHMARK.md](BENCHMARK.md).

Đánh giá theo năm khía cạnh: **độ chính xác truy xuất**, **tính mạch lạc của chunk**, **tính hữu dụng của metadata**, **chất lượng grounding** và **tác động của chiến lược dữ liệu**. Giải thích lựa chọn bằng kết quả, ví dụ lỗi và các đánh đổi.

## 3. Chuẩn bị bài nộp

1. Chạy pipeline và lưu cấu hình, kết quả top-3, trace cùng nhãn đánh giá thủ công.
2. Điền [thông tin học viên](STUDENT.md), [nhật ký thí nghiệm](artifacts/experiment_log.csv) và bản sao [mẫu báo cáo cá nhân](report/individual/MSSV_HoTen.md).
3. Kiểm tra mã nguồn, cách chạy, manifest dữ liệu và checklist trong [SUBMISSION.md](SUBMISSION.md).

## Tài liệu hướng dẫn

| Bạn cần tìm | Tài liệu |
|---|---|
| Setup baseline PostgreSQL + pgvector | [starter/README.md](starter/README.md) |
| Các bước làm và cách tính chỉ số | [GUIDE.md](GUIDE.md) |
| Tiến độ trong 4 giờ | [CHECKPOINTS.md](CHECKPOINTS.md) |
| Năm tiêu chí benchmark và bộ câu hỏi | [BENCHMARK.md](BENCHMARK.md) |
| Tiêu chí chấm điểm | [RUBRIC.md](RUBRIC.md) |
| Quy tắc sử dụng dữ liệu, AI và API | [RULES.md](RULES.md) |
| Cách nộp bài | [SUBMISSION.md](SUBMISSION.md) |

[data/format-example.json](data/format-example.json) chỉ minh họa định dạng, không phải corpus đủ điều kiện. Phần xử lý và benchmark do bạn tự hiện thực; không bắt buộc xây chatbot.

---

## Bài làm: Python 3.13 Docs + ChromaDB

Corpus: 10 file tài liệu Python 3.13 (6 Tutorial + 4 Library), 117 đơn vị trang ≥1.500 ký tự. Embedding local `sentence-transformers/all-MiniLM-L6-v2` (384 chiều), vector store ChromaDB 1.5.9 persistent (cosine, HNSW). Ba chiến lược: A fixed 500/50, B theo heading/đoạn ≤1.000, C = B + lọc `doc_type`.

```bash
cd starter
python -m venv .venv            # Windows: .venv\Scripts\Activate.ps1 ; Unix: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m src.run all           # prepare -> validate -> ingest -> evaluate
python scripts/make_audit_sheets.py   # sheet đọc để chấm thủ công
python scripts/audit_summary.py       # kiểm tra metadata + tổng hợp nhãn
python scripts/test_reingest.py       # kiểm tra nạp lại / tài liệu đổi (Chroma tạm)
```

Lần chạy đầu cần mạng để tải archive tài liệu (4,2 MB) và model (~90 MB). Không cần API key, chi phí 0.

| Đường dẫn | Nội dung |
|---|---|
| `starter/src/` | ingestion, chunking, embeddings, store (Chroma), evaluation, run |
| `data/manifest.json`, `data/pages.jsonl`, `data/corpus/` | manifest nguồn/quyền/đơn vị trang, text đã chuẩn hóa, file gốc |
| `benchmark/questions.json` | 28 câu (22 dev / 6 test), gold page + evidence |
| `artifacts/experiment_log.csv` | cấu hình và giả thuyết A/B/C |
| `results/` | trace top-3, chỉ số, thống kê ingest, nhãn audit |
| `report/individual/2A202603766_DoanDangKhoa.md` | báo cáo cá nhân |
