import os
import sys
import argparse
from PIL import Image

# Lấy bbox phần thực
def square(img):
    alpha = img.split()[-1]
    return alpha.getbbox()

# Đổi màu (nếu có) cho phần thực
def recolor(image, new_rgb_color):
    if not new_rgb_color:
        return image
    else:
        data = image.getdata()
        new_data = []
        for r, g, b, a in data:
            if a != 0:
                new_data.append((*new_rgb_color, 255))
            else:
                new_data.append((22, 21, 19, 0))
        image.putdata(new_data)
        return image

def overlay_icon(cat_img, mask_img, icon_img, scale, new_color):
    # Lấy bbox phần thực trong ảnh mask
    square_box = square(mask_img)
    if not square_box:
        raise ValueError("file mask_png không hợp lệ")  # Nếu không có vùng alpha, báo lỗi

    # Tính kích thước phần thực
    width = square_box[2] - square_box[0]
    height = square_box[3] - square_box[1]

    # Lấy phần thực trong icon
    icon_bbox = square(icon_img)
    if not icon_bbox:
        raise ValueError("file icon_png không hợp lệ")
    icon_cropped = icon_img.crop(icon_bbox)

    # Kích thước icon sau cắt
    icon_width, icon_height = icon_cropped.size

    # Resize icon để vừa với vùng mask
    scale = min(width / icon_width, height / icon_height) * (scale / 100)
    new_size = (int(icon_width * scale), int(icon_height * scale))
    resized_icon = icon_cropped.resize(new_size, Image.LANCZOS)

    # Đổi màu (nếu có) cho icon để đè lên pattern   !!! Cần để sau khi resize để
    if new_color:
        resized_icon = recolor(resized_icon, new_color)

    # Tính vị trí paste icon để nằm giữa vùng mask
    paste_x = square_box[0] + (width - new_size[0]) // 2
    paste_y = square_box[1] + (height - new_size[1]) // 2

    # Tạo một ảnh trống cùng kích thước với pattern
    overlay = Image.new("RGBA", cat_img.size, (22, 21, 19, 0))  # nền trong suốt

    # Dán icon đã resize lên ảnh trống tại vị trí đã tính
    overlay.paste(resized_icon, (paste_x, paste_y), resized_icon)  # dùng alpha làm mask

    # Gộp lớp overlay với icon
    return Image.alpha_composite(cat_img, overlay)

# Tìm các đường dẫn đến file ảnh từ thư mục, file .txt hoặc trực tiếp
def find_paths(inputs):
    all_paths = []
    for item in inputs:
        # Loại bỏ dấu nháy, khoảng trắng thừa
        item = item.strip().strip('"').strip("'").strip()

        # Nếu là thư mục: duyệt toàn bộ file nằm trực tiếp trong thư mục
        if os.path.isdir(item):
            for file in os.listdir(item):
                if file.lower().endswith(".png"):
                    all_paths.append(os.path.join(item, file))

        # Nếu là file .txt: đọc từng dòng để lấy đường dẫn icon .png
        elif os.path.isfile(item) and item.lower().endswith(".txt"):
            with open(item, 'r', encoding='utf-8') as f:
                for line in f:
                    path = line.strip().strip('"').strip("'").strip() # Loại bỏ dấu nháy, khoảng trắng thừa
                    if os.path.isfile(path) and path.lower().endswith(".png"):
                        all_paths.append(path)

        # Nếu là file .png
        elif os.path.isfile(item) and item.lower().endswith(".png"):
            all_paths.append(item)
    return all_paths

#Thêm stt để tránh ghi đè file
def fix_path(path):
    if not os.path.exists(path):
        return path
    else:
        base, ext = os.path.splitext(path)
        count = 1
        new_path = f"{base} ({count}){ext}"
        while os.path.exists(new_path):
            count += 1
            new_path = f"{base} ({count}){ext}"
        print(f"Ten file ({path}) trung lap, da luu voi ten moi: {os.path.basename(new_path)}")
        return new_path

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Cong cu tao icon meo klein cho ung dung\n\n(Luu y: Neu trong ten anh/thu muc co chua dau cach thi can su dung dau nhay kep\nVD: \"D:\\Hinh Nen\\Klein cat.png\").",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-s", metavar="output_folder", help="Duong dan den thu muc de luu cac anh ket qua.", required=True)
    parser.add_argument("-r", metavar=("cat_png", "mask_png"), nargs=2, help="Duong dan den hai anh (.png): (1) anh meo klein (2) anh khop hinh tron.", required=True)
    parser.add_argument("-f", metavar="icon_png", nargs='+', help="Duong dan den:\nCac anh icon ung dung (.png)\nhoac thu muc chua cac anh icon ung dung (.png)\nhoac file (.txt) chua cac anh icon ung dung (.png).", required=True)
    parser.add_argument("-p", metavar="ty_le_resize", type=int, default=100, help="Ty le resize icon_png theo mask_png (%%) (mac dinh: 100).")
    parser.add_argument("-c", metavar="new_color", help="Mau moi (neu can) (dinh dang R,G,B (0<=x<=255))")
    args = parser.parse_args()
    if args.c:
        try:
            new_color = tuple(map(int, args.c.split(",")))
            if len(new_color) != 3 or not all(0 <= x <= 255 for x in new_color):
                raise ValueError
        except ValueError:
            print("Tham số -c phải ở dạng R,G,B (mỗi giá trị từ 0 đến 255).")
            sys.exit(1)
    else:
        new_color = None
    cat_img_path, mask_img_path = args.r
    output_folder = args.s
    icon_paths = find_paths(args.f)

    # Ktra và mở ảnh gốc
    if not icon_paths:
        print("Khong tim thay bat ky file .png nao tu cac dau vao.")
        sys.exit(1)
    os.makedirs(output_folder, exist_ok=True)
    try:
        cat_img = Image.open(cat_img_path).convert("RGBA")
        mask_img = Image.open(mask_img_path).convert("RGBA")
    except Exception as e:
        print(f"Loi khi mo anh dau vao: {e}")
        sys.exit(1)

    # Xử lí từng icon
    for icon_path in icon_paths:
        #Mở và chồng icon lên ảnh gốc
        try:
            icon_img = Image.open(icon_path).convert("RGBA")
        except Exception as e:
            print(f"Loi khi mo anh {icon_path}: {e}")
            continue
        try:
            result = overlay_icon(cat_img, mask_img, icon_img, args.p, new_color,)
        except Exception as e:
            print(f"Loi khi chong icon {icon_path}: {e}")
            continue

        # Lưu ảnh
        icon_name = os.path.splitext(os.path.basename(icon_path))[0]
        output_path = os.path.join(output_folder, f"cvt_{icon_name}.png")
        output_path = fix_path(output_path)
        try:
            result.save(output_path)
            print(f"Da luu {icon_path} o {output_path}")
        except Exception as e:
            print(f"Loi khi luu anh ket qua {output_path}: {e}")
            continue

