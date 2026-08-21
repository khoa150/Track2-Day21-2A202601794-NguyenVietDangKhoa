# Báo Cáo Lab Day 21 - CI/CD cho AI Systems

|              |                                              |
| ------------ | -------------------------------------------- |
| Họ và tên    | Nguyễn Việt Đăng Khoa                       |
| MSSV         | 2A202601794                                  |
| Lớp / Khóa  | K4                                           |
| Repo GitHub  | https://github.com/khoa150/Track2-Day21-2A202601794-NguyenVietDangKhoa |
| Ngày nộp     | 21/08/2026                                   |

---

## 1. Bộ Siêu Tham Số Đã Chọn và Lý Do

| Lần chạy | n_estimators | learning_rate | max_depth | f1_score | accuracy |
| --------- | ----------- | ------------- | --------- | -------- | -------- |
| 1         | 150         | 0.15          | 4         | 0.7182   | 0.876    |
| 2         | 200         | 0.1           | 5         | 0.7149   | 0.874    |
| 3         | 50          | 0.05          | 2         | 0.6051   | 0.846    |

**Bộ siêu tham số đã chọn:** `n_estimators=150`, `learning_rate=0.15`, `max_depth=4`.

**Lý do:** Bộ tham số này đạt f1_score cao nhất (0.7182) trong 3 lần chạy. Lần chạy 3 có accuracy cao nhất (0.846) nhưng f1_score lại thấp nhất (0.6051), chứng tỏ accuracy không phản ánh đúng chất lượng mô hình. Quan sát thấy khi giảm learning_rate thì cần tăng n_estimators để bù lại.

---

## 2. Vì Sao Ngưỡng Chất Lượng Đặt Trên F1 Chứ Không Phải Accuracy

Tập dữ liệu Adult có tỷ lệ thu nhập trên 50K chỉ 24.8%, nên mô hình luôn trả lời "thu nhập thấp" đã đạt accuracy 75.2% dù hoàn toàn vô dụng. F1 score đo cân bằng precision và recall của lớp dương, phản ánh đúng mô hình có học được gì không. Không nên dùng average="weighted" vì bị lớp đa số kéo lên, che giấu việc bỏ sót thu nhập cao.

---

## 3. Khó Khăn Gặp Phải và Cách Giải Quyết

| Khó khăn | Nguyên nhân | Cách giải quyết |
| --------- | ----------- | ---------------- |
| Service trên EC2 không khởi động được | Thiếu thư viện fastapi, boto3 trên VM | Cài đặt thủ công các thư viện cần thiết bằng pip3 |
| GitHub Actions SSH deploy fail | Service chưa được tạo trên EC2 | Tạo systemd service file và enable income-api.service |
| DVC push lỗi thiếu module | Chưa cài dvc-s3 | Cài đặt dvc-s3 bằng pip install dvc-s3 |

---

## 4. So Sánh Bước 2 và Bước 3

|                      | f1_score | accuracy |
| -------------------- | -------- | -------- |
| Bước 2 (chỉ train_batch1) | 0.7182   | 0.876    |
| Bước 3 (thêm train_batch2) | 0.7175   | 0.874    |

**Nhận xét:** F1 score giảm nhẹ 0.0007 khi tăng gấp đôi dữ liệu từ 22361 lên 44722 mẫu. Nguyên nhân là hai nửa dữ liệu được chia ngẫu nhiên từ cùng một nguồn nên có cùng phân phối, dữ liệu mới không mang thêm thông tin mới cho mô hình học. Điều này cho thấy thêm dữ liệu không phải lúc nào cũng cải thiện mô hình.

---

