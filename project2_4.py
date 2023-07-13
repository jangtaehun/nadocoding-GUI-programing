from tkinter import *
import os
import tkinter.ttk as ttk  # 콤보박스, 프로그래스바
from tkinter import filedialog  # 서브 모듈이라 별도로 명시해야한다.
import tkinter.messagebox as msgbox
from PIL import Image
from PIL import ImageGrab
import time
import keyboard

root = Tk()
root.title("ZZangtae Photo")
root.geometry("650x580+900+150")
#########################################################################
# 출력 경로


def add_file():
    # askopenfilenames 파일 선택
    files = filedialog.askopenfilenames(title="이미지 파일을 선택하세요",
                                        filetypes=(
                                            ("PNG 파일", "*.png"), ("모든 파일", "*.*")),
                                        initialdir=r"C:\Users\jangt\Downloads")  # 최초에 c:/ 경로를 보여준다.
    for file in files:
        list_file.insert(END, file)


def del_file():
    # curselection=위치반환
    # 거꾸로 반환 reversed=새로운 값을 반환 -> 실재 값에 영향을 주지 않는다.
    for index in reversed(list_file.curselection()):
        list_file.delete(index)

# 저장 경로(폴더)


def browse_dest_path():  # askdirectory 폴더 선택
    folder_selected = filedialog.askdirectory(
        title="저장경로를 선택하세요", initialdir=r"C:\Users\jangt\Downloads")
    if folder_selected == "":  # 사용자가 취소
        return
    txt_dest_path.delete(0, END)  # 0부터 끝까지 기존에 있던 경로 삭제
    txt_dest_path.insert(0, folder_selected)  # 맨 처음에 넣는다.


# 이미지 통합
def merge_image():
    # print("가로넓이: ", cmb_width.get())
    # print("간격: ", cmb_space.get())
    # print("포맷: ", cmb_format.get())
    try:
        img_width = cmb_width.get()
        if img_width == "원본유지":
            img_width = -1  # -1 일떄는 원본 기준으로 이미지 통합
        else:
            img_width = int(img_width)

        img_space = cmb_space.get()
        if img_space == "좁게":
            img_space = 30
        elif img_space == "보통":
            img_space = 60
        elif img_space == "넓게":
            img_space = 90
        else:
            img_space = 0

        # print(list_file.get(0, END)) #모든 파일 목록
        # 0~끝까지 불러와 x에 저장 [size=160x160 at 0x172B46760D0>, size=80x80 at 0x1CD699CF5D0>...]
        images = [Image.open(x) for x in list_file.get(0, END)]

        # 이미지 사이즈를 리스트에 넣어서 하나씩 처리
        image_size = []  # (width1, height1), (width2, height2)...
        if img_width > -1:  # 크기 변경
            image_size = [(int(img_width), int(img_width * x.size[1] / x.size[0]))
                          for x in images]  # 원본 width : 원본 height = 변경 width : 변경 height
            # print(image_size) -> [(1024, 1024), (1024, 1024), (1024, 1024), (1024, 1024), (1024, 1024)]
        else:  # -1: 사이즈 그대로 사용
            image_size = [(x.size[0], x.size[1]) for x in images]

        # size -> size[0]: width, size[1]: height
        # width = [x.size[0] for x in images]
        # height = [x.size[1] for x in images] #[(10,10), (20,20), (30,30)...]
        # max(): 입력받은 값들 중 최댓값 반환, sum(): 입력받은 값을 모두 더한 값 반환
        # width, height = zip(*(x.size for x in images)) #[(10,10), (20,20), (30,30)...] 첫 번째 값들을 width에 두 번째 값들을 height에 저장
        width, height = zip(*(image_size))
        max_width, total_height = max(width), sum(height)  # 최대 넓이 전체 높이 구함

        # 스케치북
        if img_space > 0:  # 이미지 간격
            total_height += img_space * (len(images) - 1)
        result_img = Image.new("RGB", (max_width, total_height), (255, 255, 255))
        y_offset = 0  # y위치
        # for img in images:
        #     result_img.paste(img, (0, y_offset))
        #     y_offset += img.size[1] #height 값 만큼 더한다.
        for idx, img in enumerate(images):
            # width가 원본유지가 아니면 이미지 크기 조절
            if img_width > -1:
                # print(image_size )=[(1024, 1024), (1024, 1024), (1024, 1024), (1024, 1024), (1024, 1024)] 크기 1024일 경우
                img = img.resize(image_size[idx])
                # size=1024x1024 at 0x18614790590, size=1024x1024 at 0x18614790590, size=1024x1024 at 0x18614790590...
                # print(img)
            result_img.paste(img, (0, y_offset))
            y_offset += (img.size[1] + img_space)  # height 값 + 사용자가 지정한 간격

            progress = (idx + 1) / len(images) * 100  # 실제 percent 정보 계산
            p_var.set(progress)
            progressbar.update()

        # 포멧 옵션 처리
        img_format = cmb_format.get().lower()  # 값을 받아와 소문자로 변경
        file_name = "ZZangtae_Photo." + img_format
        dest_path = os.path.join(txt_dest_path.get(), file_name)
        result_img.save(dest_path)
        msgbox.showinfo("알림", "작업이 완료되었습니다.")
    except Exception as err:
        msgbox.showerror("에러", err)

# 시작


def start():
    # 각 옵션들 값을 확인
    # print("가로넓이: ", cmb_width.get())
    # print("간격: ", cmb_space.get())
    # print("포맷: ", cmb_format.get())
    # 파일 목록 확인
    if list_file.size() == 0:  # 크기 -> 파일이 없다.
        msgbox.showwarning("경고", "이미지 파일을 추가하세요.")
        return
    if len(txt_dest_path.get()) == 0:  # 글자를 가져온다 = get()
        msgbox.showwarning("경고", "저장경로를 선택하세요.")

    merge_image()
###############################################################################################


# 파일 프레임 (파일 추가, 선택 삭제)
file_frame = Frame(root)
file_frame.pack(fill="both")  # expand="True"

btn_add_file = Button(file_frame, text="파일 추가", command=add_file)
btn_add_file.pack(side="left", padx=5, pady=5)
btn_del_file = Button(file_frame, text="선택 삭제", command=del_file)
btn_del_file.pack(side="right", padx=5, pady=5)


# 리스트 프레임, 스크롤
list_frame = LabelFrame(root, text="사진 목록")
list_frame.pack(fill="x", padx=5, pady=5)

scrollbar_list = Scrollbar(list_frame)  # pack(side="right", fill="y")
scrollbar_list.pack(side="right", fill="y")

list_file = Listbox(list_frame, selectmode="extended", height=15,
                    yscrollcommand=scrollbar_list.set)  # list_ file = Listbox(넣는곳)
list_file.pack(side="left", fill="both", expand=True, padx=5, pady=5)
scrollbar_list.config(command=list_file.yview)  # list_file이 yvuew를 맵핑하도록


# 저장 경로 프레임
path_frame = LabelFrame(root, text="저장 경로")
path_frame.pack(fill="x", padx=5, pady=5, ipady=5)

txt_dest_path = Entry(path_frame)  # entry여서 0~END, text라면 "1.0", END
txt_dest_path.pack(side="left", fill="x", expand=True,
                   ipady=4, padx=5, pady=5)  # ipad=높이 변경

btn_dest_path = Button(path_frame, text="찾아보기",
                       width=10, command=browse_dest_path)
btn_dest_path.pack(side="right", padx=5, pady=5)


# 옵션 프레임
frame_option = LabelFrame(root, text="옵션")
frame_option.pack(fill="x", padx=5, pady=5, ipady=5)

# 가로 옵션
lbl_width = Label(frame_option, text="가로넓이", width=8)
lbl_width.pack(side="left", padx=3, pady=3)
opt_width = ["원본유지", "1024", "800", "640"]
# 정의한 값만 받는다.
cmb_width = ttk.Combobox(frame_option, state="readonly",
                         values=opt_width, width=10)
cmb_width.current(0)  # 0번째 인덱스 값 선택
cmb_width.pack(side="left")
# 간격 옵션
lbl_space = Label(frame_option, text="간격", width=8)
lbl_space.pack(side="left")
opt_space = ["없음", "좁게", "보통", "넓게"]
# 정의한 값만 받는다.
cmb_space = ttk.Combobox(frame_option, state="readonly",
                         values=opt_space, width=10)
cmb_space.current(0)  # 0번째 인덱스 값 선택
cmb_space.pack(side="left")
# 파일 포맷 옵션
lbl_format = Label(frame_option, text="포멧", width=8)
lbl_format.pack(side="left")
opt_format = ["PNG", "JPG", "BMP"]
# 정의한 값만 받는다.
cmb_format = ttk.Combobox(
    frame_option, state="readonly", values=opt_format, width=10)
cmb_format.current(0)  # 0번째 인덱스 값 선택
cmb_format.pack(side="left")


# 진행상황 progress bar
frame_progress = LabelFrame(root, text="진행상황")
frame_progress.pack(fill="x", padx=5, pady=5, ipady=5)
p_var = DoubleVar()
progressbar = ttk.Progressbar(frame_progress, maximum=100, variable=p_var)
progressbar.pack(fill="x", padx=5, pady=5)


# 실행 프레임
frame_run = Frame(root)
frame_run.pack(fill="x", padx=5, pady=5, ipady=5)
btn_close = Button(frame_run, text="닫기", width=12, command=root.quit)
btn_close.pack(side="right", padx=3, pady=3)
btn_start = Button(frame_run, text="시작", width=12, command=start)
btn_start.pack(side="right", padx=3, pady=3)

#########################################################################
root.mainloop()  # 창이 닫히지 않도록 한다.
