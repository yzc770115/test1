import pygame
import sys
import random

# 初始化常量
WINDOW_HEIGHT = 800  # 基准高度
WINDOW_WIDTH = int(WINDOW_HEIGHT * 9/16)  # 根据9:16比例计算宽度 (约450)
GRID_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 16

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# 在类定义前添加形状常量
# 方块形状定义（每个形状包含4种旋转状态）
SHAPES = {
    'I': [
        [[0, 0, 0, 0],
         [1, 1, 1, 1],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
        [[0, 0, 1, 0],
         [0, 0, 1, 0],
         [0, 0, 1, 0],
         [0, 0, 1, 0]],
        [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [1, 1, 1, 1],
         [0, 0, 0, 0]],
        [[0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 0, 0]]
    ],
    'O': [
        [[1, 1],
         [1, 1]]
    ],
    'T': [
        [[0, 1, 0],
         [1, 1, 1],
         [0, 0, 0]],
        [[0, 1, 0],
         [0, 1, 1],
         [0, 1, 0]],
        [[0, 0, 0],
         [1, 1, 1],
         [0, 1, 0]],
        [[0, 1, 0],
         [1, 1, 0],
         [0, 1, 0]]
    ],
    'L': [
        [[0, 0, 1],
         [1, 1, 1],
         [0, 0, 0]],
        [[0, 1, 0],
         [0, 1, 0],
         [0, 1, 1]],
        [[0, 0, 0],
         [1, 1, 1],
         [1, 0, 0]],
        [[1, 1, 0],
         [0, 1, 0],
         [0, 1, 0]]
    ],
    'J': [
        [[1, 0, 0],
         [1, 1, 1],
         [0, 0, 0]],
        [[0, 1, 1],
         [0, 1, 0],
         [0, 1, 0]],
        [[0, 0, 0],
         [1, 1, 1],
         [0, 0, 1]],
        [[0, 1, 0],
         [0, 1, 0],
         [1, 1, 0]]
    ],
    'S': [
        [[0, 1, 1],
         [1, 1, 0],
         [0, 0, 0]],
        [[0, 1, 0],
         [0, 1, 1],
         [0, 0, 1]],
        [[0, 0, 0],
         [0, 1, 1],
         [1, 1, 0]],
        [[1, 0, 0],
         [1, 1, 0],
         [0, 1, 0]]
    ],
    'Z': [
        [[1, 1, 0],
         [0, 1, 1],
         [0, 0, 0]],
        [[0, 0, 1],
         [0, 1, 1],
         [0, 1, 0]],
        [[0, 0, 0],
         [1, 1, 0],
         [0, 1, 1]],
        [[0, 1, 0],
         [1, 1, 0],
         [1, 0, 0]]
    ]
}

# 方块颜色定义
SHAPE_COLORS = {
    'I': (0, 255, 255),   # 青色
    'O': (255, 255, 0),   # 黄色
    'T': (128, 0, 128),   # 紫色
    'L': (255, 165, 0),   # 橙色
    'J': (0, 0, 255),     # 蓝色
    'S': (0, 255, 0),     # 绿色
    'Z': (255, 0, 0)      # 红色
}

class Particle:
    """表示单个粒子的类"""
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 4)
        # 随机速度和方向
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-3, 0)
        self.life = 1.0  # 生命值从1递减到0

    def update(self):
        """更新粒子位置和生命值"""
        self.x += self.vx
        self.vy += 0.1  # 重力效果
        self.y += self.vy
        self.life -= 0.02  # 逐渐消失
        return self.life > 0

    def draw(self, screen):
        """绘制粒子"""
        alpha = int(self.life * 255)
        color = (*self.color, alpha)
        surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.rect(surf, color, (0, 0, self.size, self.size))
        screen.blit(surf, (self.x, self.y))

class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.is_hovered = False

    def draw(self, screen):
        color = (min(self.color[0] + 30, 255),
                min(self.color[1] + 30, 255),
                min(self.color[2] + 30, 255)) if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class Tetris:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()  # 初始化音频系统
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Tetris')
        self.clock = pygame.time.Clock()
        
        # 初始化音效属性为None
        self.move_sound = None
        self.rotate_sound = None
        self.drop_sound = None
        self.clear_sound = None
        self.game_over_sound = None
        self.sounds_loaded = False
        
        # 尝试加载音效
        try:
            self.move_sound = pygame.mixer.Sound('sounds/move.wav')
            self.rotate_sound = pygame.mixer.Sound('sounds/rotate.wav')
            self.drop_sound = pygame.mixer.Sound('sounds/drop.wav')
            self.clear_sound = pygame.mixer.Sound('sounds/clear.wav')
            self.game_over_sound = pygame.mixer.Sound('sounds/gameover.wav')
            
            # 加载背景音乐
            pygame.mixer.music.load('sounds/background.mp3')
            pygame.mixer.music.set_volume(0.5)  # 设置音量为50%
            
            self.sounds_loaded = True
            print("所有音效文件加载成功！")
        except Exception as e:
            print(f"警告：无法加载音效文件: {str(e)}")
            self.sounds_loaded = False
        
        # 在游戏状态中添加暂停状态
        self.game_state = 'menu'  # 'menu', 'playing', 'paused', 'game_over', 'level_complete'
        
        # 定义关卡相关的属性
        self.level_score_goals = {
            1: 1000,
            2: 2000,
            3: 3000
        }
        self.fall_speeds = {
            1: 500,  # 第1关：500ms
            2: 400,  # 第2关：400ms
            3: 300   # 第3关：300ms
        }
        
        # 创建开始按钮
        button_width = 200
        button_height = 50
        button_x = WINDOW_WIDTH // 2 - button_width // 2
        button_y = WINDOW_HEIGHT * 7 // 8 - button_height // 2  # 修改这里，将按钮移到屏幕底部1/8处
        self.start_button = Button(button_x, button_y, button_width, button_height, 
                                 "START GAME", (0, 100, 0))
        
        # 定义底部边距
        self.bottom_margin = 50  # 添加底部边距
        
        # 加载背景图片
        try:
            self.menu_bg = pygame.image.load('images/menu_bg.jpg')
            self.menu_bg = pygame.transform.scale(self.menu_bg, (WINDOW_WIDTH, WINDOW_HEIGHT))
            self.game_bg = pygame.image.load('images/game_bg.jpg')  # 添加游戏背景
            self.game_bg = pygame.transform.scale(self.game_bg, (WINDOW_WIDTH, WINDOW_HEIGHT))
            print("背景图片加载成功！")
        except Exception as e:
            print(f"警告：无法加载背景图片: {str(e)}")
            self.menu_bg = None
            self.game_bg = None
        
        # 创建暂停按钮
        pause_button_width = 100
        pause_button_height = 40
        pause_button_x = 20  # 左边距
        pause_button_y = WINDOW_HEIGHT - pause_button_height - 20  # 底部边距
        self.pause_button = Button(pause_button_x, pause_button_y, 
                                 pause_button_width, pause_button_height, 
                                 "PAUSE", (100, 100, 100))  # 灰色按钮
        
        # 创建暂停界面的按钮
        button_width = 200
        button_height = 50
        button_spacing = 20  # 按钮之间的间距
        
        # 计算按钮位置，使其在屏幕中央
        resume_button_x = WINDOW_WIDTH // 2 - button_width // 2
        resume_button_y = WINDOW_HEIGHT // 2 - button_height - button_spacing // 2
        
        quit_button_x = WINDOW_WIDTH // 2 - button_width // 2
        quit_button_y = WINDOW_HEIGHT // 2 + button_spacing // 2
        
        self.resume_button = Button(resume_button_x, resume_button_y, 
                                  button_width, button_height, 
                                  "RESUME", (0, 100, 0))  # 绿色按钮
        
        self.quit_button = Button(quit_button_x, quit_button_y, 
                                button_width, button_height, 
                                "QUIT", (100, 0, 0))  # 红色按钮
        
        # 初始化游戏相关属性
        self.initialize_game()
        self.state_change_time = 0  # 用于控制状态切换的计时
        self.particles = []  # 添加粒子列表
    
    def initialize_game(self):
        """初始化游戏相关的所有属性"""
        # 游戏区域位置参数
        self.side_margin = (WINDOW_WIDTH - (GRID_SIZE * GRID_WIDTH)) // 2  # 水平居中
        self.top_margin = 200  # 顶部边距
        
        self.game_area = pygame.Rect(
            self.side_margin,
            self.top_margin,
            GRID_SIZE * GRID_WIDTH,
            GRID_SIZE * GRID_HEIGHT
        )
        
        # 调整预览区域位置到屏幕顶部
        preview_size = 4 * GRID_SIZE
        self.preview_area = pygame.Rect(
            WINDOW_WIDTH - preview_size - 20,  # 右侧边距20像素
            20,  # 顶部边距20像素
            preview_size,
            preview_size
        )
        
        # 确保游戏区域底部不会超出窗口
        if self.game_area.bottom + self.bottom_margin > WINDOW_HEIGHT:
            # 如果超出，向上调整游戏区域
            self.game_area.y = WINDOW_HEIGHT - GRID_SIZE * GRID_HEIGHT - self.bottom_margin
        
        # 初始化其他属性
        self.score = 0
        self.level = 1
        self.board = [[None for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]
        self.fall_speed = self.fall_speeds[self.level]
        self.last_fall_time = pygame.time.get_ticks()
        
        # 初始化方块属性
        self.next_shape = random.choice(list(SHAPES.keys()))
        self.next_piece = SHAPES[self.next_shape][0]
        
        # 确保当前方块被正确初始化
        self.current_shape = random.choice(list(SHAPES.keys()))
        self.current_rotation = 0
        self.current_piece = SHAPES[self.current_shape][self.current_rotation]
        self.current_x = GRID_WIDTH // 2 - len(self.current_piece[0]) // 2
        self.current_y = 0
    
    def play_sound(self, sound):
        """安全地播放音效"""
        if self.sounds_loaded and sound is not None:
            try:
                sound.play()
            except:
                print("播放音效时出错")
    
    def start_background_music(self):
        """开始播放背景音乐"""
        if self.sounds_loaded:
            pygame.mixer.music.play(-1)  # -1表示循环播放
    
    def stop_background_music(self):
        """停止背景音乐"""
        if self.sounds_loaded:
            pygame.mixer.music.stop()
    
    def new_piece(self):
        """生成新的方块，检查游戏是否结束"""
        self.current_shape = self.next_shape
        self.current_rotation = 0
        self.current_piece = SHAPES[self.current_shape][self.current_rotation]
        
        # 设置方块初始位置
        self.current_x = GRID_WIDTH // 2 - len(self.current_piece[0]) // 2
        self.current_y = 0
        
        # 生成新的预览方块
        self.next_shape = random.choice(list(SHAPES.keys()))
        self.next_piece = SHAPES[self.next_shape][0]
        
        # 检查游戏是否结束
        if self.check_collision():
            self.play_sound(self.game_over_sound)
            self.stop_background_music()
            self.game_state = 'game_over'
            self.state_change_time = pygame.time.get_ticks()
    
    def check_collision(self):
        """检查当前方块是否发生碰撞"""
        for y in range(len(self.current_piece)):
            for x in range(len(self.current_piece[y])):
                if self.current_piece[y][x] == 0:
                    continue
                
                new_x = self.current_x + x
                new_y = self.current_y + y
                
                if (new_x < 0 or new_x >= GRID_WIDTH or 
                    new_y >= GRID_HEIGHT or 
                    (new_y >= 0 and self.board[new_y][new_x] is not None)):
                    return True
        return False
    
    def lock_piece(self):
        """将当前方块锁定到游戏板上并检查消行"""
        # 锁定方块
        for y in range(len(self.current_piece)):
            for x in range(len(self.current_piece[y])):
                if self.current_piece[y][x] == 1:
                    self.board[self.current_y + y][self.current_x + x] = self.current_shape
        
        # 检查并处理消行
        self.clear_lines()
    
    def create_particles(self, row):
        """为消除的行创建粒子效果"""
        for x in range(GRID_WIDTH):
            if self.board[row][x]:
                color = SHAPE_COLORS[self.board[row][x]]
                # 为每个方块创建多个粒子
                for _ in range(15):  # 每个方块15个粒子
                    px = self.game_area.left + x * GRID_SIZE + random.randint(0, GRID_SIZE)
                    py = self.game_area.top + row * GRID_SIZE + random.randint(0, GRID_SIZE)
                    self.particles.append(Particle(px, py, color))

    def clear_lines(self):
        """检查并清除已填满的行"""
        lines_cleared = 0
        y = GRID_HEIGHT - 1
        while y >= 0:
            if self.is_line_full(y):
                self.create_particles(y)  # 在消除行之前创建粒子
                self.remove_line(y)
                lines_cleared += 1
            else:
                y -= 1
        
        # 播放消行音效
        if lines_cleared > 0:
            self.play_sound(self.clear_sound)
            
        # 计算得分
        if lines_cleared > 0:
            scores = {1: 100, 2: 300, 3: 500, 4: 800}
            self.score += scores.get(lines_cleared, 0)
    
    def is_line_full(self, y):
        """检查指定行是否已填满"""
        return all(self.board[y][x] is not None for x in range(GRID_WIDTH))
    
    def remove_line(self, y):
        """删除指定行并使上方方块下落"""
        # 从指定行开始，将每一行都复制为上一行的内容
        for cur_y in range(y, 0, -1):
            self.board[cur_y] = self.board[cur_y - 1][:]
        # 最顶行设为空
        self.board[0] = [None] * GRID_WIDTH
    
    def draw_piece(self):
        """绘制当前方块"""
        if not self.current_piece or self.game_state != 'playing':
            return
        
        for y in range(len(self.current_piece)):
            for x in range(len(self.current_piece[y])):
                if self.current_piece[y][x] == 1:
                    rect = pygame.Rect(
                        self.game_area.left + (self.current_x + x) * GRID_SIZE,
                        self.game_area.top + (self.current_y + y) * GRID_SIZE,
                        GRID_SIZE,
                        GRID_SIZE
                    )
                    pygame.draw.rect(self.screen, SHAPE_COLORS[self.current_shape], rect)
                    pygame.draw.rect(self.screen, WHITE, rect, 1)
    
    def draw_board(self):
        """绘制已经固定的方块"""
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.board[y][x]:
                    rect = pygame.Rect(
                        self.game_area.left + x * GRID_SIZE,
                        self.game_area.top + y * GRID_SIZE,
                        GRID_SIZE,
                        GRID_SIZE
                    )
                    pygame.draw.rect(self.screen, SHAPE_COLORS[self.board[y][x]], rect)
                    pygame.draw.rect(self.screen, WHITE, rect, 1)
    
    def draw_grid(self):
        """绘制网格"""
        for x in range(GRID_WIDTH + 1):
            pygame.draw.line(
                self.screen,
                GRAY,
                (self.game_area.left + x * GRID_SIZE, self.game_area.top),
                (self.game_area.left + x * GRID_SIZE, self.game_area.bottom)
            )
        
        for y in range(GRID_HEIGHT + 1):
            pygame.draw.line(
                self.screen,
                GRAY,
                (self.game_area.left, self.game_area.top + y * GRID_SIZE),
                (self.game_area.right, self.game_area.top + y * GRID_SIZE)
            )
    
    def rotate_piece(self):
        """旋转当前方块"""
        # 保存当前状态以便发生碰撞时恢复
        old_rotation = self.current_rotation
        old_piece = self.current_piece
        
        # 获取下一个旋转状态
        self.current_rotation = (self.current_rotation + 1) % len(SHAPES[self.current_shape])
        self.current_piece = SHAPES[self.current_shape][self.current_rotation]
        
        # 如果旋转后发生碰撞，尝试进行墙踢（wall kick）
        if self.check_collision():
            # 尝试向左移动
            self.current_x -= 1
            if self.check_collision():
                # 尝试向右移动
                self.current_x += 2
                if self.check_collision():
                    # 如果都不行，恢复原状
                    self.current_x -= 1
                    self.current_rotation = old_rotation
                    self.current_piece = old_piece
    
    def draw_score(self):
        """绘制分数"""
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'SCORE: {self.score}', True, WHITE)
        # 调整分数显示位置到屏幕顶部
        score_pos = (20, 20)  # 左上角位置
        self.screen.blit(score_text, score_pos)
    
    def hard_drop(self):
        """方块快速下落到底部"""
        while not self.check_collision():
            self.current_y += 1
        
        # 回退一步（因为上面的循环会多下落一格）
        self.current_y -= 1
        # 锁定方块并生成新方块
        self.lock_piece()
        self.new_piece()
    
    def draw_preview(self):
        """绘制预览区域和下一个方块"""
        # 绘制预览区域边框
        pygame.draw.rect(self.screen, WHITE, self.preview_area, 2)
        
        # 修改为英文
        font = pygame.font.Font(None, 30)
        text = font.render("NEXT:", True, WHITE)
        self.screen.blit(text, (self.preview_area.x, self.preview_area.y - 30))
        
        # 计算预览方块的位置，使其在预览区域居中
        piece_height = len(self.next_piece)
        piece_width = len(self.next_piece[0])
        start_x = self.preview_area.x + (self.preview_area.width - piece_width * GRID_SIZE) // 2
        start_y = self.preview_area.y + (self.preview_area.height - piece_height * GRID_SIZE) // 2
        
        # 绘制预览方块
        for y in range(piece_height):
            for x in range(piece_width):
                if self.next_piece[y][x] == 1:
                    rect = pygame.Rect(
                        start_x + x * GRID_SIZE,
                        start_y + y * GRID_SIZE,
                        GRID_SIZE, GRID_SIZE
                    )
                    pygame.draw.rect(self.screen, SHAPE_COLORS[self.next_shape], rect)
                    pygame.draw.rect(self.screen, WHITE, rect, 1)
    
    def check_level_up(self):
        """检查是否达到关卡目标"""
        if self.level < 3 and self.score >= self.level_score_goals[self.level]:
            self.level += 1
            self.fall_speed = self.fall_speeds[self.level]
            self.game_state = 'level_complete'
            self.state_change_time = pygame.time.get_ticks()
            return True
        elif self.level == 3 and self.score >= self.level_score_goals[self.level]:
            self.game_state = 'game_complete'
            self.state_change_time = pygame.time.get_ticks()
            return True
        return False
    
    def draw_level_info(self):
        """绘制关卡信息"""
        font = pygame.font.Font(None, 36)
        # 调整关卡信息显示位置
        level_text = font.render(f'LEVEL: {self.level}', True, WHITE)
        level_pos = (20, 60)  # 分数下方
        self.screen.blit(level_text, level_pos)
        
        goal_text = font.render(f'GOAL: {self.level_score_goals[self.level]}', True, WHITE)
        goal_pos = (20, 100)  # 关卡信息下方
        self.screen.blit(goal_text, goal_pos)
    
    def draw_level_complete(self):
        """绘制关卡完成画面"""
        font = pygame.font.Font(None, 48)
        if self.game_state == 'level_complete':
            text = font.render(f'LEVEL {self.level-1} COMPLETE!', True, WHITE)
            subtext = font.render('GET READY FOR NEXT LEVEL...', True, WHITE)
        else:  # game_complete
            text = font.render('CONGRATULATIONS!', True, WHITE)
            subtext = font.render(f'FINAL SCORE: {self.score}', True, WHITE)
            
        text_rect = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 30))
        subtext_rect = subtext.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 30))
        
        self.screen.blit(text, text_rect)
        self.screen.blit(subtext, subtext_rect)
    
    def draw_menu(self):
        """绘制主菜单界面"""
        # 绘制背景图片
        if self.menu_bg:
            self.screen.blit(self.menu_bg, (0, 0))
        else:
            self.screen.fill(BLACK)
        
        # 绘制开始按钮
        self.start_button.draw(self.screen)
    
    def draw_game_over(self):
        """绘制游戏结束画面"""
        # 创建半透明的黑色遮罩
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))
        
        # 绘制游戏结束文本
        font = pygame.font.Font(None, 64)
        game_over_text = font.render("GAME OVER", True, WHITE)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        
        font_small = pygame.font.Font(None, 36)
        return_text = font_small.render("Press SPACE to return to menu", True, WHITE)
        
        # 居中显示文本
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 50))
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 10))
        return_rect = return_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 70))
        
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(return_text, return_rect)
    
    def draw_pause_screen(self):
        """绘制暂停界面"""
        # 创建半透明的黑色遮罩
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(128)  # 设置透明度
        self.screen.blit(overlay, (0, 0))
        
        # 绘制按钮
        self.resume_button.draw(self.screen)
        self.quit_button.draw(self.screen)

    def update_particles(self):
        """更新所有粒子的状态"""
        self.particles = [p for p in self.particles if p.update()]

    def draw_particles(self):
        """绘制所有粒子"""
        for particle in self.particles:
            particle.draw(self.screen)

    def run(self):
        while True:
            current_time = pygame.time.get_ticks()
            
            # 事件处理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if self.game_state == 'menu':
                    if self.start_button.handle_event(event):
                        self.game_state = 'playing'
                        self.initialize_game()
                        self.start_background_music()
                
                elif self.game_state == 'playing':
                    # 处理暂停按钮点击
                    if self.pause_button.handle_event(event):
                        self.game_state = 'paused'
                        pygame.mixer.music.pause()
                    
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self.current_x -= 1
                            if self.check_collision():
                                self.current_x += 1
                            else:
                                self.play_sound(self.move_sound)
                        elif event.key == pygame.K_RIGHT:
                            self.current_x += 1
                            if self.check_collision():
                                self.current_x -= 1
                            else:
                                self.play_sound(self.move_sound)
                        elif event.key == pygame.K_DOWN:
                            self.current_y += 1
                            if self.check_collision():
                                self.current_y -= 1
                            else:
                                self.play_sound(self.move_sound)
                        elif event.key == pygame.K_UP:
                            self.rotate_piece()
                            self.play_sound(self.rotate_sound)
                        elif event.key == pygame.K_SPACE:
                            while not self.check_collision():
                                self.current_y += 1
                            self.current_y -= 1
                            self.play_sound(self.drop_sound)
                            self.lock_piece()
                            self.new_piece()
                
                elif self.game_state == 'paused':
                    # 处理暂停界面的按钮点击
                    if self.resume_button.handle_event(event):
                        self.game_state = 'playing'
                        pygame.mixer.music.unpause()
                    elif self.quit_button.handle_event(event):
                        self.game_state = 'menu'
                        pygame.mixer.music.stop()  # 停止背景音乐
                    
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            self.game_state = 'playing'
                            pygame.mixer.music.unpause()
                
                elif self.game_state == 'game_over':
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.game_state = 'menu'
            
            # 更新游戏状态
            if self.game_state == 'menu':
                self.screen.fill(BLACK)
                self.draw_menu()
            
            elif self.game_state == 'playing':
                if current_time - self.last_fall_time > self.fall_speed:
                    self.current_y += 1
                    if self.check_collision():
                        self.current_y -= 1
                        self.lock_piece()
                        self.new_piece()
                    self.last_fall_time = current_time
                
                # 绘制游戏背景
                if self.game_bg:
                    self.screen.blit(self.game_bg, (0, 0))
                else:
                    self.screen.fill(BLACK)
                
                pygame.draw.rect(self.screen, WHITE, self.game_area, 2)
                self.draw_grid()
                self.draw_board()
                self.draw_piece()
                self.draw_score()
                self.draw_preview()
                self.draw_level_info()
                
                # 更新和绘制粒子效果
                self.update_particles()
                self.draw_particles()
                
                # 绘制暂停按钮
                self.pause_button.text = "PAUSE"
                self.pause_button.draw(self.screen)
            
            elif self.game_state == 'paused':
                # 先绘制游戏画面
                if self.game_bg:
                    self.screen.blit(self.game_bg, (0, 0))
                else:
                    self.screen.fill(BLACK)
                
                pygame.draw.rect(self.screen, WHITE, self.game_area, 2)
                self.draw_grid()
                self.draw_board()
                self.draw_piece()
                self.draw_score()
                self.draw_preview()
                self.draw_level_info()
                
                # 在游戏画面上绘制暂停界面
                self.draw_pause_screen()
            
            elif self.game_state == 'game_over':
                # 保持游戏画面，在上面绘制游戏结束信息
                self.draw_game_over()
            
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == '__main__':
    game = Tetris()
    game.run() 