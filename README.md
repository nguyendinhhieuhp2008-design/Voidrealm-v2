# Void Realm (Cõi Hư Không) — mod Minecraft Java 1.21.1 NeoForge

Mang vũ khí, giáp, vật phẩm, quái vật và công trình từ một không gian khác vào Overworld.
Thiết kế nhẹ cho **Zalith Launcher 2** (Android): không phụ thuộc mod khác, dùng model vanilla,
texture 16x16, ít hạt (particle), có file cấu hình `config/voidrealm-common.toml`.

## Nội dung
- **Vật liệu**: Mảnh Hư Không (quặng sinh tự nhiên, tầng -64..32), Thỏi Thép Hư Không, Tơ Hư Ảnh, Lõi Khe Nứt, Táo Hư Không.
- **Bộ Thép Hư Không**: kiếm, cuốc chim, rìu, xẻng, cuốc + giáp 4 món (mặc đủ bộ: kháng sát thương + chống cháy).
- **Vũ khí đặc biệt**: Kiếm Xé Không Gian (chuột phải lao tới), Lưỡi Hái Hư Vô (Héo Mòn + hút máu), Giáo Xuyên Hư Không (tầm với +2), Trượng Trọng Lực (kéo quái về phía bạn).
- **Giáp Hư Ảnh**: nhẹ, mặc đủ bộ được tăng tốc + nhảy cao.
- **6 quái vật**: Kẻ Lang Thang Hư Không, Cung Thủ Dị Giới, Kẻ Rình Rập Hư Ảnh (dịch chuyển), Lợn Rừng Hư Không, Hộ Pháp Dị Giới, và boss **Chúa Tể Hư Không** (thanh máu, xung hư không, gọi đồng bọn).
- **3 công trình**: Tháp Bia Hư Không (có spawner + rương trên đỉnh), Phế Tích Dị Giới (bàn thờ + spawner), Thành Trì Hư Không (boss, 2 Hộ Pháp, 4 tháp góc, rương loot).
- **Khối**: quặng (thường + deepslate), Đá/Gạch Hư Không, Khối Thép, Đèn Khe Nứt. Mọi món có công thức chế tạo.
- **Đồ họa & hiệu ứng**: texture quái vẽ chi tiết kèm lớp phát sáng (mắt, rune, vết nứt dung nham) bằng RenderType vanilla; khối động (quặng lấp lánh, đèn xoáy, rune thép nhấp nháy, đá hư không đầy sao); vũ khí có ánh phù phép, vệt hạt khi dịch chuyển/đánh trúng; boss có vòng hạt xoáy, sóng xung và hiệu ứng chết; giáp có hạt khi mặc đủ bộ. Tất cả hạt giảm được bằng `particlePercent`.
- Ngôn ngữ: Tiếng Việt (vi_vn) và English.

## Lấy file .jar (không cần cài gì trên điện thoại)
Mod chưa được biên dịch sẵn. Cách dễ nhất là để GitHub tự build:
1. Tạo 1 repository GitHub mới (có thể để private), upload toàn bộ nội dung thư mục này lên (giữ nguyên cấu trúc, gồm cả thư mục `.github`).
2. Vào tab **Actions** → workflow **Build** chạy tự động (hoặc bấm *Run workflow*).
3. Khi xong, mở lần chạy đó → mục **Artifacts** → tải `voidrealm-jar` (file zip chứa `voidrealm-1.0.0.jar`).

Hoặc trên máy tính có JDK 21: `./gradlew build` → jar nằm ở `build/libs/`.

## Cài vào Zalith Launcher 2
1. Trong Zalith: tạo phiên bản **Minecraft 1.21.1** và cài **NeoForge 21.1.x** (mục tải phiên bản → NeoForge).
2. Chép `voidrealm-1.0.0.jar` vào thư mục `mods` của phiên bản đó.
3. Nên cấp RAM 2–3 GB trong cài đặt phiên bản; dùng Java 21.
4. Tăng hiệu năng: giảm `particlePercent` trong `config/voidrealm-common.toml` (mặc định 50), giảm Simulation/Render Distance.

## Tùy chỉnh
- `tools/gen_art.py` (đồ họa nâng cấp, chạy cái này để sinh lại toàn bộ texture), `tools/gen_textures.py`, `tools/gen_data.py`, `tools/gen_structures.py` sinh lại texture, model/lang/công thức/loot/worldgen và công trình (.nbt).
- Bản mod này viết trên API NeoForge 21.1.x; môi trường tạo ra nó không biên dịch được, nên nếu build báo lỗi hãy gửi nội dung lỗi để sửa.
