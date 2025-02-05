import pygame
import sys

print("开始初始化 Pygame...")
pygame.init()
print("Pygame 初始化完成")

print("创建窗口...")
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Pygame测试')
print("窗口创建完成")

print("进入主循环...")
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("退出程序...")
            pygame.quit()
            sys.exit()
    
    screen.fill((255, 255, 255))
    pygame.display.flip() 