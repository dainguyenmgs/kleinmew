<!-- LOGO -->
<br />
<p align="center">
  <img src="https://github.com/user-attachments/assets/3581539a-accd-4ab4-952b-fc360bf88af7" alt="Logo" width="80" height="80">

  <h3 align="center">Kleinmew</h3>

  <p align="center">
    Công cụ tạo icon ứng dụng mèo klein
    <br />

</p>

## Cách tải xuống

#### Để bắt đầu, bạn cần có python3. Nếu chưa, hãy tải xuống tại [đây](https://www.python.org/downloads/).

#### Nếu bạn chưa tải thư viện Pillow, hãy chạy mã sau từ terminal:

```bash
pip install Pillow
```

#### Nếu bạn đã tải git, hãy chạy mã sau từ terminal để tải toa bộ mã về máy:

```bash
git clone https://github.com/dainguyenmgs/kleinmew.git
cd kleinmew
```

Ngoài ra, bạn cũng có thể tải xuống từng file một.

---

# Công cụ chuyển đổi MTZ sang ZIP (cvt_mtz.py)

Chuyển đổi file `.mtz` (theme của MIUI) thành file `.zip`.

---

## Giới thiệu

### File `.mtz` thực chất là file `.zip` được đổi đuôi. Bên trong đó chứa các file ví dụ như `com.android.systemui` hay `icon` thực chất cũng đều là các file `.zip` được xóa đuôi. Đoạn mã này giúp chuyển đổi file `.mtz` thành file `.zip` bằng cách thêm đuôi `.zip` cho các file như thế và giải nén. Ngoài ra còn có các file khác như `.jpg`, `.png` hay `.xml`, những file này sẽ được giữ nguyên

---

## Cách sử dụng

### Chạy từ terminal:

```bash
python cvt_mtz.py -f <duong_dan_den_file_.mtz> -s <duong_dan_ra_file_.zip> [-p <>]
```

### Tham số:

* `-s <output_zip>` *(bắt buộc)*: Đường dẫn đến file `.mtz`.
* `-f <input_mtz>` *(bắt buộc)*: Đường dẫn đến file `.zip` kết quả (tự đặt tên cho file mới)
* `-p <preserve_extensions>` *(không bắt buộc)*: Bỏ qua các file có đuôi này (mặc định: `.xml`, `.jpg`, `.png`).

### Ví dụ:

```bash
python cvt_mtz.py "D:\Py\hn cod\theme.mtz" "D:\Py\hn cod\theme_convert.zip" -p .xml,.jpg,.png,.txt
```

Lệnh trên sẽ:

* Đọc file `theme.mtz`.
* Chuyển file `theme.mtz` thành file `.zip`, bỏ qua các file có đuôi `.xml`, `.jpg`, `.png`, `.txt`
* Lưu kết quả vào thư mục `D:\Py\hn cod` dưới tên `theme_convert.zip`.

---

# Công cụ tạo icon ứng dụng mèo klein (crt_icon.py)

---

## Giới thiệu

### Đoạn mã này giúp tạo icon ứng dụng bằng cách ghép biểu tượng ứng dụng vào pattern mèo sẵn có trong file `.mtz` (`.\icons\res\drawable-xxhdpi\icon_pattern.png`) vào vị trí thích hợp đã được căn chỉnh trong một file `.png` sẵn có trong file `.mtz` (`.\icons\res\drawable-xxhdpi\icon_mask.png`)

---

## Cách sử dụng

### Chạy từ terminal:

```bash
python crt_icon.py -s <output_folder> -r <cat_png.png> <mask_png.png> -f <icon...> [-p <ty_le_resize>] [-c <new_color>]
```

### Tham số

* `-s <output_folder>` *(bắt buộc)*: Thư mục để lưu ảnh kết quả.
* `-r <cat_png.png> <mask_png.png>`: Hai ảnh định dạng `.png`:
  * `cat_png.png` *(bắt buộc)*: Ảnh gốc.
  * `mask_png.png` *(bắt buộc)*: Ảnh mask có vùng alpha hiển thị vùng cần chồng icon.
* `-f <icon...>` *(một hoặc nhiều)*:
  * Tệp `.png` icon cần chồng.
  * Thư mục chứa các `.png` icon cần chồng *(Lưu ý: các tệp `.png` phải nằm trực tiếp trong thư mục (thư mục con sẽ không được quét))*.
  * Tệp `.txt` chứa danh sách đường dẫn đến các `.png` icon cần chồng *(Lưu ý: mỗi hàng một đường dẫn)*.
* `-p <ty_le_resize>` *(không bắt buộc)*: Phần trăm resize icon (%) (mặc định: `100`).
* `-c <new_color>` *(không bắt buộc)*: Màu cần đổi, định dạng R,G,B (0<=x<=255)

### Ví dụ 1

```bash
python crt_icon.py -s "D:\Py\hn cod" -r "D:\Py\mtz\icons\res\drawable-xxhdpi\icon_pattern.png" "D:\Py\mtz\icons\res\drawable-xxhdpi\icon_mask.png" -f "D:\Py\logos" -p 80
```

Lệnh trên sẽ:

* Đọc ảnh `icon_pattern.png` và `icon_mask.png`.
* Tìm và tách các icon trong các tệp `.png` trong thư mục `logos`.
* Resize icon còn 80% kích thước bằng lanczos.
* Chồng icon lên ảnh gốc tại vùng mask.
* Lưu kết quả vào thư mục `D:\Py\hn cod`.
* Các icon được lưu với tên dạng: `cvt_<ten_file_logo>.png`

### Ví dụ 2

```bash
python crt_icon.py -s "D:\Py\hn cod" -r "D:\Py\mtz\icons\res\drawable-xxhdpi\com.android.soundrecorder.png" "D:\Py\mtz\icons\res\drawable-xxhdpi\icon_mask.png" -f "D:\Py\mtz\icons\res\drawable-xxhdpi\icon_mask.png" -p 120 -c 22,21,19
```

Lệnh trên sẽ:

* Đọc ảnh `com.android.soundrecorder.png` và `icon_mask.png`.
* Tìm và tách "icon" là phần ảnh thực (alpha>0) trong `icon_mask.png`.
* Resize icon lên 120% và đổi icon sang màu RGB #161513 (22,21,19) trùng với pattern mèo.
* Chồng icon lên ảnh gốc tại vùng mask.
* Lưu kết quả vào thư mục `D:\Py\hn cod` dưới tên `cvt_icon_mask.png`

Lưu ý:

* Lệnh trên dùng để tạo pattern mới từ ảnh đã chồng icon bằng cách đè lên phần icon trong ảnh bằng màu RGB 22,21,19 trùng với màu ảnh (cần resize hợp lý để che phủ toàn bộ icon)

### Lưu ý

* Ảnh mask cần có kênh alpha (vùng trong suốt). Vùng không trong suốt sẽ xác định vùng đặt icon.
