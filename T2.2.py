import pygame
import random

pygame.init()

# Cửa sổ game
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption('RunningBro')

# Icon và background
icon = pygame.image.load(r'image\icon.jpg')
pygame.display.set_icon(icon)

def main():
    running = True
    play_button_img = pygame.image.load(r'image/playbutton.png')  # Load hình ảnh cho nút Play
    play_button_img = pygame.transform.scale(play_button_img, (300, 200))
    background = pygame.image.load(r'image/background.jpg')  # Icon và background
    background = pygame.transform.scale(background, (1000, 700))

    back_button_img = pygame.image.load(r'image/backbutton.png')  # Load hình ảnh cho nút Back
    back_button_img = pygame.transform.scale(back_button_img, (100, 50))
    back_button_rect = back_button_img.get_rect(topleft=(20, 20))

    mbappe = pygame.image.load(r"image\\mbappe.png").convert_alpha()  #  convert_alpha() để giữ phần nền trong suốt
    mbappe = pygame.transform.scale(mbappe, (300, 200))
    mbappe_rect= mbappe.get_rect(topleft=(50,390))
    show_back_button = False  # Biến để xác định xem nút Back có hiển thị hay không
    show_mbappe = False  # Biến để xác định xem ảnh Mbappe có hiển thị hay không
    show_gameplay = False  # Biến để xác định xem gameplay có hiển thị hay không
    show_clock = False
    # Các biến gameplay
    clock = pygame.time.Clock()
    WHITE = (255, 255, 255)
    font = pygame.font.SysFont(None, 50)
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    letter_images = {letter: font.render(letter, True, WHITE) for letter in letters}

    class Letter:
        def __init__(self, lane, speed=1):
            self.letter = random.choice(letters)
            self.image = letter_images[self.letter]
            self.speed = speed
            self.lane = lane
            self.rect = self.image.get_rect(midbottom=(1000, self.lane))

        def update(self):
            self.rect.x -= self.speed

    letters_list = []
    score = 0
    lives = 3

    speed_increase_interval = 5  # Khoảng thời gian tăng tốc độ (giây)
    speed_increase_amount = 1  # Số đơn vị tốc độ tăng sau mỗi khoảng thời gian

    speed_update_time = pygame.time.get_ticks() / 1000  # Thời gian kể từ lần cuối cùng tốc độ được cập nhật

    def start_gameplay():
        nonlocal letters_list
        lanes = [400, 480, 560]  # 3 dòng chữ
        letters_list = [Letter(lane) for lane in lanes]  # Khởi tạo danh sách các chữ cái

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:  #tạo để ấn vào được nút play
                mouse_pos = pygame.mouse.get_pos()
                if play_button_img is not None:  # Kiểm tra nút play có tồn tại không
                    button_rect = play_button_img.get_rect(topleft=(370, 170))
                    if button_rect.collidepoint(mouse_pos):
                        background_gp = pygame.image.load(r"image\\gp.jpg").convert()
                        background = pygame.transform.scale(background_gp, (1000, 700))
                        play_button_img = None  # Mất nút play
                        show_back_button = True  # Hiển thị nút Back khi chuyển đổi màn hình
                        show_mbappe = True  # Hiển thị ảnh Mbappe khi chuyển đổi màn hình
                        show_gameplay = True  # Hiển thị gameplay khi chuyển đổi màn hình
                        show_clock = True
                        start_gameplay()  # Bắt đầu trò chơi
                        start_time = pygame.time.get_ticks() 
                elif back_button_rect.collidepoint(mouse_pos):
                    # Xử lý sự kiện khi nhấn nút back và quay lại màn hình trước đó
                    background = pygame.image.load(r'image/background.jpg').convert()
                    background = pygame.transform.scale(background, (1000, 700))
                    play_button_img = pygame.image.load(r'image/playbutton.png')  # Tạo lại nút play
                    play_button_img = pygame.transform.scale(play_button_img, (300, 200))
                    show_back_button = False  # Ẩn nút Back khi quay lại background
                    show_mbappe = False  # Ẩn ảnh Mbappe khi quay lại background
                    show_gameplay = False  # Ẩn gameplay khi quay lại background
                    show_clock = False
            elif event.type == pygame.KEYDOWN:  # Xử lý sự kiện phím được nhấn
                if show_gameplay:  # Chỉ xử lý khi đang hiển thị gameplay
                    # Kiểm tra xem phím được nhấn có trùng với chữ cái hiện tại không
                    for letter in letters_list:
                        if event.unicode.lower() == letter.letter.lower():
                            # Nếu trùng, loại bỏ chữ cái đó khỏi danh sách
                            letters_list.remove(letter)
                            score += 1  # Tăng điểm khi gõ đúng
                            break

        screen.blit(background, (0, 0))
        if play_button_img:  # Chỉ hiển thị nút play nếu play_button_img không phải None
            screen.blit(play_button_img, (370, 170))
        
        # Hiển thị nút "Back" nếu biến show_back_button là True
        if show_back_button:
            screen.blit(back_button_img, (20, 20))

        if show_mbappe:  # Hiển thị ảnh Mbappe nếu show_mbappe là True
            screen.blit(mbappe, (50, 390))

        if show_gameplay:  # Hiển thị gameplay nếu show_gameplay là True
            for letter in letters_list:
                letter.update()
                screen.blit(letter.image, letter.rect)
                if letter.rect.colliderect(mbappe_rect):
                    lives -= 1
                    letters_list.remove(letter)
               
            if len(letters_list) < 3:
                    lanes = [400, 480, 560]  # Các dòng chữ
                    letters_list.append(Letter(random.choice(lanes)))  # Thêm chữ cái mới
            
            score_text = font.render(f"Score: {score}", True, WHITE)
            lives_text = font.render(f"Lives: {lives}", True, WHITE)
            screen.blit(score_text, (900 - score_text.get_width(), 20))  # Hiển thị score ở góc phải trên cùng
            screen.blit(lives_text, (900 - lives_text.get_width(), 60))  # Hiển thị lives ở góc phải bên dưới score
            if show_clock:  # Hiển thị đồng hồ nếu show_clock là True
                elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # Thời gian đã trôi qua tính bằng giây
                clock_text = font.render(f"Time: {elapsed_time}s", True, WHITE)
                screen.blit(clock_text, (500 - clock_text.get_width() // 2, 20))  # Hiển thị đồng hồ ở giữa phía trên màn hình
                
            # Cập nhật thời gian đã trôi qua kể từ lần cuối cùng tốc độ được cập nhật
            current_time = pygame.time.get_ticks() / 1000
            time_since_update = current_time - speed_update_time
            
            if time_since_update >= speed_increase_interval:
                # Tăng tốc độ sau mỗi khoảng thời gian
                for letter in letters_list:
                    letter.speed += speed_increase_amount
                    print(letter.speed)
                speed_update_time = current_time  # Cập nhật thời gian lần cuối cùng tốc độ được cập nhật

        pygame.display.update()
        clock.tick(60)  # FPS là 60

if __name__ == "__main__":
    main()
