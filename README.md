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


## Mo hinh 3D (ban moi)
- Vu khi/dung cu/vat pham (kiem, cuoc, riu, xeng, cuoc dat, Rift Blade, Void Reaper, Voidpiercer, Gravity Staff, manh vo, thoi thep, to, loi, tao) la model 3D nhieu khoi, co phan phat sang.
- Den Khe Nut la model 3D (khung + loi xoay phat sang); quang co tinh the 3D moc ra.
- Quai vat co sung, ao choang, canh, duoi, giap vai, nga, tinh the tren lung (ModelExtras).
- Sinh bang: python3 tools/gen_data.py && python3 tools/gen_models.py
- Neu vu khi cam tay bi nghieng nguoc: doi DIAG = -45 thanh 45 trong tools/gen_models.py roi chay lai.

## Giap v3
- Texture giap mac tren nguoi + icon ve lai bang tools/gen_armor.py (chay SAU gen_art.py).
- Bo Thep Hu Khong: khang sat thuong + chay lua, giam 50% sat thuong no.
- Bo Hu Anh: nhanh + nhay cao, khong mat mau khi roi.

## Phep thuat & Magitech (ban moi)
- **Truong Bop Me Khong Gian (Warp Rod)**: chuot phai tao lo den hut quai vat roi no.
- **Mat Nhin Thuc Tai (Eye of the Void)**: cam tren tay -> khung mau xuyen tuong quanh quang, sinh vat (ke ca tang hinh) phat sang.
- **May Dich Chuyen Tuc Thoi (Void Gateway)**: dat >= 2 may, chuot phai de nhay sang may ke tiep (Shift: may truoc). Ton Manh Hu Khong trong tui do (xa/khac chieu hon ton nhieu hon).
- **Thac Nuoc Nguoc (Void Flux)**: dat lo, phun dong chay nguoc len troi toi da 28 khoi; sinh vat va vat roi bi day bay len, giu Shift de lo lung.
- **Void Wisp** (dung Loi Wisp hoac trung): dong hanh bay quanh, toa sang, tu nhat vat pham roi xuong vuc.
- **Chim Rinh Rap Hu Khong**: xuat hien o End va vung nui; cho an Tao/Banh Hu Khong de thuan hoa, chuot phai de cuoi (nhin len/xuong de bay, W lao toi, Shift xuong).
- **Day Thung Trong Luc (Void Tether)**: chuot phai moc vao khoi, tu keo toi do; Shift tha; roi cham sau khi tha.
- **Banh Chuoi Hu Khong (Void Fruit)**: an de co Levitation 3 giay + Slow Falling.
- Thu tu sinh asset: gen_art -> gen_data -> gen_models -> gen_armor -> gen_magitech.

## Void Realm - chiều không gian mới & Đền Tế (bản mới)
- **Đền Tế Hư Không** (`voidrealm:void_sanctum`, hiếm, ở Overworld): 8 cột đá khổng lồ, đền thờ ở giữa với **Bàn Tế**, sau lưng đền là cổng 5x5 (khung `void_portal_frame`).
  Tìm bằng `/locate structure voidrealm:void_sanctum`.
- **Kích hoạt cổng**: ném **Trứng Rồng Ender** (Dragon Egg dạng vật phẩm) vào Bàn Tế. Nghi lễ diễn ra nhiều giai đoạn (sét thị giác, tia sáng từ 8 cột, khung cổng sáng dần), cuối cùng mặt cổng xuất hiện. Bước vào cổng để sang **Void Realm** (`voidrealm:void_realm`).
- **Void Realm**: chiều kiểu End không có địa hình, chỉ có các **đảo lơ lửng** (tinh thể, đền đổ nát, cây tinh thể, tháp nhọn) và đảo trung tâm **Nexus** (có cổng về). 3 biome: Hư Không Mênh Mông, Vườn Tinh Thể, Vực Sao. Rơi khỏi đảo = chết (void).
  Dùng lệnh: `/execute in voidrealm:void_realm run tp @s ~ 80 ~` (nếu cần).
- Khối mới: Gạch Lát, Cột, Đá Khắc, Đất Hư Không, Khối Tinh Thể, Bậc/Phiến Gạch Hư Không, Khung Cổng, Bàn Tế. Toàn bộ texture khối vẽ lại (có hoạt ảnh).
- 3 công trình cũ (Tháp Bia, Phế Tích, Pháo Đài) được xây lại đẹp hơn bằng khối mới.
- Sinh lại dữ liệu: `gen_art → gen_data → gen_models → gen_armor → gen_magitech → gen_blocks → gen_realm`.

## Dream Crystal (màu xanh dương)
- **Quặng Dream Crystal** (`dream_crystal_ore`): chỉ có trong chiều Void Realm, rất hiếm, mọc thành cụm 3-5 khối ở phần dưới/sườn các đảo lơ lửng. Cần cuốc kim cương trở lên; hỗ trợ Fortune/Silk Touch. Rơi ra `dream_crystal`.
- **Kiếm Mộng Tinh**: 13.5 sát thương, làm chậm mục tiêu 2 giây.
- **Rìu Chiến Mộng Tinh**: 15 sát thương, bỏ qua giáp của mọi sinh vật.
- **Nỏ Mộng Tinh**: nạp cực nhanh, mũi tên +7 sát thương và phát sáng (chế từ nỏ thường + Dream Crystal + Thép Hư Không).
- **Bộ giáp Mộng Tinh** (khi mặc đủ 4 món): chestplate cho lướt như elytra (nhảy khi đang rơi); phím **C** = tăng tốc như pháo hoa (khi đang lướt); phím **K** = xúc tu xanh đánh kẻ địch trong 8 block (hồi chiêu 3 giây). Đổi phím ở Controls > Void Realm. Trên Zalith hãy gán nút điều khiển ảo cho C và K.
- Cánh lướt dùng texture elytra mặc định.
- Sinh lại dữ liệu: `... gen_blocks → gen_dream → gen_realm`.

## Texture khối bản liền mạch
- Mọi texture khối nền dùng nhiễu tuần hoàn (tileable) nên các khối cạnh nhau nối liền, không thấy đường ghép.
- Đá Hư Không và Khối Tinh Thể xoay ngẫu nhiên 4 hướng (blockstate) để tránh lặp họa tiết.

## Texture do người chơi tùy chỉnh
Toàn bộ texture hiện là bản người dùng tự chỉnh (đã ghép vào repo). **Không chạy lại** `tools/gen_art.py`, `gen_armor.py`, `gen_blocks.py`, `gen_dream.py`... vì chúng sẽ ghi đè texture.

## Mũi Khoan Mộng Tinh (`dream_drill`)
- **Shift + chuột phải**: bật/tắt chế độ đào 3x3 (vuông góc với mặt đang đào).
- **Giữ chuột phải** (không shift) ~1.5 giây: tích lực rồi thả để bắn tia năng lượng phá hủy mọi khối trong vùng 3x3 dài 20 block theo hướng nhìn (hồi chiêu 5 giây, tốn độ bền).
- Công thức: 5 Dream Crystal + Cuốc Thép Hư Không + Thỏi Thép Hư Không.
- Mọi vũ khí và dụng cụ (kiếm, rìu, cuốc, xẻng, cuốc đất, lưỡi hái, giáo, trượng) nay dùng icon 2D phẳng; riêng Trượng Bóp Méo, Mắt Hư Không, Dây Thừng vẫn là model 3D.
